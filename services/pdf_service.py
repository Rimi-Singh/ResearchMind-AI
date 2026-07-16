import os
import shutil

from fastapi import UploadFile

from config.settings import PDF_FOLDER
from scripts.ingest import ingest_pdf
from scripts.logger import logger
from services.rag_service import rag_service


class PDFService:

    @staticmethod
    def save_pdf(file: UploadFile):

        os.makedirs(
            PDF_FOLDER,
            exist_ok=True
        )

        save_path = os.path.join(
            PDF_FOLDER,
            file.filename
        )

        with open(save_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        logger.info(f"PDF Saved : {file.filename}")

        return save_path

    @staticmethod
    def update_vectorstore(pdf_path: str):

        logger.info("=" * 80)
        logger.info("Updating Vector Store")
        logger.info("=" * 80)

        try:

            ingest_pdf(pdf_path)

            rag_service.reload()

            logger.info("Vector Store Updated Successfully")

            return True

        except Exception as e:

            logger.exception(e)

            return False