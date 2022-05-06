import sys, os
from pathlib import Path

def run():
    pdf_accessibility_check(int(sys.argv[1]), sys.argv[2])
    input()



if __name__ == '__main__':
    p = Path(__file__).parents[2]
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), p)))
    from job_scripts import pdf_accessibility_check
    run()
