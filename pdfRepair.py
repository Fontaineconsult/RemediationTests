from pikepdf import Pdf, Dictionary, Array, String, Object, Name, PdfError, OutlineItem
import pikepdf
from pdfValidation import verify_headings
import re


headings_map = {
    pikepdf.Name("/H1"): 1,
    pikepdf.Name("/H2"): 2,
    pikepdf.Name("/H3"): 3,
    pikepdf.Name("/H4"): 4,
    pikepdf.Name("/H5"): 5,
    pikepdf.Name("/H6"): 6,

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

    def recurse_k_nodes(node):

        if isinstance(node, Dictionary):
            if "/K" in node.keys():

                recurse_k_nodes(node.get('/K'))
        if isinstance(node, Array):

            for each in node:

                if isinstance(each, Dictionary):

                    if "/K" in each.keys():
                        print(each.get('/Pg'))

                        recurse_k_nodes(each.get("/K"))

                    if "/S" in each.keys():

                        if each.get("/S") in ["/H1", "/H2", "/H3", "/H4", "/H5", "/H6"]:

                            # if each.get("/S") == "/H1":
                            #     print(repr(each.get('/Pg')))

                            mcid = each.get("/K")

                            page_bytes = each.get('/Pg').get("/Contents").read_bytes()
                            print(page_bytes)
                            # print(page_bytes)
                            # Get Bookmark Position
                            raw_location_re = f"<</MCID {mcid} >>BDC\s(.*?)(Tm|Td)"
                            mcid_re = re.compile(raw_location_re, flags=re.DOTALL)
                            location_string = re.search(mcid_re, page_bytes.decode('utf-8'))
                            if location_string is not None:
                                x = location_string.group().split()[-3]
                                y = location_string.group().split()[-2]
                            else:
                                print("Failed to find bookmark data")
                                continue

                            # Get Bookmark Title
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
                            page_number = _get_page_number_of_page(each.get("/Pg"), Pikepdf)

                            with Pikepdf.open_outline() as outline:
                                oi = OutlineItem(bookmark_title, page_number - 1, "XYZ", left=int(float(x)),
                                                 top=int(float(y)))
                                outline.root.append(oi)

                if isinstance(each, Array):
                    recurse_k_nodes(each)
    print(repr(parent_tree))
    if Pikepdf.Root.get("/AcroForm"):
        if "/PDFDocEncoding" in Pikepdf.Root.AcroForm.DR.Encoding.keys():
            if isinstance(Pikepdf.Root.Pages.Kids, Array):
                print("Adding Bookmarks")
                recurse_k_nodes(parent_tree.get("/Nums"))
            else:
                print("Page stored as Dict")
        else:
            print("Encoding Not Supported for Bookmarks")
    else:
        recurse_k_nodes(parent_tree.get("/Kids").get("/Nums"))




def remove_all_headings(document):

    root = document.Root.get("/StructTreeRoot")

    verify_headings(document)
    first_check = False

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
                        print(each.get("/S"))
                        if each.get("/S") in headings_map.keys():
                            print(each.get("/S"))

                            each["/S"] = Name("/Span")

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





def repair_pdf(location):


        Pikepdf = Pdf.open(location, allow_overwriting_input=True)
        # remove_all_headings(Pikepdf)
        add_bookmarks_from_headings(Pikepdf)
        verify_headings(Pikepdf)
        # Pikepdf.save()
        Pikepdf.close()




repair_pdf(r"Z:\ACRS\project_files\876bdcbb33fc465b2a9c0bce5a82391bb42ffe2a5877743737eeab2c238a4ba3\active\2006_Daniel Frontino Elash.pdf")