from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse

from services.pdf_service import PDFService

router = APIRouter()


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    """
    Upload a research paper and update the vector database.
    """

    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:

        save_path = PDFService.save_pdf(file)

        success = PDFService.update_vectorstore(save_path)

        if not success:

            raise HTTPException(
                status_code=500,
                detail="Failed to update the vector database."
            )

        return RedirectResponse(
            url="/ingestion",
            status_code=303
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )