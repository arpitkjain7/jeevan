import { Typography, styled } from "@mui/material";
import React from "react";
import ComplaintTable from "./Sections/ComplaintTable";
import MedicalHistoryTable from "./Sections/MedicalHistoryTable";
import MedicationTable from "./Sections/MedicationTable";
import PhysicalExaminationTable from "./Sections/PhysicalExaminationTable";
import AttachmentSection from "./Sections/Attachments";

const HealthReportBodyContainer = styled("div")(({ theme }) => ({
  width: "800px",
  margin: "0 auto",
}));

const HealthReportHeader = styled("div")(({ theme }) => ({
  "& .documentInfo": {
    display: "flex",
    flexDirection: "row",
    margin: "0px 0px 0px 10px",
  },
  "& .ReportInfo": {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    padding: theme.spacing(1),
    backgroundColor: "#cbc8c8",
    borderRadius: "5px",
  },
  "& .ReportDate": {
    display: "flex",
    flexDirection: "column",
  },
}));

const HealthReportBody = styled("div")(({ theme }) => ({
  border: "1px solid black",
  padding: theme.spacing(2, 4),
  height: "500px",
  overflowY: "auto",
  scrollbarWidth: "thin",
}));

const ReportSections = styled("div")(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  marginBottom: theme.spacing(5),
}));

function FhirDoc() {
  const FhirDocDetails = JSON.parse(sessionStorage?.getItem("FhirDocDetails"));
  const DocData = FhirDocDetails?.patient_data_transformed[0];
  const DocDate = DocData.Composition[0].date;
  return (
    <HealthReportBodyContainer>
      <HealthReportHeader>
        <Typography
          variant="h4"
          fontSize={25}
          sx={{ textTransform: "uppercase", mb: 2 }}
        >
          {FhirDocDetails.hip_name}
        </Typography>
        <div className="ReportInfo">
          <div className="documentInfo">
            <Typography variant="h6" fontSize={18} fontWeight={600}>
              Document:
            </Typography>
            <Typography variant="h6" fontSize={18} fontWeight={600}>
              {DocData.DocumentReference[0].type.text}
            </Typography>
          </div>
          <div className="ReportDate">
            <div className="documentInfo">
              <Typography variant="body1" fontSize={14} fontWeight={600}>
                Date:
              </Typography>
              <Typography variant="body1" fontSize={14}>
                {DocDate}
              </Typography>
            </div>
            <div className="documentInfo">
              <Typography variant="body1" fontSize={14} fontWeight={600}>
                Authors:
              </Typography>
              <Typography variant="body1" fontSize={14}>
                {DocData.Practitioner[0].name[0].text}
              </Typography>
            </div>
            <div className="documentInfo">
              <Typography variant="body1" fontSize={14} fontWeight={600}>
                Status:
              </Typography>
              <Typography
                variant="body1"
                fontSize={14}
                sx={{ textTransform: "uppercase" }}
              >
                {DocData.Composition[0].status}
              </Typography>
            </div>
          </div>
        </div>
      </HealthReportHeader>
      <HealthReportBody>
        <div className="EncounterSection">
          <Typography variant="h6" fontSize={18} fontWeight={600}>
            Encounter:
          </Typography>
          <ul style={{ listStyle: "circle black" }}>
            <li>
              <Typography variant="body1" fontSize={14}>
                {`${DocData.Encounter[0].class.display},${DocData.Encounter[0].status}`}
              </Typography>
            </li>
          </ul>
        </div>
        <ReportSections>
          <ReportSections>
            <MedicationTable data={DocData.MedicationRequest} />
          </ReportSections>
          <ReportSections>
            <ComplaintTable data={DocData.Condition} />
          </ReportSections>
          <ReportSections>
            <MedicalHistoryTable data={DocData.Condition} />
          </ReportSections>
          <ReportSections>
            <PhysicalExaminationTable
              data={DocData.Observation}
              date={DocDate}
            />
          </ReportSections>
          <ReportSections>
            <AttachmentSection data={DocData.DocumentReference} />
          </ReportSections>
        </ReportSections>
      </HealthReportBody>
    </HealthReportBodyContainer>
  );
}

export default FhirDoc;
