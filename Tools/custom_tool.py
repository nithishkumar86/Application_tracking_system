import fitz
from crewai.tools import tool
import re

@tool("pdf_extractor")
def pdf_extractor()->str:
    """
    custom tool for extracting the content and text from the .pdf files or .docx files from the 
    given path

    ARGS (path = "resume.pdf"):
    Returns : "context"
    """
    path = r"E:\CREWAI_APPLICATION_TRACKING_SYSTEM\Resume\resume.pdf"

    text_blocks = []
    with fitz.open(path) as doc:
        for page in doc:
            text = page.get_text("text").strip()
            if text:
                text_blocks.append(text)


    paragraphs = []
    for page_text in text_blocks:
        # Split on double line breaks or long newlines
        chunks = re.split(r'\n\s*\n', page_text)
        for chunk in chunks:
            clean = chunk.strip()
            paragraphs.append(clean)
    
    result = "\n\n".join(paragraphs)
    return result



