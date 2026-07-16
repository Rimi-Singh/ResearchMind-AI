from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.auth import router as auth_router
from api.upload import router as upload_router
from api.chat import router as chat_router
from api.history import router as history_router
from api.files import router as files_router
from fastapi.responses import FileResponse
import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI(title="ResearchMind.ai")

@app.get("/download-source")
def download_source(path: str):

    # Convert to absolute path
    requested_path = os.path.abspath(path)

    # Folder that contains uploaded PDFs
    pdf_folder = os.path.abspath("data/pdfs")

    # Security check
    if not requested_path.startswith(pdf_folder):

        raise HTTPException(
            status_code=403,
            detail="Access denied."
        )

    if not os.path.exists(requested_path):

        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return FileResponse(
        requested_path,
        filename=os.path.basename(requested_path),
        media_type="application/pdf"
    )




app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


@app.get("/ingestion", response_class=HTMLResponse)
async def ingestion_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="ingestion.html",
        context={}
    )


@app.get("/health")
async def health():

    return {
        "status": "running",
        "application": "ResearchMind.ai"
    }



app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(history_router)
app.include_router(files_router)