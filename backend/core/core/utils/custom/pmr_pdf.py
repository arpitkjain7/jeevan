from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import uuid, os, json, io

from functools import reduce

from core import logger

logging = logger(__name__)

vital_units_map = {
    "blood_pressure": "mm/Hg",
    "heart_rate": "/min",
    "respiratory_rate": "/min",
    "temperature": "°C",
    "oxygen_saturation": "%",
}


# Define a function to create the PDF
def create_pdf(file_obj, input_data, pdf_type):
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

    def create_text_section(title, data):
        if data:
            elements.append(Paragraph(title, styles["Bold"]))
            for item in data:
                elements.append(Paragraph(f"{item['label']}", styles["Normal"]))
            elements.append(Spacer(1, 12))

    if pdf_type == "summary":
        logging.info(f"{pdf_type=}")
        # Vitals section
        logging.info("Adding vital section")
        vitals_data = []
        for key, value in input_data["pmr_request"]["summarised_notes"]["objective"][
            "vital_signs"
        ].items():
            if value is not None and value != "":
                vitals_data.append(
                    {
                        "label": key.replace("_", " ").title(),
                        "value": f"{value} {vital_units_map[key]}",
                    }
                )
        create_section("Vitals", vitals_data)

        # Cheif Complaints section
        logging.info("Adding cheif complaints section")
        item = input_data["pmr_request"]["summarised_notes"]["subjective"][
            "chief_complaint"
        ]
        chief_complaint_data = [{"label": item}]
        create_text_section("Cheif Complaints", chief_complaint_data)

        # Symptoms section
        logging.info("Adding symtoms section")
        symptoms_data = [
            {"label": item}
            for item in input_data["pmr_request"]["summarised_notes"]["subjective"][
                "history_of_present_illness"
            ]
        ]
        create_text_section("Symptoms", symptoms_data)

        # Medical history section
        logging.info("Adding medical history section")
        medical_history_data = [
            {"label": item}
            for item in input_data["pmr_request"]["summarised_notes"]["subjective"][
                "past_medical_history"
            ]
        ]
        create_text_section("Medical History", medical_history_data)

        # Family history section
        logging.info("Adding Family history section")
        family_history_data = [
            {"label": item}
            for item in input_data["pmr_request"]["summarised_notes"]["subjective"][
                "family_history"
            ]
        ]
        create_text_section("Family History", family_history_data)

        # Examination Findings section
        examination_findings_data = []
        if input_data["pmr_request"]["summarised_notes"]["objective"][
            "physical_examination_findings"
        ]:
            examination_findings_data.append(
                {
                    "label": "Examination Findings",
                    "value": input_data["pmr_request"]["summarised_notes"]["objective"][
                        "physical_examination_findings"
                    ],
                }
            )
        if len(examination_findings_data) > 0:
            logging.info("Adding Examination Findings section")
            create_section("Examination Findings", examination_findings_data)

        # Diagnosis section
        diagnosis_data = []
        if input_data["pmr_request"]["summarised_notes"]["assessment"][
            "preliminary_diagnosis"
        ]:
            diagnosis_data.append(
                {
                    "label": "Preliminary Diagnosis",
                    "value": input_data["pmr_request"]["summarised_notes"][
                        "assessment"
                    ]["preliminary_diagnosis"],
                }
            )
        if input_data["pmr_request"]["summarised_notes"]["assessment"][
            "differential_diagnosis"
        ]:
            logging.info("differential_diagnosis")
            logging.info(
                input_data["pmr_request"]["summarised_notes"]["assessment"][
                    "differential_diagnosis"
                ]
            )
            diagnosis_data.append(
                {
                    "label": "Differential Diagnosis",
                    "value": input_data["pmr_request"]["summarised_notes"][
                        "assessment"
                    ]["differential_diagnosis"],
                }
            )
        if len(diagnosis_data) > 0:
            logging.info("Adding diagnosis section")
            create_section("Diagnosis", diagnosis_data)

        # Lab investigation section
        lab_investigation_data = []
        if input_data["pmr_request"]["summarised_notes"]["tests_to_be_taken"][
            "laboratory_tests"
        ]:
            item = reduce(
                lambda x, y: str(x) + ", " + str(y),
                input_data["pmr_request"]["summarised_notes"]["tests_to_be_taken"][
                    "laboratory_tests"
                ],
            )
            lab_investigation_data.extend(
                [{"label": "Lab Investigation", "value": item}]
            )
        if input_data["pmr_request"]["summarised_notes"]["tests_to_be_taken"][
            "imaging_tests"
        ]:
            # Imaging investigation section
            item = reduce(
                lambda x, y: str(x) + ", " + str(y),
                input_data["pmr_request"]["summarised_notes"]["tests_to_be_taken"][
                    "imaging_tests"
                ],
            )
            lab_investigation_data.extend(
                [{"label": "Imaging Investigation", "value": item}]
            )

        if input_data["pmr_request"]["summarised_notes"]["tests_to_be_taken"][
            "special_exams"
        ]:
            # Special investigation section
            item = reduce(
                lambda x, y: str(x) + ", " + str(y),
                input_data["pmr_request"]["summarised_notes"]["tests_to_be_taken"][
                    "special_exams"
                ],
            )
            lab_investigation_data.extend(
                [{"label": "Special Investigation", "value": item}]
            )
        if len(lab_investigation_data) > 0:
            logging.info("Adding lab investigation section")
            create_section("Investigations", lab_investigation_data)
        # Prescription section
        if input_data["pmr_request"]["summarised_notes"]["prescription"]["medications"]:
            logging.info("Adding medication section")
            elements.append(Paragraph("Prescription", styles["Bold"]))
            medication_data = [
                [
                    Paragraph("Medications", styles["TableHeader"]),
                    Paragraph("Frequency", styles["TableHeader"]),
                    Paragraph("Duration", styles["TableHeader"]),
                    Paragraph("Dosage", styles["TableHeader"]),
                    Paragraph("Time of day", styles["TableHeader"]),
                    Paragraph("Notes", styles["TableHeader"]),
                ]
            ]
            for item in input_data["pmr_request"]["summarised_notes"]["prescription"][
                "medications"
            ]:
                medication_data.append(
                    [
                        item["med_name"],
                        item["frequency"],
                        item["duration"],
                        item["dosages"],
                        item["time_of_day"],
                        item["instructions"],
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

        # Advice section
        if input_data["pmr_request"]["summarised_notes"]["other_next_steps"][
            "precautions"
        ]:
            logging.info("Adding advice section")
            elements.append(Paragraph("Advice", styles["Bold"]))
            for item in input_data["pmr_request"]["summarised_notes"][
                "other_next_steps"
            ]["precautions"]:
                elements.append(
                    Paragraph(
                        item,
                        styles["Normal"],
                    )
                )
            elements.append(Spacer(1, 12))

        # Lifestyle modifications section
        if input_data["pmr_request"]["summarised_notes"]["other_next_steps"][
            "lifestyle_modifications"
        ]:
            logging.info("Adding lifestyle modifications section")
            elements.append(Paragraph("Lifestyle Modifications", styles["Bold"]))
            for item in input_data["pmr_request"]["summarised_notes"][
                "other_next_steps"
            ]["lifestyle_modifications"]:
                elements.append(
                    Paragraph(
                        item,
                        styles["Normal"],
                    )
                )
            elements.append(Spacer(1, 12))

        # Notes section
        if input_data["pmr_request"]["summarised_notes"]["additional_notes"]["content"]:
            logging.info("Adding Notes section")
            elements.append(Paragraph("Notes", styles["Bold"]))
            elements.append(
                Paragraph(
                    input_data["pmr_request"]["summarised_notes"]["additional_notes"][
                        "content"
                    ]
                )
            )
            elements.append(Spacer(1, 12))

        # Follow-up section
        if input_data["pmr_request"]["summarised_notes"]["plan"]["follow_up"]:
            logging.info("Adding follow-up section")
            elements.append(Paragraph("Follow-up", styles["Bold"]))
            for follow_up in input_data["pmr_request"]["summarised_notes"]["plan"][
                "follow_up"
            ].split("|"):
                elements.append(
                    Paragraph(
                        follow_up,
                        styles["Normal"],
                    )
                )
            elements.append(Spacer(1, 12))

        # Referral section
        if input_data["pmr_request"]["summarised_notes"]["other_next_steps"][
            "referrals"
        ]:
            logging.info("Adding referral section")
            elements.append(Paragraph("Referral", styles["Bold"]))
            for referral in input_data["pmr_request"]["summarised_notes"][
                "other_next_steps"
            ]["referrals"]:
                elements.append(
                    Paragraph(
                        referral,
                        styles["Normal"],
                    )
                )
            elements.append(Spacer(1, 12))

    elif pdf_type == "pmr":
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
            elements.append(
                Paragraph(input_data["pmr_request"]["notes"], styles["Normal"])
            )
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
                Paragraph(
                    input_data["appointment_request"]["followup"], styles["Normal"]
                )
            )
            elements.append(Spacer(1, 12))

        # Build the PDF
    doc.build(elements)
    return file_obj
