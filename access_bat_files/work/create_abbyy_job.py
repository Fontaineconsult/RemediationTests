import os, sys
from pathlib import Path

def run():
    send_to_abby_server(int(sys.argv[1]))  # conversion_id
    update_abbyy_job_status(int(sys.argv[2]))  # file_id
    input()

if __name__ == '__main__':
    p = Path(__file__).parents[2]
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), p)))
    from job_scripts import send_to_abby_server, update_abbyy_job_status
    run()