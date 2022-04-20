import os, sys

def run():
    send_to_abby_server(int(sys.argv[1]))  # conversion_id
    update_abbyy_job_status(int(sys.argv[2]))  # file_id


if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    from job_scripts import send_to_abby_server, update_abbyy_job_status
    run()