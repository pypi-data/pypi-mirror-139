import os
import subprocess
from docx2pdf import convert



def _PrintDocument(filename, printer):

    inputFile = filename
    filename_pdf = filename.split(".")
    filename_pdf = filename_pdf[0]
    filename_pdf += ".pdf"

    outputFile = filename_pdf

    convert(inputFile, outputFile)

    print_cmd = 'lpr -P %s %s'
    os.system(print_cmd % (stampante[1], filename))


stampante = subprocess.getoutput("lpstat -d").split(": ")
_PrintDocument("testo.docx",stampante[1])