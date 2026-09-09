"""
Professional PDF Report Generator
"""

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.platypus import Image, PageBreak
from reportlab.lib.utils import ImageReader


class PDFReport:

    def __init__(self, filename):

        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=1.5*cm,
            bottomMargin=1.5*cm
        )

        self.styles = getSampleStyleSheet()

        self.story = []

        self._create_styles()

    def _create_styles(self):

        self.title_style = self.styles["Title"]
        self.title_style.alignment = TA_CENTER

        self.heading = self.styles["Heading1"]

        self.normal = self.styles["BodyText"]

    def add_title(self):

        self.story.append(
            Paragraph(
                "DisasterVision AI",
                self.title_style
            )
        )

        self.story.append(
            Paragraph(
                "<b>Emergency Damage Assessment Report</b>",
                self.styles["Heading2"]
            )
        )

        self.story.append(Spacer(1, 15))

    def add_metadata(self):

        data = [

            ["Generated", datetime.now().strftime("%d %B %Y %H:%M")],

            ["Model", "DeepLabV3-ResNet50"],

            ["Framework", "PyTorch"],

            ["Explainability", "Grad-CAM Enabled"]

        ]

        table = Table(
            data,
            colWidths=[5*cm, 10*cm]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

            ])

        )

        self.story.append(table)

        self.story.append(Spacer(1, 20))

    def add_severity(self, severity):

        self.story.append(
            Paragraph(
                "Disaster Severity Index",
                self.heading
            )
        )

        data = [

            ["Severity Score", f"{severity['score']} / 100"],

            ["Severity Level", severity["level"]]

        ]

        table = Table(
            data,
            colWidths=[6*cm, 8*cm]
        )

        table.setStyle(

            TableStyle([

                ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

            ])

        )

        self.story.append(table)

        self.story.append(Spacer(1, 20))

    def add_section(self, title):

        self.story.append(
            Paragraph(title, self.heading)
        )

    def add_image(
        self,
        title,
        image_path,
        width=15
    ):
        """
        Add an image with a heading.
        """

        self.story.append(
            Paragraph(
                title,
                self.heading
            )
        )

        img = Image(
            image_path,
            width=width * cm,
            height=width * 0.75 * cm
        )

        img.hAlign = "CENTER"

        self.story.append(img)

        self.story.append(
            Spacer(1, 12)
        )

    def add_bullets(self, items):

        for item in items:

            self.story.append(
                Paragraph(
                    f"• {item}",
                    self.normal
                )
            )

        self.story.append(
            Spacer(1, 12)
        )

    def build(self):

        self.doc.build(self.story)


def create_pdf_report(
    filename,
    severity,
    summary,
    percentages,
    assessment,
    actions,
    original_path,
    segmentation_path,
    gradcam_path
):

    pdf = PDFReport(filename)

    pdf.add_title()

    pdf.add_metadata()

    pdf.add_severity(severity)

    pdf.add_image(
        "Original UAV Image",
        original_path
    )

    pdf.add_image(
        "Predicted Segmentation",
        segmentation_path
    )

    pdf.add_image(
        "Grad-CAM Explanation",
        gradcam_path
    )

    pdf.add_section("Executive Summary")

    pdf.add_bullets(summary)

    pdf.add_section("Operational Assessment")

    pdf.add_bullets(assessment)

    pdf.add_section("Recommended Actions")

    pdf.add_bullets(actions)

    pdf.build()
