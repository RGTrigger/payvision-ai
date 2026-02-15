from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
from analytics.metrics import advanced_metrics
from analytics.anomaly import explain_anomalies

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_pdf_report():
    path = OUTPUT_DIR / "report.pdf"

    doc = SimpleDocTemplate(str(path))
    styles = getSampleStyleSheet()

    metrics = advanced_metrics()

    content = [
        Paragraph("Digital Payment Forecast Report", styles['Heading1']),
        Spacer(1, 20),
    ]

    for k, v in metrics.items():
        content.append(Paragraph(f"<b>{k}</b>: {v}", styles['Normal']))
        content.append(Spacer(1, 10))

    # ✅ Fraud Insight Section
    content.append(Spacer(1, 20))
    content.append(Paragraph("Risk & Fraud Insight", styles['Heading2']))
    content.append(Spacer(1, 10))
    content.append(Paragraph(explain_anomalies(), styles['Normal']))

    doc.build(content)

    return path
