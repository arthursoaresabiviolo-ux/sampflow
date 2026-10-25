import io
import datetime
from decimal import Decimal
import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def format_date_english(d):
    if not d:
        d = datetime.date.today()
    day = d.day
    if 11 <= (day % 100) <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    month = d.strftime('%B').upper()
    return f"{month} {day}{suffix}, {d.year}"


def generate_invoice_pdf(sample):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    page_w, page_h = A4  # 595.27 x 841.89 points

    # Outer margins: 38 pt
    margin = 38
    x0, y0 = margin, margin
    x1, y1 = page_w - margin, page_h - margin

    # Outer rectangle border
    c.setLineWidth(1.8)
    c.rect(x0, y0, x1 - x0, y1 - y0)

    # 1. Top Header Box
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(page_w / 2, y1 - 25, 'COOP. CAFEIC. E AGROP. - COCAPEC')

    c.setFont('Helvetica', 9)
    c.drawCentredString(page_w / 2, y1 - 52, 'AV. WILSON SABIO DE MELLO, NRO.:3100, DISTRITO INDUSTRIAL')
    c.drawCentredString(page_w / 2, y1 - 72, 'CEP: 14406-052, FRANCA - SP - TEL.: (16) 3711-6200')
    c.drawCentredString(page_w / 2, y1 - 98, 'CNPJ: 54.772.017/0001-96')

    # Divider 1
    y_div1 = y1 - 116
    c.setLineWidth(1.5)
    c.line(x0, y_div1, x1, y_div1)

    # 2. Commercial Invoice & Date
    invoice_number = (sample.contract_ref or '').strip()
    if not invoice_number:
        invoice_year = sample.shipping_date.year if sample.shipping_date else datetime.date.today().year
        invoice_number = f"{sample.id:03d}/{invoice_year} SPLS"

    date_str = format_date_english(sample.shipping_date)

    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(x0 + 10, y_div1 - 22, 'COMMERCIAL INVOICE:')
    c.setFont('Helvetica', 9.5)
    c.drawString(x0 + 155, y_div1 - 22, invoice_number)

    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(x0 + 10, y_div1 - 42, 'DATE:')
    c.setFont('Helvetica', 9.5)
    c.drawString(x0 + 155, y_div1 - 42, date_str)

    # Divider 2
    y_div2 = y_div1 - 65
    c.line(x0, y_div2, x1, y_div2)

    # 3. APPLICANT Section
    # Contains ONLY the information that the user provided for the client
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(x0 + 10, y_div2 - 20, 'APPLICANT:')

    applicant_lines = []
    if sample.client:
        if sample.client.name:
            applicant_lines.extend(textwrap.wrap(sample.client.name.strip().upper(), width=70))
        if sample.client.address:
            applicant_lines.extend(textwrap.wrap(sample.client.address.strip().upper(), width=70))
        if sample.client.country:
            applicant_lines.extend(textwrap.wrap(sample.client.country.strip().upper(), width=70))
        if sample.client.email:
            applicant_lines.append(f"Mail: {sample.client.email.strip()}")
        if sample.client.phone:
            applicant_lines.append(f"Tel: {sample.client.phone.strip()}")

    c.setFont('Helvetica', 9)
    curr_y = y_div2 - 40
    for line in applicant_lines:
        c.drawString(x0 + 10, curr_y, line)
        curr_y -= 15

    # Divider 3 (Table top)
    y_div3 = y_div2 - 155
    c.line(x0, y_div3, x1, y_div3)

    # 4. Table Header
    x_col = x1 - 75
    y_header_bottom = y_div3 - 22
    c.line(x0, y_header_bottom, x1, y_header_bottom)
    c.line(x_col, y_div3, x_col, y_header_bottom)

    c.setFont('Helvetica-Bold', 9.5)
    c.drawCentredString((x0 + x_col) / 2, y_div3 - 15, 'DESCRIPTION')
    c.drawCentredString((x_col + x1) / 2, y_div3 - 15, 'Value USD')

    # Description Row
    # Determine weights
    weight_kg = sample.weight_in_kg
    if weight_kg is None or weight_kg <= 0:
        weight_kg = Decimal('0.500')
    else:
        weight_kg = Decimal(str(weight_kg))

    net_weight_str = f"{weight_kg:.3f}".replace('.', ',')
    gross_weight = weight_kg + Decimal('0.050')
    gross_weight_str = f"{gross_weight:.3f}".replace('.', ',')

    description_text = f"COFFEE WITH {net_weight_str} UNITS OF TYPE: GREEN COFFEE 100% ÁRABICA, REGIÃO DE ALTA MOGIANA."

    y_desc_bottom = y_header_bottom - 42
    c.line(x0, y_desc_bottom, x1, y_desc_bottom)
    c.line(x_col, y_header_bottom, x_col, y_desc_bottom)

    c.setFont('Helvetica', 9)
    c.drawCentredString((x0 + x_col) / 2, y_header_bottom - 24, description_text)
    c.drawCentredString((x_col + x1) / 2, y_header_bottom - 24, '1,00')

    # 5. Airport & Sub-box (TOTAL AMOUNT USD & FCA USD)
    x_sub_left = x1 - 180
    y_box_mid = y_desc_bottom - 20
    y_box_bottom = y_box_mid - 20

    # Sub-box borders
    c.line(x_sub_left, y_desc_bottom, x_sub_left, y_box_bottom)
    c.line(x_col, y_desc_bottom, x_col, y_box_bottom)
    c.line(x_sub_left, y_box_mid, x1, y_box_mid)
    c.line(x_sub_left, y_box_bottom, x1, y_box_bottom)

    c.setFont('Helvetica-Bold', 8.5)
    c.drawCentredString((x_sub_left + x_col) / 2, y_desc_bottom - 14, 'TOTAL AMOUNT USD')
    c.drawCentredString((x_sub_left + x_col) / 2, y_box_mid - 14, 'FCA USD')

    c.setFont('Helvetica', 8.5)
    c.drawCentredString((x_col + x1) / 2, y_desc_bottom - 14, '1,00')
    c.drawCentredString((x_col + x1) / 2, y_box_mid - 14, '1,00')

    # Airport Info
    discharge = 'N/A'
    if sample.client and sample.client.country:
        discharge = sample.client.country.strip().upper()

    c.setFont('Helvetica-Bold', 9)
    c.drawString(x0 + 10, y_desc_bottom - 18, 'AIRPORT OF LOADING:')
    c.setFont('Helvetica', 9)
    c.drawString(x0 + 155, y_desc_bottom - 18, 'VIRACOPOS, BRAZIL')

    c.setFont('Helvetica-Bold', 9)
    c.drawString(x0 + 10, y_desc_bottom - 38, 'AIRPORT OF DISCHARGE:')
    c.setFont('Helvetica', 9)
    c.drawString(x0 + 155, y_desc_bottom - 38, discharge)

    # 6. Samples without commercial value & Weights
    c.setFont('Helvetica-Bold', 9)
    c.drawString(x0 + 10, y_box_bottom - 42, 'SAMPLES WITHOUT COMMERCIAL VALUE')

    x_val = x1 - 25
    x_colon = x1 - 65

    c.setFont('Helvetica-Bold', 9)
    c.drawRightString(x_colon, y_box_bottom - 22, 'TOTAL GROSS WEIGHT:')
    c.setFont('Helvetica', 9)
    c.drawRightString(x_val, y_box_bottom - 22, gross_weight_str)

    c.setFont('Helvetica-Bold', 9)
    c.drawRightString(x_colon, y_box_bottom - 42, 'TOTAL NET WEIGHT :')
    c.setFont('Helvetica', 9)
    c.drawRightString(x_val, y_box_bottom - 42, net_weight_str)

    c.setFont('Helvetica-Bold', 9)
    c.drawRightString(x_colon, y_box_bottom - 62, 'TOTAL VOLUMES:')
    c.setFont('Helvetica', 9)
    c.drawRightString(x_val, y_box_bottom - 62, '1')

    # 7. Bottom Signature Line & Company Name
    y_sig = y0 + 80
    c.setLineWidth(1)
    c.line(page_w / 2 - 140, y_sig, page_w / 2 + 140, y_sig)

    c.setFont('Helvetica-Bold', 9.5)
    c.drawCentredString(page_w / 2, y_sig - 16, 'COOP. CAFEIC. E AGROP. - COCAPEC')

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
