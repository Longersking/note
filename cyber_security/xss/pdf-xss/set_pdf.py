from PyPDF2 import PdfReader,PdfWriter

new_PDF = PdfWriter()
# 写入JavaScript代码
new_PDF.add_js("app.alert('yvoone');")
f = open("somethins.pdf","wb")
new_PDF.write(f)
f.close() 
