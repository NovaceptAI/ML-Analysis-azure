# from pdfminer.pdfpage import PDFPage
# # from tabula import read_pdf
#
#
# def get_pdf_searchable_pages(fname):
#     """
#
#     :param fname: path of the file from content root of absolute file
#     :return: Boolean value indication if pdf is non machine readable
#     """
#     searchable_pages = []
#     non_searchable_pages = []
#     page_num = 0
#     with open("/home/novneetpatnaik/Projects/ML_OCR/tmp/" + fname, 'rb') as infile:
#         # check pages in file and check
#         # if font is detectable. If yes
#         # it is machine readable
#         for page in PDFPage.get_pages(infile):
#             page_num += 1
#             if 'Font' in page.resources.keys():
#                 searchable_pages.append(page_num)
#             else:
#                 non_searchable_pages.append(page_num)
#     # code returns true of machine readable else it returns false
#     if page_num > 0:
#         if len(non_searchable_pages) == page_num:
#             print(f"Document '{fname}' has {page_num} page(s). "
#                   f"Complete document is non-searchable")
#             return False
#         elif len(searchable_pages) == page_num:
#             print(f"Document '{fname}' has {page_num} page(s). "
#                   f"Complete document is searchable")
#             return True
#         elif len(non_searchable_pages) == 0:
#             print(f"Document '{fname}' has {page_num} page(s). "
#                   f"Complete document is searchable")
#             return True
#         else:
#             print(f"searchable_pages : {searchable_pages}")
#             print(f"non_searchable_pages : {non_searchable_pages}")
#             return False
#     else:
#         print(f"Not a valid document")
#         return False