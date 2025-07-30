from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from .parser import parse_code, validate_code

app = FastAPI(title="ESP Long Coding Decoder", version="1.0.0")
templates = Jinja2Templates(directory="app/templates")


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    return "ok"


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "result": None, "error": None}
    )


@app.post("/decode", response_class=HTMLResponse)
async def decode_form(request: Request, code: str = Form(...)):
    try:
        data = parse_code(code)
        # Берём HTML-версию
        html_text = data["html"]
        return templates.TemplateResponse(
            "index.html", {"request": request, "result": html_text, "error": None}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", {"request": request, "result": None, "error": str(e)}
        )


@app.post("/api/decode")
async def decode_api(payload: dict):
    code = payload.get("code", "")
    try:
        validate_code(code)
        data = parse_code(code)
        return JSONResponse({"ok": True, "output": data})
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
