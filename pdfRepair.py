from pikepdf import Pdf, Dictionary, Array, String, Object, Name, PdfError, OutlineItem, NameTree
import pikepdf
from pdfValidation import verify_headings
import re
import zlib

headings_map = {
    pikepdf.Name("/H1"): 1,
    pikepdf.Name("/H2"): 2,
    pikepdf.Name("/H3"): 3,
    pikepdf.Name("/H4"): 4,
    pikepdf.Name("/H5"): 5,
    pikepdf.Name("/H6"): 6,
    "/H1": 1,
    "/H2": 2,
    "/H3": 3,
    "/H4": 4,
    "/H5": 5,
    "/H6": 6,


}



def _get_page_number_of_page(page_obj: Object, document: Pdf):

    count = 0

    for each in list(document.Root.Pages.Kids):

        if each.get("/Type") == "/Pages":
            for page in each.get("/Kids"):
                count += 1
                if page == page_obj:
                    return count

        else:
            count += 1
            if each == page_obj:
                return count



def add_bookmarks_from_headings(Pikepdf):

    root = Pikepdf.Root.get("/StructTreeRoot")
    parent_tree = root.get("/ParentTree")
    page = Pikepdf.pages[0]
    print(repr(page))
    unicode = page.get("/Resources").get("/Font").get("/TT0").get("/ToUnicode").read_bytes()
    print(unicode.decode('Latin1'))

    def check_bookmark(node):
        if node.get("/S") in ["/H1", "/H2", "/H3", "/H4", "/H5", "/H6"]:

            if node.get("/S") == "/H1":
                print(repr(node.get('/Pg')))
            mcid = node.get("/K")
            page_bytes = node.get('/Pg').get("/Contents").read_bytes()

            # print("GGGG1", zlib.decompress(page_bytes))
            try:
                print("GGGG", repr(node.get('/Pg').get("/Resources").get("/Font").get("/TT0").get("/ToUnicode").read_bytes().decode('utf-8')))
            except:
                pass
            # print(page_bytes)
            # Get Bookmark Position
            raw_location_re = f"<</MCID {mcid} >>BDC\s(.*?)(Tm|Td)"
            mcid_re = re.compile(raw_location_re, flags=re.DOTALL)
            location_string = re.search(mcid_re, page_bytes.decode('utf-8'))
            if location_string is not None:
                x = location_string.group().split()[-3]
                y = location_string.group().split()[-2]
                raw_title_re = f"<</MCID {mcid} >>BDC(.*?)EMC"
                title_re = re.compile(raw_title_re, flags=re.DOTALL)
                title_string = re.search(title_re, page_bytes.decode('utf-8'))
                in_paren = False
                output = []
                for position, char in enumerate(title_string.group()):
                    if char == "(":
                        in_paren = True
                        continue
                    if char == ")":
                        in_paren = False
                        continue
                    if in_paren is True:
                        output.append(char)
                bookmark_title = "".join(output)
                page_number = _get_page_number_of_page(node.get("/Pg"), Pikepdf)

                with Pikepdf.open_outline() as outline:
                    oi = OutlineItem(bookmark_title, page_number - 1, "XYZ", left=int(float(x)),
                                     top=int(float(y)))
                    outline.root.append(oi)

            else:
                print("Failed to find bookmark data")

    def recurse_k_nodes(node):

        if isinstance(node, Dictionary):
            if "/K" in node.keys():
                if "/S" in node.keys():
                    check_bookmark(node)
                recurse_k_nodes(node.get('/K'))
        if isinstance(node, Array):

            for each in node:
                if isinstance(each, Dictionary):
                    if "/K" in each.keys():
                        recurse_k_nodes(each.get("/K"))

                    if "/S" in each.keys():
                        check_bookmark(each)

                if isinstance(each, Array):
                    recurse_k_nodes(each)

    # if Pikepdf.Root.get("/AcroForm"):
    #     if "/PDFDocEncoding" in Pikepdf.Root.AcroForm.DR.Encoding.keys():
    #         if isinstance(Pikepdf.Root.Pages.Kids, Array):
    #             print("Adding Bookmarks")
    #             recurse_k_nodes(parent_tree.get("/Nums"))
    #         else:
    #             print("Page stored as Dict")
    #     else:
    #         print("Encoding Not Supported for Bookmarks")
    # else:
    #     try:
    #         recurse_k_nodes(parent_tree.get("/Nums"))
    #     except AttributeError:
    #         recurse_k_nodes(parent_tree.get("/Kids").get("/Nums"))



def remove_all_headings(document):

    root = document.Root.get("/StructTreeRoot")
    # print(type(root))
    # verify_headings(document)
    first_check = False
    new_stream = []

    page = document.pages[0]
    roleMap = root.get("/RoleMap")
    print(repr(roleMap))
    # print(page.Contents.read_bytes())
    # print(pikepdf.parse_content_stream(page))


    for operands, operator, in pikepdf.parse_content_stream(page):
        # print(f"operator {operands}, {operator}")
            # print("OP", operands, operator)

        for count, each in enumerate(operands):
            if isinstance(each, Name):
                if each in headings_map:
                    # print(each, count)
                    # print(operands)
                    operands.pop(count)
                    operands.insert(count, pikepdf.Name("/P"))
        new_stream.append((operands, operator))


    new_content = pikepdf.unparse_content_stream(new_stream)
    page.Contents = document.make_stream(new_content)

    def check_dictionary(node):

        if "/S" in node.keys():

            if node.get("/S") in headings_map.keys():
                # print(node.get("/P").keys(), type(node))
                # print(repr(node.get("/K")))
                parent = node.get("/P")
                child = parent.get("/K")
                if isinstance(child, Array):
                    for each in child:
                        if each.get("/S") in headings_map:
                            pass
                            # print("SSEEEINK", repr(each.get("/K")))
                            each["/S"] = Name('/P')


                        # print(repr(each.get("/S")))
                if isinstance(child, Dictionary):
                    if child.get("/S") in headings_map:
                        pass
                        child["/S"] = Name('/P')
                        # print("SSEEEINK", repr(child.get("/K")))

    def recurse_k_nodes(node):

        if isinstance(node, Dictionary):
            if "/K" in node.keys():

                check_dictionary(node)
                recurse_k_nodes(node.get('/K'))
        if isinstance(node, Array):
            for each in node:
                if isinstance(each, Dictionary):
                    check_dictionary(each)
                    if "/K" in each.keys():
                        recurse_k_nodes(each.get('/K'))
                if isinstance(each, Array):
                    recurse_k_nodes(each)

    recurse_k_nodes(root)


def normalize_headings(document):
    verify_headings(document)
    root = document.Root.get("/StructTreeRoot")


    headings = []

    def find_group(start_index):
        pass

    def recurse_k_nodes(node):

        if isinstance(node, Dictionary):
            if "/K" in node.keys():
                recurse_k_nodes(node.get('/K'))


        if isinstance(node, Array):
            for each in node:
                if isinstance(each, Dictionary):
                    if "/K" in each.keys():
                        recurse_k_nodes(each.get("/K"))
                    if "/S" in each.keys():

                        if each.get("/S") in headings_map.keys():

                            if len(headings) == 0:
                                if each.get("/S") != "/H1":
                                    each["/S"] = Name("/H1")
                                    headings.append(headings_map[each.get("/S")])

                            else:

                                if len(headings) == 1:
                                    print(headings)
                                    if headings_map[each.get("/S")] - headings[0] > 1:
                                        each["/S"] = headings[0] + 1
                                        headings.append(each["/S"])
                                else:
                                    if headings_map[each.get("/S")] - headings[-1] > 1:
                                        each["/S"] = headings[-1] + 1
                                        headings.append(each["/S"])

                if isinstance(each, Array):
                    recurse_k_nodes(each)


    recurse_k_nodes(root)
    print(headings)






class PdfRepair:

    def __init__(self, location:str):
        self.location = location
        self.file = None

    def _open(self):
        self.file = Pdf.open(self.location, allow_overwriting_input=True)
        print(self.file.open_metadata())

    def _finalize(self):
        self.file.save()
        self.file.close()

    def remove_headings(self):
        self._open()
        remove_all_headings(self.file)
        self._finalize()

    def add_bookmarks_from_headings(self):
        self._open()
        add_bookmarks_from_headings(self.file)
        self._finalize()

    def normalize_headings(self):
        self._open()
        normalize_headings(self.file)
        self._finalize()

#
#
#
#
test = PdfRepair(r"Z:\ACRS\project_files\897458a53576aeca31c4d4ad4ca9d7d7a6903176a6311024f0866db750f42dfe\active\2007_Ari Cushner.pdf")
getattr(test, "add_bookmarks_from_headings")()
#
#
