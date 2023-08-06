import importlib
import json
from crontab import CronTab
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class CronTasks(Base):
    __tablename__ = "crontasks"
    id = Column(Integer, primary_key=True)
    crontab = Column(String)
    python_funct = Column(String)
    input_json = Column(String)
    user_id = Column(Integer)


class PyCronServer:
    def __init__(self, session, username=True, user_id=1):
        self._session = session
        self._username = username
        self._user_id = user_id

    def write_to_crontab(self):
        with CronTab(user=self._username) as cron:
            cron.remove_all(comment="pycronserver")
            for cron_tab in set(self._get_crontab_timesteps()):
                job = cron.new(
                    command="pycronserver '" + cron_tab + "'", comment="pycronserver"
                )
                job.setall(cron_tab)

    def store(self, crontab, python_funct_path, input_dict):
        self._session.add(
            CronTasks(
                crontab=crontab,
                python_funct=python_funct_path,
                input_json=json.dumps(input_dict),
                user_id=self._user_id,
            )
        )

    def execute_tasks(self, crontab, filter_by_user_id=True):
        if filter_by_user_id:
            query = (
                self._session.query(CronTasks)
                .filter(CronTasks.user_id == self._user_id)
                .filter(CronTasks.crontab == crontab)
            )
        else:
            query = self._session.query(CronTasks).filter(CronTasks.crontab == crontab)
        for task in query.all():
            execute_funct(
                module_funct=task.python_funct, input_dict=json.loads(task.input_json)
            )

    def _get_crontab_timesteps(self, filter_by_user_id=True):
        if filter_by_user_id:
            query = self._session.query(CronTasks.crontab).filter(
                CronTasks.user_id == self._user_id
            )
        else:
            query = self._session.query(CronTasks.crontab)
        return [entry[0] for entry in query.all()]

    @staticmethod
    def execute_funct(module_funct, input_dict):
        return execute_funct(module_funct=module_funct, input_dict=input_dict)


def execute_funct(module_funct, input_dict):
    module_funct_lst = module_funct.split(".")
    funct_name = module_funct_lst[-1]
    module_path = ".".join(module_funct_lst[:-1])
    module = importlib.import_module(module_path)
    funct = getattr(module, funct_name)
    return funct(**input_dict)


def get_pycronserver(engine, session, username=True, user_id=1):
    Base.metadata.create_all(engine)
    return PyCronServer(session=session, username=username, user_id=user_id)
