import os
from fpdf import FPDF
from docx2pdf import convert
from PIL import Image
from reportlab.pdfgen import canvas
import comtypes.client

class converter:
    def txt_to_pdf(self, path, file_name, file_extension):
        og_path = os.path.join(path, f"{file_name}{file_extension}")
        converted = os.path.join(path, f"{file_name}.pdf")
        pdf = FPDF()  
        pdf.add_page()
        pdf.set_font("Arial", size = 15)
        f = open(og_path, "r")
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'L')
        pdf.output(converted)

    def docx_to_pdf(self, path, file_name, file_extension):
        og_path = os.path.join(path, f"{file_name}{file_extension}")
        converted = os.path.join(path, f"{file_name}.pdf")
        convert(og_path, converted)

    def image_to_pdf(self, folder, file_name, file_extension):
        og_path = os.path.join(folder, file_name + file_extension)
        converted = os.path.join(folder, file_name + ".pdf")
        image = Image.open(og_path)
        image.save(converted, "PDF", resolution=100.0)
        image.close()

    def doc_to_pdf(self, path, file_name, file_extension):
        og_path = os.path.join(path, file_name + file_extension)
        converted = os.path.join(path, file_name + ".pdf")
        word = comtypes.client.CreateObject("Word.Application")
        doc = word.Documents.Open(og_path)
        doc.SaveAs(converted, FileFormat=17)
        doc.Close()
        word.Quit()