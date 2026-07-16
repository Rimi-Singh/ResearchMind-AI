from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from config.settings import USERNAME, PASSWORD

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...)
):

    if username == USERNAME and password == PASSWORD:

        return RedirectResponse(
            url="/dashboard",
            status_code=302
        )

    return HTMLResponse(
        """
        <h2>Invalid Username or Password</h2>
        <a href="/">Back to Login</a>
        """
    )