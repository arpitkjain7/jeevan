import React, { useEffect, useState } from "react";
import { Box, Typography, Grid, styled } from "@mui/material";
import { useSelector } from "react-redux";

const RegisterationConfirmationWrapper = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    padding: theme.spacing(4, 6),
  },
  ".registration-success-text": {
    "&.MuiTypography-root": theme.typography.successText,
  },
  ".registeration-success-key": {
    "&.MuiTypography-root": theme.typography.customKeys,
  },
  ".registration-success-header": {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: theme.spacing(6),
  },
}));

const RegisterationConfirmation = () => {
  const dataState = useSelector((state) => state);
  const patientData =
    dataState.PatientRegistartion.registeredPatientDetails;
  const [data, setData] = useState([]);

  const navigateToAppointment = () => {};
  useEffect(() => {

      const pageData = [
        { key: "Patient Name", value: patientData?.name },
        {
          key: "Patient Id",
          value: patientData?.id,
        },
        { key: "Gender", value: patientData?.gender },
        { key: "Date Of Birth", value: patientData?.DOB },
        { key: "Email Address", value: patientData?.email },
        { key: "AABHA Address", value: patientData?.aabha_address },
        { key: "ABHA ID", value: patientData?.aabha_number },
      ];
  
      setData(pageData);
    
  
  }, [patientData]);

  console.log(patientData)
  return (
    <RegisterationConfirmationWrapper>
      <Box padding={2}>
        <div className="registration-success-header">
          <Typography
            variant="h6"
            color="primary"
            gutterBottom
            className="registration-success-text"
          >
            Success
          </Typography>
          {/* <Button
            onClick={() => navigateToAppointment()}
            variant="contained"
            className="success-appointment-btn"
          >
            Create Appointment
          </Button> */}
        </div>
        <Grid container spacing={4} xs={12}>
          {data?.map((item) => (
            <Grid item key={item.key} xs={4}>
              <Typography
                variant="subtitle1"
                gutterBottom
                className="registeration-success-key"
              >
                {item?.key}
              </Typography>
              <Typography
                variant="body1"
                gutterBottom
                className="registeration-success-value"
              >
                {item?.value}
              </Typography>
            </Grid>
          ))}
        </Grid>
      </Box>
    </RegisterationConfirmationWrapper>
  );
};

export default RegisterationConfirmation;
