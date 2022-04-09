from docx import Document
from lxml import etree
from zipfile import ZipFile



doc = ZipFile(r"Z:\ACRS\Requests\AAS 510 Temp Shell\Resources for Faculty (Hidden from Student View)\SyllabiComplianceChecklist.docx")
doc_xml = doc.read('word/document.xml')
test = doc.open('word/document.xml')
print(type(test))
tree = etree.parse(doc_xml)
print(tree.tostring(tree, pretty_print=True))

# document = Document(r'C:\Users\913678186\Downloads\companyprofile-problemstatement-3.docx')
#
# print(document.paragraphs)
#




#Headings
#AltText
#DataTables
#Links
#Lists and Columns
