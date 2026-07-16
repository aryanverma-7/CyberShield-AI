import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class CaseReportGenerator:
    @staticmethod
    def generate_pdf(case_data):
        """
        Generates a production-quality, forensic-grade PDF case document.
        Takes a dictionary of case parameters and returns a BytesIO buffer.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch
        )
        
        styles = getSampleStyleSheet()
        
        # Custom Typography Layouts
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'DocSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=20
        )
        
        h1_style = ParagraphStyle(
            'SectionH1',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#1e3a8a'),
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            'BodyMain',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=15,
            textColor=colors.HexColor('#334155'),
            spaceAfter=10
        )
        
        bold_body = ParagraphStyle(
            'BodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        story = []

        # 1. Header Banner/Title Component
        story.append(Paragraph("CYBERSHIELD NATIONAL INTELIGENCE PLATFORM", title_style))
        story.append(Paragraph(f"OFFICIAL INCIDENT DOSSIER // GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST", subtitle_style))
        
        # 2. Case Overview Meta Grid Matrix
        meta_data = [
            [Paragraph("<b>Case Reference ID:</b>", body_style), Paragraph(case_data.get('case_id', 'N/A'), body_style),
             Paragraph("<b>Classification:</b>", body_style), Paragraph(case_data.get('classification', 'CONFIDENTIAL'), body_style)],
            [Paragraph("<b>Primary Scam Type:</b>", body_style), Paragraph(case_data.get('scam_type', 'N/A'), body_style),
             Paragraph("<b>Threat Vector Index:</b>", body_style), Paragraph(f"{case_data.get('threat_score', 0)} / 100", bold_body)],
            [Paragraph("<b>Assigned Precinct:</b>", body_style), Paragraph(case_data.get('location', 'National Cyber Cell'), body_style),
             Paragraph("<b>Current Status:</b>", body_style), Paragraph(case_data.get('status', 'Under Review'), bold_body)]
        ]
        
        meta_table = Table(meta_data, colWidths=[1.5*inch, 2.25*inch, 1.5*inch, 2.25*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 15))

        # 3. Incident Summary
        story.append(Paragraph("1. Executive Summary & Incident Narrative", h1_style))
        story.append(Paragraph(case_data.get('summary', 'No summary details provided.'), body_style))

        # 4. Deep Threat Analysis
        story.append(Paragraph("2. Forensic Threat Vector Analysis", h1_style))
        story.append(Paragraph(case_data.get('analysis', 'No formal intelligence analysis logged.'), body_style))

        # 5. Infrastructure Network / Extracted Evidence Node Grid
        story.append(Paragraph("3. Logged Infrastructure Evidence Base", h1_style))
        
        evidence_headers = [Paragraph("<b>Entity Token</b>", bold_body), Paragraph("<b>Infrastructure Class</b>", bold_body), Paragraph("<b>Risk Metric</b>", bold_body)]
        evidence_rows = [evidence_headers]
        
        for entity in case_data.get('entities', []):
            evidence_rows.append([
                Paragraph(entity.get('value', 'N/A'), body_style),
                Paragraph(entity.get('type', 'N/A'), body_style),
                Paragraph(entity.get('risk', 'N/A'), body_style)
            ])
            
        evidence_table = Table(evidence_rows, colWidths=[3.5*inch, 2.25*inch, 1.75*inch])
        evidence_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0'))
        ]))
        story.append(evidence_table)
        story.append(Spacer(1, 15))

        # 6. Actionable Operational Recommendations
        story.append(Paragraph("4. Statutory Directives & Countermeasures", h1_style))
        story.append(Paragraph(case_data.get('recommendation', 'No direct instructions logged.'), body_style))

        # Build Document Container Array
        doc.build(story)
        buffer.seek(0)
        return buffer