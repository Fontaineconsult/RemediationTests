import os, sys

def run():
    replace_old_file_with_abbyy_file(int(sys.argv[1]), int(sys.argv[2]))  # abbyyJobId fileLocation

if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
    from job_scripts import replace_old_file_with_abbyy_file
    run()