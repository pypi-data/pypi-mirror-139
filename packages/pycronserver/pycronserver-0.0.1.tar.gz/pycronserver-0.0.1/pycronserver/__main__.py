import argparse
from pycronserver.local import get_local_pycronserver


def command_line_parser():
    """
    Main function primarly used for the command line interface
    """
    parser = argparse.ArgumentParser(prog="pycronserver")
    parser.add_argument(
        "crontab",
        help="Crontab timestamp",
    )
    args = parser.parse_args()
    pcs = get_local_pycronserver()
    pcs.execute_tasks(args.crontab)


if __name__ == "__main__":
    command_line_parser()
