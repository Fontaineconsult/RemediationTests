import sys, os
from pathlib import Path

def run():
    repair = PdfRepair((sys.argv[1]))
    getattr(repair, sys.argv[2])()
    input()

if __name__ == '__main__':
    p = Path(__file__).parents[2]
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), p)))
    from pdfRepair import PdfRepair
    run()
