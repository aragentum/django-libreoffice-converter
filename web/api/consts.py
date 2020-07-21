class ConverterClass:
    TEXT = "text"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    GRAPHIC = "graphic"


# MIME TYPES

TEXT_MIME_TYPES = {
    "application/pdf": ["pdf"],
    "application/msword": ["doc"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ["docx"],
    "application/vnd.oasis.opendocument.text": ["odt"],
    "text/plain": ["txt"],
    "text/html": ["html", "htm"],
    "application/rtf": ["rtf"],
}

SPREADSHEET_MIME_TYPES = {
    "application/vnd.ms-excel": ["xls"],
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ["xlsx"],
    "application/vnd.oasis.opendocument.spreadsheet": ["ods"],
    "text/csv": ["csv"],
}

PRESENTATION_MIME_TYPES = {
    "application/pdf": ["pdf"],
    "application/vnd.ms-powerpoint": ["ppt"],
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ["pptx"],
    "application/vnd.oasis.opendocument.presentation": ["odp"],
}

GRAPHIC_MIME_TYPES = {
    "image/bmp": ["bmp"],
    "image/jpeg": ["jpeg", "jpg"],
    "image/png": ["png"],
    "image/svg+xml": ["svg"],
}
