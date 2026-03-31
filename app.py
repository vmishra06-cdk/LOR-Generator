from flask import Flask, request, send_file, render_template_string
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import io
from datetime import datetime
import os

app = Flask(__name__)

# --- Beautiful UI Template ---
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LOR Generator | Bit By Bit</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --bg: #f8fafc;
            --text: #1e293b;
            --card-bg: #ffffff;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
            background-size: 30px 30px;
            color: var(--text);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }

        .container {
            background: var(--card-bg);
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 420px;
            border: 1px solid #e2e8f0;
        }

        h2 {
            margin-top: 0;
            font-weight: 800;
            color: #0f172a;
            text-align: center;
            letter-spacing: -0.025em;
            margin-bottom: 0.5rem;
        }

        p.subtitle {
            text-align: center;
            color: #64748b;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }

        .form-group {
            margin-bottom: 1.25rem;
        }

        label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.025em;
        }

        input {
            width: 100%;
            padding: 0.8rem 1rem;
            border: 1px solid #cbd5e1;
            border-radius: 10px;
            font-size: 1rem;
            box-sizing: border-box;
            transition: all 0.2s ease;
            outline: none;
            background: #fdfdfd;
        }

        input:focus {
            border-color: var(--primary);
            background: #fff;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
        }

        button {
            width: 100%;
            background-color: var(--primary);
            color: white;
            padding: 1rem;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 1rem;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
        }

        button:hover {
            background-color: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        }

        button:active {
            transform: translateY(0);
        }

        .footer {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.75rem;
            color: #94a3b8;
            font-weight: 500;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>LOR Generator</h2>
    <p class="subtitle">Enter details to generate a formal recommendation</p>

    <form action="/lor" method="POST">
        <div class="form-group">
            <label>Full Name</label>
            <input name="name" placeholder="Candidate's Name" required>
        </div>

        <div class="form-group">
            <label>Designation / Role</label>
            <input name="role" placeholder="e.g. Technical Lead" required>
        </div>

        <div class="form-group">
            <label>Organization</label>
            <input name="org" placeholder="e.g. Bit By Bit Club" required>
        </div>

        <div class="form-group">
            <label>Tenure Duration</label>
            <input name="duration" placeholder="e.g. June 2023 - July 2024" required>
        </div>

        <button type="submit">Download PDF Document</button>
    </form>

    <div class="footer">
        Official Document Utility • Bit By Bit Club
    </div>
</div>

</body>
</html>
"""

def create_lor(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20)

    styles = getSampleStyleSheet()
    content = []

    # LOGO (Checking if file exists)
    if os.path.exists("logo.png"):
        logo = RLImage("logo.png", width=480, height=110)
        content.append(logo)
        content.append(Spacer(1, 10))

    # Title
    content.append(Paragraph("<b>LETTER OF RECOMMENDATION</b>", styles['Title']))
    content.append(Spacer(1, 15))

    # Date
    content.append(Paragraph(f"Date: {data['date']}", styles['Normal']))
    content.append(Spacer(1, 20))

    # CONTENT
    p1 = f"""
    This is to certify that <b>{data['name']}</b> has served as the <b>{data['role']}</b>
    at <b>{data['org']}</b> during the period of <b>{data['duration']}</b>.
    Throughout this tenure, {data['name']} has consistently demonstrated exceptional dedication,
    commitment, and professionalism in all assigned responsibilities.
    """

    p2 = f"""
    In this capacity, {data['name']} exhibited strong leadership qualities, excellent problem-solving skills,
    and the ability to work effectively both independently and as part of a team.
    Their innovative mindset and analytical thinking played a significant role in driving successful outcomes
    in various initiatives undertaken by the organization.
    """

    p3 = f"""
    {data['name']} actively contributed to planning, execution, and management of projects,
    ensuring timely delivery and maintaining high standards of quality.
    Their communication skills and collaborative approach greatly enhanced team productivity
    and fostered a positive working environment.
    """

    p4 = f"""
    Moreover, {data['name']}'s ability to adapt to challenges, learn new technologies, and take initiative
    in critical situations highlights their strong work ethic and growth mindset.
    Their contributions have been highly valuable and impactful.
    """

    p5 = """
    We sincerely appreciate the dedication, sincerity, and professionalism demonstrated,
    and we strongly recommend them for future academic and professional opportunities.
    We are confident that they will continue to achieve excellence in all their future endeavors.
    """

    # Add paragraphs
    for p in [p1, p2, p3, p4, p5]:
        content.append(Paragraph(p, styles['Normal']))
        content.append(Spacer(1, 15))

    # Signature
    content.append(Spacer(1, 20))
    content.append(Paragraph("Sincerely,", styles['Normal']))
    content.append(Spacer(1, 30))
    content.append(Paragraph("<b>Bit By Bit Club</b>", styles['Normal']))
    content.append(Paragraph("VIT Bhopal", styles['Normal']))

    doc.build(content)
    buffer.seek(0)
    return buffer

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/lor', methods=['POST'])
def lor():
    data = {
        'name': request.form['name'],
        'role': request.form['role'],
        'org': request.form['org'],
        'duration': request.form['duration'],
        'date': datetime.now().strftime("%d %B, %Y")
    }

    pdf = create_lor(data)
    return send_file(pdf, download_name=f"LOR_{data['name']}.pdf", mimetype='application/pdf')

if __name__ == "__main__":
    app.run(debug=True)
