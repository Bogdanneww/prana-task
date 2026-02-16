from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def build_profile_pdf(claims: dict) -> BytesIO:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 800, "User Profile")

    c.setFont("Helvetica", 12)
    lines = [
        f"Name: {claims.get('name')}",
        f"Surname: {claims.get('surname')}",
        f"Email: {claims.get('email')}",
        f"Date of birth: {claims.get('date_of_birth')}",
    ]

    y = 760
    for line in lines:
        c.drawString(72, y, line)
        y -= 20

    c.showPage()
    c.save()

    buf.seek(0)
    return buf
