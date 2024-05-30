import { Typography, styled } from "@mui/material";
import React from "react";
import pdfData from "../../assets/jsonFile/HealthData.json";
import ConditionTable from "./Sections/ConditionTable";
import MedicalHistoryTable from "./Sections/MedicalHistoryTable";
import MedicationTable from "./Sections/MedicationTable";
import PhysicalExaminationTable from "./Sections/PhysicalExaminationTable";

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

function HealthReport() {
  const DocData = pdfData[0];
  return (
    <HealthReportBodyContainer>
      <HealthReportHeader>
        <Typography
          variant="h4"
          fontSize={25}
          sx={{ textTransform: "uppercase", mb: 2 }}
        >
          Hospital Name
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
                Values
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
                Final:
              </Typography>
              <Typography
                variant="body1"
                fontSize={14}
                sx={{ textTransform: "uppercase" }}
              >
                {DocData.DocumentReference[0].docStatus}
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
            {DocData.Encounter.map((encounter) => (
              <li key={`${encounter.id}`}>
                <Typography variant="body1" fontSize={14}>
                  {`${encounter.class.display},${encounter.status}`}
                </Typography>
              </li>
            ))}
          </ul>
        </div>
        <ReportSections>
          <ReportSections>
            <MedicationTable data={DocData.MedicationRequest} />
          </ReportSections>
          <ReportSections>
            <ConditionTable data={DocData.Condition} />
          </ReportSections>
          <ReportSections>
            <MedicalHistoryTable data={DocData.Condition} />
          </ReportSections>
          <ReportSections>
            <PhysicalExaminationTable data={DocData.Observation} />
          </ReportSections>
        </ReportSections>
      </HealthReportBody>
    </HealthReportBodyContainer>
  );
}

export default HealthReport;
