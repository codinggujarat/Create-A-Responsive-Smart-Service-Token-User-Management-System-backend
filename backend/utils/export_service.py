import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

def export_to_excel(users):
    data = []
    for user in users:
        data.append({
            'Token Number': user.token_number,
            'Name': user.name,
            'Email': user.email,
            'Contact Number': user.contact_number,
            'Address': user.address,
            'Work Description': user.work_description,
            'Status': user.status,
            'Created At': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
            'Updated At': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else ''
        })
    
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Service Tokens')
    output.seek(0)
    return output

def export_to_csv(users):
    data = []
    for user in users:
        data.append({
            'Token Number': user.token_number,
            'Name': user.name,
            'Email': user.email,
            'Contact Number': user.contact_number,
            'Address': user.address,
            'Work Description': user.work_description,
            'Status': user.status,
            'Created At': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
            'Updated At': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else ''
        })
    
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

def export_to_pdf(users):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#4F46E5'),
        spaceAfter=30,
        alignment=1
    )
    
    title = Paragraph("Service Token Report", title_style)
    elements.append(title)
    
    subtitle = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.3*inch))
    
    data = [['Token', 'Name', 'Email', 'Contact', 'Status']]
    
    for user in users:
        data.append([
            str(user.token_number),
            user.name[:20] if len(user.name) > 20 else user.name,
            user.email[:25] if len(user.email) > 25 else user.email,
            user.contact_number,
            user.status
        ])
    
    table = Table(data, colWidths=[0.8*inch, 1.5*inch, 2*inch, 1.2*inch, 1*inch])
    
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    return buffer
