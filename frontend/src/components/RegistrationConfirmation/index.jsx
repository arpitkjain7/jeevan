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
import { fetchDoctorList } from "../AppointmentForm/AppointmentForm.slice";
import { createAppointment } from "../ScheduleAppointment/scheduleAppointment.slice";
import {
  getEMRId,
  getPatientDetails,
} from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import {
  getAbhaCard,
} from "../../pages/PatientRegistration/PatientRegistration.slice";
import CustomLoader from "../CustomLoader";

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
      gap: theme.spacing(1),
    },
  },
  ".submit-btn": {
    "&.MuiButtonBase-root": {
      display: "flex",
      float: "right",
      justifyContent: "center",
      alignItems: "center",
      marginRight: "10px",
      padding: "8px 32px",
      height: "40px",
      marginTop: theme.spacing(8),
      textTransform: "capitalize",
      "&": theme.typography.tertiaryButton,
      [theme.breakpoints.down("sm")]: {
        fontSize: "13px",
        padding: "0 3px",
        margin: "0 2px",
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
      marginRight: "10px",
      marginTop: theme.spacing(8),
      textTransform: "capitalize",
      "&": theme.typography.tertiaryButton,
      [theme.breakpoints.down("sm")]: {
        fontSize: "13px",
        padding: "0 3px",
        margin: "0 2px",
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
  isAppointment, // = false
  onSubmit,
}) => {
  const dispatch = useDispatch();
  const [isAbhaPresent, setIsAbhaPresent] = useState(false);
  const [isAbhaDisabled, setIsAbhaDisabled] = useState(false);
  const dataState = useSelector((state) => state);
  const [abhaCardBytes, setAbhaCardBytes] = useState("");
  const [showLoader, setShowLoader] = useState(false);
  // const doctorId = sessionStorage.getItem("appointment_doctor_id");
  const selectedPatient = dataState?.appointmentList?.patientDetails;
  const registeredPatient =
    dataState?.PatientRegistartion.registeredPatientDetails;
  const patientData =
    Object.keys(selectedPatient)?.length > 0 // && isAppointment
      ? selectedPatient
      : registeredPatient;
  console.log(patientData);
  const [data, setData] = useState([]);
  const navigate = useNavigate();
  const currentPatient = JSON.parse(sessionStorage.getItem("selectedPatient"));
  const [drListPopup, setDrListPopup] = useState(false);
  const [doctorID, setDoctorID] = useState("");
  const [doctorName, setDoctorName] = useState("");
  const hospital = sessionStorage?.getItem("selectedHospital");
  const [doctorList, setDoctorList] = useState([]);
  useEffect(() => {
    setShowLoader(true);
    if (patientData?.id) {
      let pageData = [
        { key: "Patient Name", value: patientData?.name || "-" },
        {
          key: "Patient Id",
          value: patientData?.id || "-",
        },
        {
          key: "Gender",
          value: patientData?.gender || "-",
        },
        {
          key: "Date Of Birth",
          value: patientData?.DOB || "-",
        },
        { key: "Email Address", value: patientData?.email || "-" },
        { key: "Mobile Number", value: patientData?.mobile_number || "-" },
        {
          key: "ABHA Address",
          value: patientData?.abha_address || "-",
        },
        {
          key: "ABHA Number",
          value: patientData?.abha_number || "-",
        },
      ];
      if (isAppointment) {
        const appointmentData = [
          {
            key: "Appointment Type",
            value: appointmentDetails?.appointmentType,
          },
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
      setShowLoader(false);
    }
  }, [patientData]);

  useEffect(() => {
    if (patientData?.abhaBytes) {
      setIsAbhaPresent(true);
      setAbhaCardBytes(patientData?.abhaBytes);
    }
    // else if(patientData?.abha_address || currentPatient?.abha_address){
    // if (!isAppointment) {
    else if (patientData?.token) {
      const abhaCardPayload = {
        access_token: patientData?.token,
      };
      dispatch(getAbhaCard(abhaCardPayload)).then((res) => {
        if (res?.error) {
          return;
        } else {
          setIsAbhaPresent(true);
          setAbhaCardBytes(res?.payload?.abha_card_bytes);
        }
      });
    }
  }, []);

  const downloadAbhaCard = () => {
    console.log("Downloading ABHA");
    const blob = bytesToBlob(abhaCardBytes);
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "image.jpg";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    // setIsAbhaDisabled(true);
    // dispatch(downloadAbha({ patientId: patientData.id })).then((res) => {
    //   setIsAbhaDisabled(false);
    //   if (res?.error && Object.keys(res?.error)?.length > 0) {
    //     console.log("Download ABHA failed");
    //     return;
    //   } else {
    //     const abha_url = res?.payload.abha_url;
    //     window.location.replace(abha_url);
    //   }
    // });
  };
  const doctor_details = sessionStorage.getItem("DoctorDetails");
  // const docName = sessionStorage.getItem("doctorId");
  const navigateStartVisit = () => {
    setShowLoader(true);
    let currentHospital = {};
    if (isAppointment === true) {
      navigate("/patient-emr");
    } else {
      if (hospital) {
        currentHospital = JSON.parse(hospital);
        const payload = {
          hip_id: currentHospital?.hip_id,
        };
        dispatch(fetchDoctorList(payload)).then((res) => {
          const doctorData = res?.payload;
          if (doctorData.length > 1) {
            let drList = [];
            doctorData?.map((item) => {
              const data = {
                label: item?.doc_name,
                name: item?.doc_name,
                value: item?.id,
              };

              drList?.push(data);
            });
            setDoctorList(drList);
            setDrListPopup(true);
          } else if (doctorData.length === 1) {
            setDoctorID(doctorData[0]?.id);
            setDoctorName(doctorData[0]?.doc_name);
            handleDrSubmit(doctorData[0]?.id, doctorData[0]?.doc_name);
          } else {
            console.log("Empty doctor list");
            return;
          }
        });
        // }
      }
      setShowLoader(false);
    }
  };

  const navigateToNext = () => {
    if (isAppointment) {
      navigate("/appointment-list");
    } else {
      navigate("/create-appointment");
      // sessionStorage.setItem("selectedPatient", JSON.stringify(patientData));
    }
  };

  const navigateToList = () => {
    if (isAppointment) {
      navigate("/appointment-list");
    } else {
      navigate("/patient-list");
    }
  };

  const handleCloseDrPopup = () => {
    setDrListPopup(false);
  };
  const handleDoctorNameChange = (event, name) => {
    setDoctorID(event.target.value);
    setDoctorName(name.props.children);
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

  const currentDateEndTime = () => {
    const currentDatetime = new Date();
    const year = currentDatetime.getFullYear();
    const month = String(currentDatetime.getMonth() + 1).padStart(2, "0"); // Month is zero-indexed
    const day = String(currentDatetime.getDate()).padStart(2, "0");
    currentDatetime.setMinutes(currentDatetime.getMinutes() + 15);
    const hours = String(currentDatetime.getHours()).padStart(2, "0");
    const minutes = String(currentDatetime.getMinutes()).padStart(2, "0");
    const formattedDatetime = `${year}-${month}-${day} ${hours}:${minutes}`;
    return formattedDatetime;
  };

  const handleDrSubmit = (doctor_id, doctor_name) => {
    if (doctor_id) {
      sessionStorage.setItem("doctorId", doctor_id);
    } else sessionStorage.setItem("doctorId", doctorID);
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = {
        doc_id: doctor_id || doctorID,
        patient_id: patientData?.id,
        appointment_type: "first visit",
        encounter_type: "emergency",
        hip_id: currentHospital?.hip_id,
        appointment_start: currentDateAndTime(),
        appointment_end: currentDateEndTime(),
      };
      dispatch(createAppointment(payload)).then((res) => {
        if (res.payload?.appointment_id) {
          const emrPayload = {
            patient_id: patientData?.id,
            doc_id: doctor_id || doctorID,
            appointment_id: res.payload?.appointment_id,
            hip_id: currentHospital?.hip_id,
            consultation_status: "InProgress",
          };

          dispatch(getEMRId(emrPayload)).then((response) => {
            sessionStorage.setItem("pmrID", response.payload?.pmr_details?.id);
            dispatch(getPatientDetails(patientData?.id)).then((patientDataResponse) => {
              sessionStorage.setItem("selectedPatient", JSON.stringify(patientDataResponse?.payload));
              const patientPayload = res?.payload || {}; // Ensure res?.payload is an object

              const allPatientData = {
                ...patientPayload, // Spread existing properties if any
                patientId: response.payload?.pmr_details?.patient_id,
                doc_id: response.payload?.pmr_details?.doc_id,
                doc_name: sessionStorage.getItem("doctorName") || doctor_name || doctorName,
                hip_id: response.payload?.pmr_details?.hip_id,
                id: response.payload?.appointment_details?.id,
                age_in_years: patientPayload.age_in_years,
                age_in_months: patientPayload.age_in_months,
              };

              sessionStorage.setItem(
                "encounterDetail",
                JSON.stringify(allPatientData)
              );
            });
            setTimeout(() => navigate("/patient-emr"), 2000);
          });
        }
      });
    }

    handleCloseDrPopup();
  };

  const bytesToBlob = (bytesArray) => {
    // const byteArray = new Uint8Array(bytesArray);
    // return new Blob([byteArray], { type: 'image/jpeg' });
    const decodedByteCode = atob(bytesArray);
    const byteNumbers = new Array(decodedByteCode.length);
    for (let i = 0; i < decodedByteCode.length; i++) {
      byteNumbers[i] = decodedByteCode.charCodeAt(i);
    }
    const blobData = new Blob([new Uint8Array(byteNumbers)], {
      type: "image/jpeg",
    });
    // const pdfUrls = URL.createObjectURL(blobData);
    return blobData;
  };

  return (
    <RegisterationConfirmationWrapper>
      <CustomLoader open={showLoader} />
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
                value={doctorID}
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
              disabled={!doctorID}
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
        <Grid container spacing={4}>
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
        <Button className="visit-btn" onClick={navigateToList}>
          Save
        </Button>
        <Button className="visit-btn" onClick={navigateStartVisit}>
          Start Visit
        </Button>
        <Button className="submit-btn" onClick={navigateToNext}>
          {isAppointment ? "Go to appointment list" : "Create Appointment"}
        </Button>

        {isAbhaPresent && !isAppointment && (
          <Button
            disabled={isAbhaDisabled}
            style={{
              backgroundColor: isAbhaDisabled ? "#9e9e9e" : "",
            }}
            className="submit-btn"
            onClick={downloadAbhaCard}
          >
            Download ABHA
          </Button>
        )}
      </div>
      {isAbhaPresent && !isAppointment && (
        <embed
          style={{ width: "-webkit-fill-available" }}
          src={`data:image/jpeg;base64,${abhaCardBytes}`}
          download
        />
      )}
    </RegisterationConfirmationWrapper>
  );
};

export default RegisterationConfirmation;
