from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFDocument, PDFParser

import re


def get_abstract(path):
    abstract = ""
    fr = open(path, mode="rb")
    praser = PDFParser(fr)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()

    flag = False

    if doc.is_extractable:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    results = x.get_text()
                    if re.findall("abstract", results.lower()):
                        flag = True
                    if flag and len(results) > 500:
                        abstract = results.replace("-\n", "")
                        abstract = abstract.replace("\n", "")
                        return abstract
    return abstract


# problems not each paper using conclusion and may be long
def get_conclusion(path):
    conclusion = ""
    fr = open(path, mode="rb")
    praser = PDFParser(fr)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()

    flag = False

    if doc.is_extractable:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    results = x.get_text()
                    if re.findall("conclusion", results.lower()):
                        flag = True
                    if flag and len(results) > 500:
                        conclusion = results.replace("-\n", "")
                        conclusion = conclusion.replace("\n", "")
                        return conclusion
    return conclusion


if __name__ == "__main__":
    print(get_abstract("acl-2018/P18-1024.pdf"))
    print("The End.")
