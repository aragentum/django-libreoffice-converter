from os import path

DATA_DIR = path.join(path.dirname(path.abspath(__file__)), "data")
DOCX_FILE = path.join(DATA_DIR, "docx_01.docx")
IMAGE_FILE = path.join(DATA_DIR, "image_01.png")

INVALID_IMAGE_FILE = path.join(DATA_DIR, "invalid_image_01.docx")
INVALID_DOCX_FILE = path.join(DATA_DIR, "invalid_docx_01.png")

BROKEN_DOCX_FILE = path.join(DATA_DIR, "broken_docx_01.docx")
