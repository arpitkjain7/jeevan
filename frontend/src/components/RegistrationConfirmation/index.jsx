import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  Grid,
  styled,
  Button,
  Modal,
  FormControl,
  Select,
  MenuItem,
} from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { downloadAabha } from "../../pages/PatientRegistration/PatientRegistration.slice";
import { fetchDoctorList } from "../AppointmentForm/AppointmentForm.slice";
import { createAppointment } from "../ScheduleAppointment/scheduleAppointment.slice";
import { getEMRId } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";

const RegisterationConfirmationWrapper = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    marginTop: theme.spacing(8),
    [theme.breakpoints.down("sm")]: {
      margin: "8px",
    },
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
    gap: theme.spacing(4),
    marginBottom: theme.spacing(6),
  },
  ".btn-wrapper": {
    [theme.breakpoints.down("sm")]: {
      display: "flex",
      justifyContent: "space-around",
      gap: theme.spacing(2),
    },
  },
  ".submit-btn": {
    "&.MuiButtonBase-root": {
      display: "flex",
      float: "right",
      justifyContent: "center",
      alignItems: "center",
      marginRight: theme.spacing(4),
      padding: "8px 32px",
      height: "40px",
      marginTop: theme.spacing(8),
      textTransform: "capitalize",
      "&": theme.typography.tertiaryButton,
      [theme.breakpoints.down("sm")]: {
        fontSize: "13px",
        padding: "0 3px",
        marginTop: "0",
        marginRight: theme.spacing(2),
      },
    },
  },
  ".visit-btn": {
    "&.MuiButtonBase-root": {
      display: "flex",
      float: "right",
      justifyContent: "center",
      alignItems: "center",
      padding: "8px 32px",
      height: "40px",
      marginTop: theme.spacing(8),
      textTransform: "capitalize",
      "&": theme.typography.tertiaryButton,
      [theme.breakpoints.down("sm")]: {
        fontSize: "13px",
        padding: "0 3px",
        marginTop: "0",
        marginRight: theme.spacing(2),
      },
    },
  },
  ".doctorName-dd": {
    "& > .MuiFormControl-root": {
      width: "250px",
      [theme.breakpoints.down("sm")]: {
        width: "100%",
        marginBottom: "15px",
      },
    },
  },
  ".field-title": {
    "&.MuiTypography-root": theme.typography.body2,
  },
  ".submit-dr-btn": {
    marginTop: "8px !important",
    ".verification-btn": {
      "&.MuiButtonBase-root": {
        "&": theme.typography.primaryButton,
        float: "right",

        [theme.breakpoints.down("sm")]: {
          padding: "10px",
        },
      },
    },
  },
}));

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  borderRadius: "2px",
  boxShadow: 24,
  p: 4,
};
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
  const [drListPopup, setDrListPopup] = useState(false);
  const [doctorName, setDoctorName] = useState("");
  const hospital = sessionStorage?.getItem("selectedHospital");
  const [doctorList, setDoctorList] = useState([]);

  useEffect(() => {
    let pageData = [
      { key: "Patient Name", value: patientData?.name || "-" },
      {
        key: "Patient Id",
        value: patientData?.id || currentPatient?.id || "-",
      },
      {
        key: "Gender",
        value: patientData?.gender || currentPatient?.gender || "-",
      },
      {
        key: "Date Of Birth",
        value: patientData?.DOB || currentPatient?.DOB || "-",
      },
      { key: "Email Address", value: patientData?.email || "-" },
      {
        key: "AABHA Address",
        value: patientData?.abha_address || currentPatient?.abha_address || "-",
      },
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
    dispatch(downloadAabha({ patientId: patientData.id })).then((res) => {
      setIsAabhaDisabled(false);
      if (res?.error && Object.keys(res?.error)?.length > 0) {
        console.log("Download Aabha failed");
        return;
      } else {
        const abha_url = res?.payload.abha_url;
        window.location.replace(abha_url);
      }
    });
  };

  const navigateStartVisit = () => {
    let currentHospital = {};
    if (!isAppointment) {
      if (hospital) {
        currentHospital = JSON.parse(hospital);
        const payload = {
          hip_id: currentHospital?.hip_id,
        };

        dispatch(fetchDoctorList(payload)).then((res) => {
          const doctorData = res.payload;
          let drList = [];
          doctorData?.map((item) => {
            const data = {
              label: item?.doc_name,
              value: item?.id,
            };

            drList?.push(data);
          });
          setDoctorList(drList);
        });
      }
      setDrListPopup(true);
    } else {
      navigate("/patient-emr");
    }
  };

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
  const handleCloseDrPopup = () => {
    setDrListPopup(false);
  };
  const handleDoctorNameChange = (event) => {
    setDoctorName(event.target.value);
  };

  const currentDateAndTime = () => {
    const currentDatetime = new Date();
    const year = currentDatetime.getFullYear();
    const month = String(currentDatetime.getMonth() + 1).padStart(2, "0"); // Month is zero-indexed
    const day = String(currentDatetime.getDate()).padStart(2, "0");
    const hours = String(currentDatetime.getHours()).padStart(2, "0");
    const minutes = String(currentDatetime.getMinutes()).padStart(2, "0");
    const formattedDatetime = `${year}-${month}-${day} ${hours}:${minutes}`;
    return formattedDatetime;
  };
  const handleDrSubmit = () => {
    sessionStorage.setItem("doctorId", doctorName);
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = {
        doc_id: doctorName,
        patient_id: patientData?.id,
        appointment_type: "first visit",
        encounter_type: "emergency",
        hip_id: currentHospital?.hip_id,
        appointment_start: currentDateAndTime(),
        appointment_end: currentDateAndTime(),
      };
      dispatch(createAppointment(payload)).then((res) => {
        if (res.payload?.appointment_id) {
          console.log(res.payload, "RESPONSE");
          const emrPayload = {
            patient_id: patientData?.id,
            doc_id: doctorName,
            appointment_id: res.payload?.appointment_id,
            hip_id: currentHospital?.hip_id,
            consultation_status: "InProgress",
          };
          dispatch(getEMRId(emrPayload)).then((res) => {
            sessionStorage.setItem("pmrID", res.payload?.pmr_details.id);
            navigate("/patient-emr");
          });
        }
      });
    }

    handleCloseDrPopup();
  };
  return (
    <RegisterationConfirmationWrapper>
      <Modal
        open={drListPopup}
        onClose={handleCloseDrPopup}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography id="modal-modal-title" variant="h3">
            Select Doctor
          </Typography>
          <Typography id="modal-modal-description" sx={{ mt: 2 }}></Typography>
          <div className="doctorName-dd">
            <Typography className="field-title">Doctor Name</Typography>
            <FormControl sx={{ width: "60%", marginTop: "8px" }}>
              <Select
                value={doctorName}
                onChange={handleDoctorNameChange}
                placeholder="Doctor Name"
              >
                {doctorList?.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option?.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </div>
          <div className="submit-dr-btn">
            <Button
              disabled={!doctorName}
              onClick={() => handleDrSubmit()}
              variant="contained"
              className="verification-btn"
            >
              Submit
            </Button>
          </div>
        </Box>
      </Modal>
      <Box
        padding={{ xs: 6, md: 8 }}
        marginTop={{ xs: 0, md: 4 }}
        marginBottom={4}
      >
        <div className="registration-success-header">
          <Typography
            variant="h6"
            color="primary"
            gutterBottom
            className="registration-success-text"
          >
            Success
          </Typography>
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
        <Button className="visit-btn" onClick={navigateStartVisit}>
          {/* {isAppointment ? "Go to appointment list" : "Create Appointment"} */}
          Start Visit
        </Button>
        <Button className="submit-btn" onClick={navigateToNext}>
          {isAppointment ? "Go to appointment list" : "Create Appointment"}
        </Button>
        <Button
          disabled={isAabhaDisabled}
          style={{
            backgroundColor: isAabhaDisabled ? "#9e9e9e" : "",
          }}
          className="submit-btn"
          onClick={downloadAbha}
        >
          Download Aabha
        </Button>
      </div>
    </RegisterationConfirmationWrapper>
  );
};

export default RegisterationConfirmation;
