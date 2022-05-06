from pikepdf import Pdf, Dictionary, Array, String, Object, Name, PdfError, OutlineItem
import pikepdf
from pdfValidation import verify_headings

headings_map = {
    pikepdf.Name("/H1"): 1,
    pikepdf.Name("/H2"): 2,
    pikepdf.Name("/H3"): 3,
    pikepdf.Name("/H4"): 4,
    pikepdf.Name("/H5"): 5,
    pikepdf.Name("/H6"): 6,

}


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
                            if first_check:
                                each["/S"] = Name("/P")

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


        Pikepdf = Pdf.open(location)
        # remove_all_headings(Pikepdf)
        Pikepdf.save(r"C:\Users\913678186\IdeaProjects\RemediationTests\testpdf\test.pdf")
        Pikepdf.close()




repair_pdf(r"Z:\ACRS\project_files\2137bf5ca96d9fdffd0b319a9febf1405b1e2c0f89f9ea8b0225729ae5895442\active\2005_Michael T. Caires.pdf")