import os

from fastapi import APIRouter

from config.settings import PDF_FOLDER

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/pdfs")
async def get_uploaded_pdfs():
    """
    Return all uploaded PDFs.
    """

    os.makedirs(PDF_FOLDER, exist_ok=True)

    pdfs = []

    for filename in sorted(os.listdir(PDF_FOLDER)):

        if filename.lower().endswith(".pdf"):

            path = os.path.join(PDF_FOLDER, filename)

            pdfs.append(
                {
                    "name": filename,
                    "size": os.path.getsize(path)
                }
            )

    return pdfs