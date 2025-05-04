from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO
from datetime import datetime

def create_patient_pdf(patient):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    story.append(Paragraph(f"Patient Report - {patient['name']}", title_style))

    # Define section style
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=20
    )
    
    # General Information
    story.append(Paragraph("General Information", section_style))
    general_info = [
        ["Name", patient['name']],
        ["OPD/UID", patient['opd_uid']],
        ["Age", str(patient['age'])],
        ["Gender", patient['gender']],
        ["Doctor Referred", patient.get('doctor_referred', '')],
        ["Address", patient['address']],
        ["Husband's Occupation", patient.get('occupation_husband', '')],
        ["Wife's Occupation", patient.get('occupation_wife', '')],
        ["Education", patient.get('education', '')],
        ["Phone 1", patient['phone1']],
        ["Phone 2", patient.get('phone2', '')],
        ["Email", patient.get('email', '')],
        ["Has Insurance", "Yes" if patient.get('has_insurance') else "No"],
        ["Registration Date", patient['registration_date'].strftime('%Y-%m-%d') if patient['registration_date'] else ''],
    ]
    story.append(create_table(general_info))

    # Family Information
    story.append(Paragraph("Family Information", section_style))
    family_info = [
        ["Years of Marriage", str(patient.get('years_of_marriage', ''))],
        ["Number of Boys", str(patient.get('boys_count', 0))],
        ["Number of Girls", str(patient.get('girls_count', 0))],
        ["Previous Abortion", "Yes" if patient.get('had_abortion') else "No"],
        ["Number of Abortions", str(patient.get('abortion_count', 0))],
        ["Delivery Type", patient.get('delivery_type', '')],
    ]
    story.append(create_table(family_info))

    # Menstrual Information
    story.append(Paragraph("Menstrual Information", section_style))
    menstrual_info = [
        ["Last Menstruation Date", patient.get('last_menstruation_date', '').strftime('%Y-%m-%d') if patient.get('last_menstruation_date') else ''],
        ["Days of Bleeding", str(patient.get('menstruation_days', ''))],
        ["Cycle Length (days)", str(patient.get('menstruation_cycle_length', ''))],
        ["Age When Started", str(patient.get('menstruation_start_age', ''))],
    ]
    story.append(create_table(menstrual_info))

    # Medical History
    story.append(Paragraph("Medical History", section_style))
    medical_conditions = []
    if patient.get('has_thyroid'): medical_conditions.append("Thyroid")
    if patient.get('has_diabetes'): medical_conditions.append("Diabetes")
    if patient.get('has_asthma'): medical_conditions.append("Asthma")
    if patient.get('has_bp'): medical_conditions.append("High Blood Pressure")
    if patient.get('has_epilepsy'): medical_conditions.append("Epilepsy")
    
    medical_history = [
        ["Medical Conditions", ", ".join(medical_conditions) if medical_conditions else "None"],
        ["Currently on Medication", "Yes" if patient.get('on_medication') else "No"],
        ["Medication Names", patient.get('medication_names', '')],
        ["Previous Surgeries", patient.get('previous_surgeries', '')],
        ["Previous Pap Smear", "Yes" if patient.get('had_pap_smear') else "No"],
        ["Days since Pap Smear", str(patient.get('pap_smear_days', ''))],
        ["Medicine Allergies", patient.get('medicine_allergies', '')],
        ["Family History of Cancer", "Yes" if patient.get('has_cancer_history') else "No"],
        ["Previous Reports", patient.get('previous_reports', '')],
    ]
    story.append(create_table(medical_history))

    # Symptoms & Complaints
    story.append(Paragraph("Symptoms & Complaints", section_style))
    symptoms = [
        ["Blood Clots", f"{'Yes' if patient.get('has_blood_clots') else 'No'} ({patient.get('blood_clots_days', '')} days)"],
        ["White Discharge", f"{'Yes' if patient.get('has_white_discharge') else 'No'} ({patient.get('white_discharge_days', '')} days)"],
        ["Red Discharge", f"{'Yes' if patient.get('has_red_discharge') else 'No'} ({patient.get('red_discharge_days', '')} days)"],
        ["Abdominal Pain", f"{'Yes' if patient.get('has_abdominal_pain') else 'No'} ({patient.get('abdominal_pain_days', '')} days)"],
        ["Vaginal Discharge", f"{'Yes' if patient.get('has_vaginal_discharge') else 'No'} ({patient.get('vaginal_discharge_days', '')} days)"],
        ["Bleeding After Intercourse", f"{'Yes' if patient.get('has_bleeding_intercourse') else 'No'} ({patient.get('bleeding_intercourse_days', '')} days)"],
        ["Urine Leakage", f"{'Yes' if patient.get('has_urine_leakage') else 'No'} ({patient.get('urine_leakage_days', '')} days)"],
        ["Post Menopausal Bleeding", f"{'Yes' if patient.get('has_postmenopausal_bleeding') else 'No'} ({patient.get('postmenopausal_bleeding_days', '')} days)"],
        ["Breast Lump", f"{'Yes' if patient.get('has_breast_lump') else 'No'} ({patient.get('breast_lump_days', '')} days)"],
        ["Infertility", f"{'Yes' if patient.get('has_infertility') else 'No'} ({patient.get('infertility_days', '')} days)"],
        ["Other Troubles", patient.get('other_troubles', '')],
        ["Other Troubles Days", str(patient.get('other_troubles_days', ''))],
    ]
    story.append(create_table(symptoms))

    # General Examination
    story.append(Paragraph("General Examination", section_style))
    examination = [
        ["Height", f"{patient.get('height', '')} cm"],
        ["Weight", f"{patient.get('weight', '')} kg"],
        ["Blood Pressure", patient.get('blood_pressure', '')],
        ["Pulse Rate", str(patient.get('pulse_rate', ''))],
        ["Pallar", patient.get('pallar', '')],
        ["Edema", patient.get('edema', '')],
        ["Thyroid Exam", patient.get('thyroid_exam', '')],
        ["Lymph Nodes", patient.get('lymph_nodes', '')],
        ["Breast Exam", patient.get('breast_exam', '')],
        ["RS Exam", patient.get('rs_exam', '')],
        ["CVS Exam", patient.get('cvs_exam', '')],
        ["P/A Exam", patient.get('pa_exam', '')],
        ["P/S/V Exam", patient.get('psv_exam', '')],
        ["P/R Exam", patient.get('pr_exam', '')],
    ]
    story.append(create_table(examination))

    # Surgery Details
    story.append(Paragraph("Surgery Details", section_style))
    surgery = [
        ["Surgery Name", patient.get('surgery_name', '')],
        ["Surgery Date", patient.get('surgery_date', '').strftime('%Y-%m-%d') if patient.get('surgery_date') else ''],
        ["Hospital", patient.get('surgery_hospital', '')],
        ["Pre-op Investigation", patient.get('preop_investigation', '')],
        ["Pre-op Fitness", patient.get('preop_fitness', '')],
    ]
    story.append(create_table(surgery))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_table(data):
    table = Table(data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align text to top for multi-line cells
    ]))
    return table 

def create_followup_pdf(followup, patient):
    # Create buffer and document
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    elements = []
    
    # Enhanced Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=5,
        alignment=1,  # Center
        textColor=colors.HexColor('#2c3e50')
    ))
    styles.add(ParagraphStyle(
        name='SubTitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=1,  # Center
        textColor=colors.HexColor('#34495e')
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.HexColor('#2980b9')
    ))
    styles.add(ParagraphStyle(
        name='NormalText',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=15,
        textColor=colors.HexColor('#2c3e50')
    ))

    # Common table style
    common_table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#95a5a6')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
    ])

    # Header with Logo/Hospital Name and Generation Time
    header_data = [
        [Paragraph("Sparsh Hospital", styles['CustomTitle']), 
         Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                  ParagraphStyle(
                      'GenerationTime',
                      parent=styles['Normal'],
                      fontSize=8,
                      textColor=colors.HexColor('#7f8c8d'),
                      alignment=2  # Right alignment
                  ))],
        [Paragraph("Follow-up Report", styles['SubTitle']), ""]
    ]
    
    header_table = Table(header_data, colWidths=[400, 100])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # Patient and Visit Information in a single table
    info_data = [
        # Header row
        [Paragraph("<b>Patient Information</b>", styles['NormalText']), 
         "", 
         Paragraph("<b>Visit Details</b>", styles['NormalText']), 
         ""],
        # Data rows
        ["Name:", patient['name'], "Visit Date:", followup['visit_date'].strftime('%Y-%m-%d')],
        ["Patient ID:", patient['opd_uid'], "Doctor:", followup['doctor_name']],
        ["Gender:", patient['gender'].title(), "Next Visit:", 
         followup['next_visit_date'].strftime('%Y-%m-%d') if followup['next_visit_date'] else 'Not scheduled'],
        ["Phone:", patient['phone1'], "", ""],
    ]
    
    info_table = Table(info_data, colWidths=[80, 170, 80, 170])
    info_table_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (2, 0), (3, 0), colors.HexColor('#f8f9fa')),
        ('SPAN', (0, 0), (1, 0)),  # Merge cells for "Patient Information"
        ('SPAN', (2, 0), (3, 0)),  # Merge cells for "Visit Details"
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#95a5a6')),
    ])
    info_table.setStyle(info_table_style)
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Medical Details
    for section in [
        ('Complaints', followup['complaints']),
        ('Examination', followup['examination']),
        ('Diagnosis', followup['diagnosis']),
        ('Treatment', followup['treatment'])
    ]:
        if section[1]:
            elements.append(Paragraph(section[0], styles['SectionHeader']))
            detail_table = Table([[section[1]]], colWidths=[500])
            detail_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ]))
            elements.append(detail_table)
            elements.append(Spacer(1, 10))
    
    # Prescriptions
    if followup.get('prescriptions'):
        elements.append(Paragraph("Prescriptions", styles['SectionHeader']))
        prescription_data = [["Medicine", "Quantity/Dosage", "Notes"]]
        for prescription in followup['prescriptions']:
            prescription_data.append([
                prescription['medicine_name'],
                prescription['quantity'],
                prescription.get('notes', '')
            ])
        
        prescription_table = Table(prescription_data, colWidths=[200, 150, 150])
        prescription_table.setStyle(common_table_style)
        elements.append(prescription_table)
    
    # Footer with line (remove the timestamp)
    elements.append(Spacer(1, 30))
    elements.append(Table([[""]],
                         style=[
                             ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#ecf0f1'))
                         ]))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer 