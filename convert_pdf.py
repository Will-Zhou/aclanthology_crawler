import sys
import importlib
from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import os
import re

importlib.reload(sys)


def parse(path):
    fp = open(path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        fw = open('1.txt', 'w', encoding="utf-8")
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    results = x.get_text()
                    results = results.replace("-\n", "")
                    results = results.replace("\n", "")
                    print(results + "\n\n")
                    fw.write(results + '\n')


def check_file(dic):
    counter = 0
    dics = os.listdir(dic)
    for d in dics:
        if os.path.isdir(d):
            files = os.listdir(d)
            for f in files:
                if re.findall(".pdf", f):
                    fp = open(d + "/" + f, 'rb')
                    praser = PDFParser(fp)
                    doc = PDFDocument()
                    praser.set_document(doc)
                    try:
                        doc.set_parser(praser)
                    except:
                        fp.close()
                        os.remove(d + "/" + f)
                        print(d + "/" + f + " removed")
                        counter += 1

    print(str(counter) + " files removed.")


if __name__ == '__main__':
    # parse("acl-2002/P02-1000.pdf")
    # os.remove("1.txt")
    check_file("E:/PyProjects/aclanthology")
    print("The End.")
