from pdfminer import high_level
import pdfminer

from pikepdf import Pdf, Page, PdfImage, OutlineItem



def page_contains_text(page):
    if page.groups is None:
        return False
    for each in page.groups:
        if isinstance(each, pdfminer.layout.LTTextGroupLRTB):
            return True
    return False


def image_over_text(page):

    for item in list(page):

        if isinstance(item, pdfminer.layout.LTFigure):
            variance = (item.x1 * item.y1) / (page.x1 * page.y1)
            if 0.9 < variance < 1.1:  # Check to see if the size of the text image is the same as the page
                return True
            else:
                continue
        return False


def check_status(document_location):
    pages = list(high_level.extract_pages(document_location))
    to_return = []
    for page in pages:

        image = image_over_text(page)
        text = page_contains_text(page)
        to_return.append((image,text))
    return to_return


def pdf_status(document_location):

    # True True = Image of text over text
    # False True = Text Only
    # True False = Only Image of Text
    # False False = No image of text and no page text

    t1 = 0
    t2 = 0
    page_stats = check_status(document_location)

    for each in page_stats:
        if each[0]:
            t1 += 1
        if each[1]:
            t2 += 1
    print(t1, t2)
    if t1 > 0 and t2 > 0:
        return 0  # Image of text over text
    if t1 == 0 and t2 != 0:
        return 1  # Text Only
    if t1 > 0 and t2 == 0:
        return 2  # Only Image of Text
    if t1 == 0 and t2 == 0:
        return 3  # No image of text and no page text




def test(document_location):

    pdf = Pdf.open(document_location)


    # print(pdf.pages[0])
    # imgs = pdf.pages[0].images['/Im0']
    #
    # obj = PdfImage(imgs)
    # print(obj.colorspace)
    # print((pdf.pages[0].get("/Resources").get("/Font")))
    # print(dir(pdf.pages[0].Resources.XObject.Im1))
    # print(pdf.pages[0].Resources.XObject.Im1.to_json())

    # print(dir(pdf.Root.get('/StructTreeRoot')))
    #
    # zerk = pdf.Root.get('/StructTreeRoot')
    # print(zerk.read_bytes())
    # print(dir(zerk.ParentTree))
    # print(dir(zerk.ParentTree.items()))
    # print(root[3])

    root1 = pdf.Root.get("/Outlines")
    # print(list(root1))
    # print(list(root1.get("/First").get("/First").get("/SE").get("/K")[0].get("/K")[0]))
    # print(root1.get("/First").get("/First").get("/SE").get("/K")[0].get("/K")[0].get("/Alt"))

    # print(list(root1))
    # print(list(root1["/First"]))
    # print(list(root1["/First"]["/First"]))
    # print(list(root1["/First"]["/First"]["/SE"]))
    print((root1['/First']['/First']['/SE']['/K'][1]['/P']['/K'][0]['/K'][0]['/Pg']['/Resources']['/XObject']['/Im1']['/ID']))


    # print(len(list(root1.get("/First").get("/First").get("/SE").get("/K"))))
    #
    # tst = list(root1.get("/First").get("/First").get("/SE").get("/K"))[0]





    # print(lorp.items)


test(r"Z:\ACRS\project_files\ab780356aac11e379d56431b4f3a5de454e2910ce46d52f0804b21481d7d09de\source\Number Sense -Ed Leadership.pdf")

