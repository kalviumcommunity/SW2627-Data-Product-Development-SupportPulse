import os
import html
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


def markdown_to_simple_html(markdown_text):
    """
    Convert basic Markdown into HTML.
    """

    lines = markdown_text.splitlines()

    output = []

    for line in lines:

        line = line.strip()

        if not line:
            output.append("<br>")
            continue

        if line.startswith("# "):

            output.append(
                f"<h1>{html.escape(line[2:])}</h1>"
            )

        elif line.startswith("## "):

            output.append(
                f"<h2>{html.escape(line[3:])}</h2>"
            )

        elif line.startswith("### "):

            output.append(
                f"<h3>{html.escape(line[4:])}</h3>"
            )

        elif line.startswith("- "):

            output.append(
                f"<li>{html.escape(line[2:])}</li>"
            )

        else:

            output.append(
                f"<p>{html.escape(line)}</p>"
            )

    return "\n".join(output)


def markdown_to_pdf(markdown_text, pdf_path):
    """
    Create a PDF report from Markdown content.
    """

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    for line in markdown_text.splitlines():

        line = line.strip()

        if not line:

            story.append(
                Spacer(1, 8)
            )

            continue

        if line.startswith("# "):

            story.append(
                Paragraph(
                    html.escape(line[2:]),
                    styles["Title"]
                )
            )

        elif line.startswith("## "):

            story.append(
                Paragraph(
                    html.escape(line[3:]),
                    styles["Heading2"]
                )
            )

        elif line.startswith("### "):

            story.append(
                Paragraph(
                    html.escape(line[4:]),
                    styles["Heading3"]
                )
            )

        elif line.startswith("- "):

            story.append(
                Paragraph(
                    "• " + html.escape(line[2:]),
                    styles["BodyText"]
                )
            )

        else:

            story.append(
                Paragraph(
                    html.escape(line),
                    styles["BodyText"]
                )
            )

        story.append(
            Spacer(1, 5)
        )

    document.build(story)


def create_metadata(df, report_dir):

    metadata_path = os.path.join(
        report_dir,
        "README.md"
    )

    generated_time = datetime.now()

    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "# SupportPulse Analysis Export\n\n"
        )

        file.write(
            f"- **Generated:** "
            f"{generated_time.isoformat()}\n"
        )

        file.write(
            f"- **Records:** {len(df)}\n"
        )

        file.write(
            f"- **Columns:** "
            f"{list(df.columns)}\n"
        )

        file.write(
            "- **Source:** SupportPulse customer, "
            "ticket and transaction analysis\n"
        )

    return metadata_path


def export_analysis(
    df,
    summary_text,
    charts_dict,
    output_dir="output/reports"
):
    """
    Export SupportPulse analysis as:

    - CSV
    - PDF
    - Interactive HTML
    - README metadata
    """

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H%M%S"
    )

    report_dir = os.path.join(
        output_dir,
        f"{timestamp}_analysis"
    )

    os.makedirs(
        report_dir,
        exist_ok=True
    )

    print("=" * 70)
    print("SUPPORTPULSE REPORT EXPORT")
    print("=" * 70)

    # ==========================================
    # CSV
    # ==========================================

    csv_path = os.path.join(
        report_dir,
        "cleaned_data.csv"
    )

    df.to_csv(
        csv_path,
        index=False
    )

    print(
        f"✓ CSV exported: {csv_path}"
    )

    # ==========================================
    # PDF
    # ==========================================

    pdf_path = os.path.join(
        report_dir,
        "summary_report.pdf"
    )

    markdown_to_pdf(
        summary_text,
        pdf_path
    )

    print(
        f"✓ PDF exported: {pdf_path}"
    )

    # ==========================================
    # HTML
    # ==========================================

    html_path = os.path.join(
        report_dir,
        "interactive_report.html"
    )

    summary_html = markdown_to_simple_html(
        summary_text
    )

    html_content = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>SupportPulse Analysis Report</title>

<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    background: #f8fafc;
    color: #111827;
}}

.report {{
    max-width: 1100px;
    margin: auto;
    background: white;
    padding: 35px;
    border-radius: 12px;
}}

h1 {{
    color: #1d4ed8;
}}

h2 {{
    color: #1e40af;
    margin-top: 30px;
}}

.chart-container {{
    margin-top: 35px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
}}

.metadata {{
    margin-top: 30px;
    padding: 15px;
    background: #eff6ff;
    border-radius: 8px;
}}

</style>

</head>

<body>

<div class="report">

<h1>SupportPulse Analysis Report</h1>

<div class="metadata">

<p>
Generated:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</p>

<p>
Records:
{len(df)}
</p>

</div>

<div class="summary">

{summary_html}

</div>
"""

    # ==========================================
    # PLOTLY CHARTS
    # ==========================================

    for chart_name, figure in charts_dict.items():

        chart_html = figure.to_html(
            include_plotlyjs=False,
            full_html=False
        )

        html_content += f"""

<div class="chart-container">

<h2>
{html.escape(chart_name)}
</h2>

{chart_html}

</div>

"""

    html_content += """

</div>

</body>

</html>
"""

    with open(
        html_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            html_content
        )

    print(
        f"✓ HTML exported: {html_path}"
    )

    # ==========================================
    # METADATA
    # ==========================================

    metadata_path = create_metadata(
        df,
        report_dir
    )

    print(
        f"✓ Metadata created: {metadata_path}"
    )

    print("=" * 70)

    print(
        f"All exports saved in:\n{report_dir}"
    )

    return report_dir