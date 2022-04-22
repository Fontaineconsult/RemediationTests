import sys, os


def run():
    deactivate_active_job(int(sys.argv[1]))

if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    from job_scripts import deactivate_active_job
    run()