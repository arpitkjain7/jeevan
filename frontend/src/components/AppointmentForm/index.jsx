import React, { useEffect } from "react";
import {
  Button,
  Card,
  CardContent,
  FormControl,
  FormControlLabel,
  Grid,
  MenuItem,
  Radio,
  RadioGroup,
  Select,
  Typography,
  styled,
} from "@mui/material";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchDoctorList } from "./AppointmentForm.slice";
import {
  appointmentType,
  billingType,
  encounterType,
  visitType,
} from "./constant";
import { ScheduleAppointmentActions } from "../ScheduleAppointment/scheduleAppointment.slice";

const AppointmentFormWrapper = styled("div")(({ theme }) => ({
  "&": {},
  ".doctorName-dd": {
    "& > .MuiFormControl-root": {
      width: "250px",
      [theme.breakpoints.down('sm')]: {
        width: "100%",
        marginBottom: "15px"
      },
    },
  },
  ".appointmentForm-details-key": {
    "&.MuiTypography-root": theme.typography.body2,
  },
  ".appointmentForm-details-value": {
    "&.MuiTypography-root": theme.typography.body3,
  },
  ".field-title": {
    "&.MuiTypography-root": theme.typography.body2,
  },
  ".btn-wrapper": {
    [theme.breakpoints.down('sm')]: {
      display: "flex",
      justifyContent: "center",
    }
  },
  ".submit-btn": {
    "&": theme.typography.primaryButton,
    "&:hover": {
      backgroundColor: "#0089e999",
    },
    float: "right",
    marginTop: theme.spacing(8),
    marginBottom: "10px",
    [theme.breakpoints.down('sm')]: {
      marginTop: theme.spacing(5),
    }
  },
}));

const StyledCard = styled(Card)({
  minWidth: 275,
  marginTop: "24px",
});

const StyledCardContent = styled(CardContent)(({ theme }) => ({
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  rowGap: "32px",
  [theme.breakpoints.down('sm')]: {
    display: "block",
  },
}));

const RadioFormControl = styled("div")(({ theme }) =>({
  display: "flex",
  alignItems: "center",
  [theme.breakpoints.down('sm')]: {
    marginBottom: "15px"
  },
  ".MuiFormGroup-root": {
    [theme.breakpoints.down('sm')]: {
      justifyContent: "space-between"
    },
  }
}));

function AppointmentForm(props) {
  const [doctorName, setDoctorName] = useState("" || sessionStorage.getItem("doctorName"));
  const [encounterTypeValue, setEncounterTypeValue] = useState("" || sessionStorage.getItem("encounterTypeValue"));
  const [appointmentTypeValue, setAppointmentTypeValue] = useState("" || sessionStorage.getItem("appointmentTypeValue"));
  const [visitTypeValue, setVisitTypeValue] = useState("" || sessionStorage.getItem("visitTypeValue"));
  const [billingTypeValue, setBillingTypeValue] = useState("" || sessionStorage.getItem("billingTypeValue"));
  const dispatch = useDispatch();
  const hospital = sessionStorage?.getItem("selectedHospital");
  const [doctorList, setDoctorList] = useState([]);
  const [showLoader, setShowLoader] = useState(false);
  // const dataState = useSelector((state) => state);
  const selectedPatient = JSON.parse(
    sessionStorage?.getItem("selectedPatient")
  );
  const userDetails = [
    {
      label: "Name",
      value: selectedPatient?.name || "-",
    },
    {
      label: "Gender",
      value: selectedPatient?.gender || "-",
    },
    {
      label: "Date of Birth",
      value: selectedPatient?.DOB || "-",
    },
    {
      label: "Email ID",
      value: selectedPatient?.email || "-",
    },
  ];

  const handleDoctorNameChange = (event) => {
    sessionStorage.setItem("doctorName", event?.target?.value);
    setDoctorName(event.target.value);
  };

  useEffect(() => {
    setShowLoader(true);
    let currentHospital = {};

    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = {
        hip_id: currentHospital?.hip_id,
      };

      dispatch(fetchDoctorList(payload)).then((res) => {
        setShowLoader(false);
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
  }, []);

  const handleEncounterTypeChange = (event) => {
    sessionStorage.setItem("encounterTypeValue", event?.target?.value);
    setEncounterTypeValue(event?.target?.value);
  };

  const handleVisitTypeChange = (event) => {
    sessionStorage.setItem("visitTypeValue", event?.target?.value);
    setVisitTypeValue(event?.target?.value);
  };

  const handleBillingTypeChange = (event) => {
    sessionStorage.setItem("billingTypeValue", event?.target?.value);
    setBillingTypeValue(event?.target?.value);
  };

  const handleAppointmentChange = (event) => {
    sessionStorage.setItem("appointmentTypeValue", event?.target?.value);
    setAppointmentTypeValue(event?.target?.value);
  };

  const handleSubmit = () => {
    sessionStorage.setItem("appointment_doctor_id", doctorName);
    const data = {
      doctorId: doctorName,
      appointmentType: appointmentTypeValue,
      encounterType: encounterTypeValue,
      visitType: visitTypeValue,
      billingType: billingTypeValue,
    };
    dispatch(ScheduleAppointmentActions.setAppointmentDetails(data));
    props?.setTab(1);
    props?.setCompleted(true);
  };

  return (
    <AppointmentFormWrapper>
      <StyledCard>
        <CardContent>
          <Grid container>
            {userDetails?.map((pair, index) => (
              <Grid item xs={6} md={3}>
                <Typography className="appointmentForm-details-key">
                  {pair.label}
                </Typography>
                <Typography className="appointmentForm-details-value">
                  {pair.value}
                </Typography>
              </Grid>
            ))}
          </Grid>
        </CardContent>
        {/* <PatientDetailsHeader /> */}
      </StyledCard>
      <StyledCard>
        <StyledCardContent>
          <div className="doctorName-dd">
            <Typography className="field-title">Doctor Name</Typography>
            <FormControl>
              <Select
                value={doctorName}
                onChange={handleDoctorNameChange}
                placeholder="Doctor Name"
              >
                {doctorList?.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </div>
          <div className="doctorName-dd">
            <Typography className="field-title">Appointment Type</Typography>
            <FormControl>
              <Select
                value={appointmentTypeValue}
                onChange={handleAppointmentChange}
                placeholder="Appointment Type"
              >
                {appointmentType?.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </div>
          <div className="doctorName-dd">
            <Typography className="field-title">Encounter Type</Typography>
            <FormControl>
              <FormControl>
                <Select
                  value={encounterTypeValue}
                  onChange={handleEncounterTypeChange}
                  placeholder="Encounter Type"
                >
                  {encounterType?.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </FormControl>
          </div>
          <div className="">
            <Typography className="field-title">Visit Type</Typography>
            <FormControl>
              <RadioFormControl component="fieldset">
                <RadioGroup 
                  row
                  value={visitTypeValue}
                  onChange={handleVisitTypeChange}
                >
                  {visitType?.map((option) => (
                    <FormControlLabel
                      key={option.value}
                      value={option.value}
                      control={<Radio />}
                      label={option.label}
                    />
                  ))}
                </RadioGroup>
              </RadioFormControl>
            </FormControl>
          </div>
          <div className="">
            <Typography className="field-title">Billing Type</Typography>
            <FormControl>
              <RadioFormControl component="fieldset">
                <RadioGroup
                  row
                  value={billingTypeValue}
                  onChange={handleBillingTypeChange}
                >
                  {billingType?.map((option) => (
                    <FormControlLabel
                      key={option.value}
                      value={option.value}
                      control={<Radio />}
                      label={option.label}
                    />
                  ))}
                </RadioGroup>
              </RadioFormControl>
            </FormControl>
          </div>
        </StyledCardContent>
      </StyledCard>
      <div className="btn-wrapper">
        <Button className="submit-btn" onClick={handleSubmit}>
          Save & Next
        </Button>
      </div>
    </AppointmentFormWrapper>
  );
}

export default AppointmentForm;
