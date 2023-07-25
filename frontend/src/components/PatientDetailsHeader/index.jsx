import { Avatar, Typography, styled } from "@mui/material";
import React from "react";

const DetailsHeaderContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    padding: theme.spacing(5, 6),
  },
  ".details-header": {
    display: "flex",
    alignItems: "center",
  },
  ".details-Patientdetails": {
    padding: theme.spacing(0, 6),
    borderRight: `1px solid ${theme.palette.primaryGrey}`,
  },
  ".details-emailContainer": {
    padding: theme.spacing(0, 6),
  },
  ".details-subContainer": {
    display: "flex",
    alignItems: "center",
    gap: theme.spacing(2),
  },
  ".details-patient-name": {
    "&.MuiTypography-root": theme.typography.h3,
  },
  ".details-patient-id": {
    "&.MuiTypography-root": theme.typography.body4,
  },
  "details-patient-email": {
    "&.MuiTypography-root": theme.typography.body3,
  },
}));

const PatientDetailsHeader = ({ patientDetails }) => {
  return (
    <DetailsHeaderContainer>
      <div className="details-header">
        <div className="details-avatar-container">
          <Avatar />
        </div>
        <div className="details-Patientdetails">
          <Typography className="details-patient-name">Patient Name</Typography>
          <div className="details-subContainer">
            <Typography className="details-patient-id">100032</Typography>
            <Typography className="details-patient-id">Age 38</Typography>
            <Typography className="details-patient-id">Male</Typography>
          </div>
        </div>
        <div className="details-emailContainer">
          <Typography className="details-patient-email">
            abc@gmail.com
          </Typography>
          <Typography className="details-patient-email">123456789</Typography>
        </div>
      </div>
    </DetailsHeaderContainer>
  );
};

export default PatientDetailsHeader;
