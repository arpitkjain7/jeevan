from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


# Define a function to create the PDF
def create_pdf(file_obj, input_data):
    doc = SimpleDocTemplate(
        file_obj,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=18,
    )
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="Header",
            fontSize=14,
            alignment=1,
            textColor=colors.white,
            spaceAfter=10,
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubHeader",
            fontSize=12,
            textColor=colors.white,
            spaceAfter=5,
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubHeader1",
            fontSize=10,
            alignment=1,
            textColor=colors.white,
            spaceAfter=5,
            fontName="Helvetica-Bold",
        )
    )

    styles.add(
        ParagraphStyle(
            name="Bold",
            fontSize=12,
            textColor=colors.black,
            spaceAfter=8,
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHeader",
            fontSize=12,
            textColor=colors.white,
            alignment=1,
            fontName="Helvetica-Bold",
        )
    )

    elements = []

    # PDF Header
    header_table = Table(
        [
            [
                Paragraph(
                    input_data["metadata"]["doctor_name"],
                    styles["Header"],
                ),
                Paragraph(
                    input_data["metadata"]["hospital_name"],
                    styles["SubHeader1"],
                ),
                Paragraph("Powered by CliniQ360", styles["SubHeader1"]),
            ]
        ],
        rowHeights=50,
    )
    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0089E9")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.white),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.white),
            ]
        )
    )
    elements.append(header_table)
    elements.append(Spacer(1, 5))

    # Patient details
    patient_data = [
        [
            Paragraph("Patient Name", styles["TableHeader"]),
            input_data["metadata"]["patient_name"],
            Paragraph("Patient#", styles["TableHeader"]),
            input_data["metadata"]["patient_uid"],
        ],
        [
            Paragraph("Gender", styles["TableHeader"]),
            input_data["metadata"]["patient_gender"],
            Paragraph("Contact#", styles["TableHeader"]),
            input_data["metadata"]["patient_contact_number"],
        ],
        [
            Paragraph("Age", styles["TableHeader"]),
            f"{input_data['metadata']['patient_age_years']} years",
            Paragraph("Email", styles["TableHeader"]),
            input_data["metadata"]["patient_email"],
        ],
    ]

    patient_details_table = Table(
        patient_data,
    )
    patient_details_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0089E9")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#0089E9")),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor("#0089E9")),
            ]
        )
    )
    elements.append(patient_details_table)
    elements.append(Spacer(1, 12))

    # Function to create a section
    # (rest of the function remains the same)

    # Function to create a section
    def create_section(title, data):
        if data:
            elements.append(Paragraph(title, styles["Bold"]))
            for item in data:
                elements.append(
                    Paragraph(f"{item['label']}: {item['value']}", styles["Normal"])
                )
            elements.append(Spacer(1, 12))

    # Vitals section
    vitals_data = [
        {"label": key.replace("_", " ").title(), "value": value}
        for key, value in input_data["pmr_request"]["vital"].items()
    ]
    create_section("Vitals", vitals_data)

    # Medical history section
    medical_history_data = [
        {
            "label": item["medical_history"],
            "value": f"{item['relationship']} | {item['since']}",
        }
        for item in input_data["pmr_request"]["medical_history"]["data"]
    ]
    create_section("Medical History", medical_history_data)

    # Symptoms section
    symptoms_data = [
        {"label": item["symptom"], "value": item["duration"]}
        for item in input_data["pmr_request"]["symptom"]["data"]
    ]
    create_section("Symptoms", symptoms_data)

    # Diagnosis section
    diagnosis_data = [
        {
            "label": item["disease"],
            "value": f"{item['diagnosis_type']} | {item['status']}",
        }
        for item in input_data["pmr_request"]["diagnosis"]["data"]
    ]
    create_section("Diagnosis", diagnosis_data)

    # # Condition section
    # condition_data = [
    #     {"label": item["condition"], "value": item["status"]}
    #     for item in input_data["pmr_request"]["condition"]["data"]
    # ]
    # create_section("Condition", condition_data)

    # Examination findings section
    examination_findings_data = [
        {"label": item["disease"], "value": ""}
        for item in input_data["pmr_request"]["examination_findings"]["data"]
    ]
    create_section("Examination Findings", examination_findings_data)

    # Lab investigation section
    lab_investigation_data = [
        {"label": item["name"], "value": ""}
        for item in input_data["pmr_request"]["lab_investigation"]["data"]
    ]
    create_section("Lab Investigation", lab_investigation_data)

    # Prescription section
    if input_data["pmr_request"]["medication"]["data"]:
        elements.append(Paragraph("Prescription", styles["Bold"]))
        medication_data = [
            [
                Paragraph("Medications", styles["TableHeader"]),
                Paragraph("Frequency", styles["TableHeader"]),
                Paragraph("Duration", styles["TableHeader"]),
                Paragraph("Dosage", styles["TableHeader"]),
                Paragraph("Notes", styles["TableHeader"]),
            ]
        ]
        for item in input_data["pmr_request"]["medication"]["data"]:
            medication_data.append(
                [
                    item["medicine_name"],
                    item["frequency"],
                    item["duration"],
                    item["dosage"],
                ]
            )

        medication_table = Table(medication_data)
        medication_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0089E9")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ]
            )
        )
        elements.append(medication_table)
        elements.append(Spacer(1, 12))

    # Notes section
    if input_data.get("notes"):
        elements.append(Paragraph("Notes", styles["Bold"]))
        elements.append(Paragraph(input_data["pmr_request"]["notes"], styles["Normal"]))
        elements.append(Spacer(1, 12))

    # Advice section
    if input_data.get("advice"):
        elements.append(Paragraph("Advice", styles["Bold"]))
        elements.append(
            Paragraph(input_data["pmr_request"]["advice"], styles["Normal"])
        )
        elements.append(Spacer(1, 12))

    # Follow-up section
    if input_data.get("followup"):
        elements.append(Paragraph("Follow-up", styles["Bold"]))
        elements.append(
            Paragraph(input_data["appointment_request"]["followup"], styles["Normal"])
        )
        elements.append(Spacer(1, 12))

    # Build the PDF
    doc.build(elements)
    return file_obj
