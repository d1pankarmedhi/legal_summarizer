from PyPDF2 import PdfReader
import pytesseract
import pypdfium2 as pdfium
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_from_pdf(file: bytes) -> str:
    data = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        data += page.extract_text()
    return data



def extract_from_scanned_pdf(file):
    text = ""
    pdf = pdfium.PdfDocument(file)
    n_pages = len(pdf)
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        bitmap = page.render(
            scale=1,
            rotation=0,
        )
        img = bitmap.to_pil()
        text += pytesseract.image_to_string(img, config=r"--oem 3 --psm 6")
    return text


def classify_text(text: str):
    if text.isupper():
        return "heading"
    else:
        return "body"



def tag_documents(data: str) -> list:
    tagged_documents = []
    current_heading = None
    current_paragraph = ""

    for line in data.split("\n"):
        line = line.strip()

        if not line:
            continue
        text_class = classify_text(line)

        if text_class == "heading":
            if current_heading is not None:
                tagged_documents.append(
                    {"heading": current_heading, "body": current_paragraph.strip()}
                )

            current_heading = line
            current_paragraph = ""
        else:
            current_paragraph += " " + line

    if current_heading is not None:
        tagged_documents.append(
            {"heading": current_heading, "body": current_paragraph.strip()}
        )

    # split body into documents
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n\n", "\n\n", "\n", " "],
        chunk_size=1000,
        chunk_overlap=30,
    )
    for data in tagged_documents:
        documents = text_splitter.create_documents([data["body"]])
        data["documents"] = documents

    return tagged_documents