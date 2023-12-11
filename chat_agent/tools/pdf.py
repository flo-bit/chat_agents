from pypdf import PdfReader


async def get_pdf_text(agent, pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return "PDF {pdf_path} CONTENT START: \n" + text + "\nPDF {pdf_path} CONTENT END"

tool_get_pdf_text = {
    "info": {
        "type": "function",
        "function": {
            "name": "get_pdf_text",
            "description": "Returns the text content of a pdf file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the pdf file, relative to the current working directory",
                    }
                },
                "required": ["path"],
            },
        }
    },
    "function": get_pdf_text
}
