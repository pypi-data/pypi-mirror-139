import PrintDocx
import subprocess

stampante = subprocess.getoutput("lpstat -d").split(": ")
PrintDocx._PrintDocument("testo.docx",stampante[1])