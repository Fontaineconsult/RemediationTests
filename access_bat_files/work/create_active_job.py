
import sys, os
from pathlib import Path

def run():
    start_pdf_file_conversion(int(sys.argv[1]))
    pdf_accessibility_check(int(sys.argv[1]), sys.argv[2])


if __name__ == '__main__':
    p = Path(__file__).parents[2]
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), p)))
    from job_scripts import start_pdf_file_conversion, pdf_accessibility_check
    run()