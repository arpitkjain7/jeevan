import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Typography, Grid, styled, Button } from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { downloadAabha } from "../../pages/PatientRegistration/PatientRegistration.slice";

const RegisterationConfirmationWrapper = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    marginTop: theme.spacing(8),
    [theme.breakpoints.down('sm')]: {
      margin: "8px"
    }
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
  ".btn-wrapper": {
     [theme.breakpoints.down('sm')]: {
        display: "flex",
        justifyContent: "space-around"
     }
  },
  ".submit-btn": {
    "&.MuiButtonBase-root": {
      display: "flex",
      float: "right",
      justifyContent: "center",
      alignItems: "center",
      border: `1px solid ${theme.palette.primaryBlack}`,
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      backgroundColor: theme.palette.primaryBlack,
      color: theme.palette.primaryWhite,
      padding: "8px 32px",
      height: "40px",
      marginTop: theme.spacing(8),
      textTransform: "capitalize",
      [theme.breakpoints.down('sm')]: {
        fontSize: "13px",
        padding: "0 3px",
        marginTop: "0"
      }
    },
  },
}));

const RegisterationConfirmation = ({
  appointmentDetails,
  isAppointment = false,
  onSubmit,
}) => {
  const dispatch = useDispatch();
  console.log(appointmentDetails, "details");
  const [isAabhaDisabled, setIsAabhaDisabled] = useState(false);
  const dataState = useSelector((state) => state);
  const doctorId = sessionStorage.getItem("appointment_doctor_id");
  const selectedPatient = dataState?.appointmentList?.patientDetails;
  const registeredPatient =
    dataState.PatientRegistartion.registeredPatientDetails;
  const patientData =
    Object.keys(selectedPatient)?.length > 0 && isAppointment
      ? selectedPatient
      : registeredPatient;
  const [data, setData] = useState([]);
  const navigate = useNavigate();
  const currentPatient = JSON.parse(sessionStorage.getItem("selectedPatient"));
  
  useEffect(() => {
    let pageData = [
      { key: "Patient Name", value: patientData?.name || "-" },
      {
        key: "Patient Id",
        value: patientData?.id || currentPatient?.id || "-",
      },
      { key: "Gender", value: patientData?.gender || currentPatient?.gender || "-" },
      { key: "Date Of Birth", value: patientData?.DOB || currentPatient?.DOB || "-" },
      { key: "Email Address", value: patientData?.email || "-" },
      { key: "AABHA Address", value: patientData?.abha_address || currentPatient?.abha_address || "-" },
    ];
    if (isAppointment) {
      const appointmentData = [
        { key: "Appointment Type", value: appointmentDetails?.appointmentType },
        { key: "Encounter Type", value: appointmentDetails?.encounterType },
        { key: " Visit Type", value: appointmentDetails?.visitType },
        {
          key: "Billing Type",
          value: appointmentDetails?.billingType,
        },
      ];

      pageData = [...pageData, ...appointmentData];
    }

    setData(pageData);
  }, [patientData]);

  const downloadAbha = () => {
      console.log("Downloading Aabha");
      setIsAabhaDisabled(true);
      dispatch(downloadAabha({patientId: patientData.id})).then((res) => {
        setIsAabhaDisabled(false);
        if (res?.error && Object.keys(res?.error)?.length > 0) {
          console.log("Download Aabha failed");
          return;
        }
        else {
          const abha_url = res?.payload.abha_url;
          window.location.replace(abha_url);
        }
      })
  }

  const navigateStartVisit = () => {
    navigate("/patient-emr");
    // sessionStorage.setItem("selectedPatient", JSON.stringify(patientData));
  }

  const navigateToNext = () => {
    if (isAppointment) {
      navigate("/appointment-list");
    } else {
      navigate("/create-appointment");
      sessionStorage.setItem(
        "selectedPatient",
        JSON.stringify(registeredPatient)
      );
    }
  };
  return (
    <RegisterationConfirmationWrapper>
      <Box padding={{ xs: 6, md: 8 }} marginTop={{ xs: 0, md: 4 }} marginBottom={4}>
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
            <Grid item key={item.key} xs={12} md={5}>
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
      <div className="btn-wrapper">
      <Button className="submit-btn" onClick={navigateStartVisit}>
          {/* {isAppointment ? "Go to appointment list" : "Create Appointment"} */}
          Start Visit
        </Button>
        <Button className="submit-btn" onClick={navigateToNext}>
          {isAppointment ? "Go to appointment list" : "Create Appointment"}
        </Button>
        <Button disabled={isAabhaDisabled} 
          style={{
                backgroundColor: isAabhaDisabled ? "#9e9e9e" : "",
              }}
          className="submit-btn" onClick={downloadAbha}>
         Download Aabha
        </Button>
      </div>
    </RegisterationConfirmationWrapper>
  );
};

export default RegisterationConfirmation;
