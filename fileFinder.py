from pathlib import Path
import glob
from openpyxl import Workbook



files = glob.glob("Z:\Students\Phil Ho" + '/**/*[.pdf|.docx|.doc]', recursive=True)


print(files)


