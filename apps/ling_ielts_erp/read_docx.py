import zipfile
import xml.etree.ElementTree as ET
import os

docx_path = r"d:\my-projects\httt\cs-httt\A1_Phan_tich_nghiep_vu_Ling_IELTS (2).docx"
out_path = r"d:\my-projects\httt\cs-httt\apps\ling_ielts_erp\docx_text.txt"

def read_docx(path, out_file):
    if not os.path.exists(path):
        print("File not found:", path)
        return
    with zipfile.ZipFile(path) as z:
        xml_content = z.read("word/document.xml")
        tree = ET.fromstring(xml_content)
        
        paragraphs = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            if texts:
                paragraphs.append("".join(texts))
        
        with open(out_file, "w", encoding="utf-8") as f:
            f.write("\n".join(paragraphs))
        print("Successfully wrote docx content to", out_file)

if __name__ == "__main__":
    read_docx(docx_path, out_path)
