import os, sys
from pathlib import Path


def run():
    print("FIRST", sys.argv[2])
    replace_old_file_with_abbyy_file(sys.argv[1], sys.argv[2])  # abbyyJobId fileLocation
    input()

if __name__ == '__main__':
    p = Path(__file__).parents[2]
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), p)))
    from job_scripts import replace_old_file_with_abbyy_file
    run()