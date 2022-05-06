import sys, os
from pathlib import Path

def run():
    finalize_pdf_file_conversion(int(sys.argv[1]))


if __name__ == '__main__':
    p = Path(__file__).parents[2]
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), p)))
    from job_scripts import finalize_pdf_file_conversion
    run()
