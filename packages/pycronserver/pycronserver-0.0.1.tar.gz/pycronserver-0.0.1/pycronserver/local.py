import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pycronserver.server import get_pycronserver


def create_config_folder(config_dir="~/.pycronserver"):
    os.makedirs(os.path.abspath(os.path.expanduser(config_dir)), exist_ok=True)


def load_config(config_file="~/.pycronserver/config.json"):
    with open(os.path.abspath(os.path.expanduser(config_file))) as f:
        return json.load(f)


def get_local_pycronserver(config_dir="~/.pycronserver"):
    create_config_folder(config_dir=config_dir)
    config = load_config(config_file=os.path.join(config_dir, "config.json"))
    engine = create_engine(config["connection_str"])
    session = sessionmaker(bind=engine)()
    if "username" in config.keys():
        username = config["username"]
    else:
        username = True
    if "user_id" in config.keys():
        user_id = config["user_id"]
    else:
        user_id = 1
    return get_pycronserver(
        engine=engine, session=session, username=username, user_id=user_id
    )
