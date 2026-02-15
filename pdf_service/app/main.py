from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse

from app.core.security import get_current_claims
from app.pdf.generator import build_profile_pdf

app = FastAPI(title="PDF Service", version="1.0.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/profile/pdf")
async def profile_pdf(claims: dict = Depends(get_current_claims)):
    pdf_bytes = build_profile_pdf(claims)
    filename = "profile.pdf"
    return StreamingResponse(
        pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
