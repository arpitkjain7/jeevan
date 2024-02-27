import React, { useState } from "react";
import {
  TextField,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  Button,
  Grid,
} from "@mui/material";
import { differenceInYears, format } from "date-fns";
import { useDispatch } from "react-redux";
import { registerPatient } from "../../pages/PatientRegistration/PatientRegistration.slice";
import { apis } from "../../utils/apis";
import { convertDateFormat, validateAbhaAddress } from "../../utils/utils";
import { useNavigate } from "react-router";
import CustomSnackbar from "../CustomSnackbar";
import { AppointmentPageActions } from "../../pages/AppointmentPage/AppointmentPage.slice";

const PatientRegistartionForm = ({ setUserCreated, isForAbha, txnId }) => {
  const [formData, setFormData] = useState({
    firstname: "",
    lastname: "",
    middlename: "",
    gender: "",
    dob: "01-01-1900",
    age_years: "0",
    abhaAddress: "",
    email: "",
    password: "",
  });
  const [mobile, setMobile] = useState();
  const hospital = sessionStorage?.getItem("selectedHospital");
  const dispatch = useDispatch();
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [abhaAddressError, setAbhaAddressError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isMobileError, setIsMobileError] = useState(false);
  const navigate = useNavigate();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
    if(name === "dob"){  // && value !== "01-01-1900"
      const age = differenceInYears(new Date(), new Date(value));
      setFormData((prevData) => ({
        ...prevData,
        age_years: age,
      }));
    }
    if (name === "abhaAddress") {
      if (!validateAbhaAddress(value)) {
        setAbhaAddressError(true);
      } else {
        setAbhaAddressError(false);
      }
    }
  };

  const handleNumberChange = (event) => {
    console.log(event.target.value);
    const value = event.target.value;
    setMobile(value);

    let new_Number_length = value.length;
    if (new_Number_length > 10 || new_Number_length < 10) {
      // setErrorMessage("Please enter valid number")
      setIsMobileError(true);
    } else if (new_Number_length === 10) {
      setIsMobileError(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    let currentHospital = {};

    if (hospital) {
      currentHospital = JSON.parse(hospital);
      let url = "";
      let payload = {};
      if (isForAbha) {
        if (!validateAbhaAddress(formData.abhaAddress)) {
          setAbhaAddressError(true);
          setShowSnackbar(true);
          setErrorMessage("Invalid ABHA Address");
          return;
        }
        payload = {
          firstName: formData?.firstname,
          middleName: formData?.middlename,
          lastName: formData?.lastname,
          email: formData?.email,
          gender: formData?.gender,
          dob: convertDateFormat(formData?.dob, "dd-MM-yyyy"),
          age: formData.age_years,
          healthId: formData.abhaAddress,
          password: formData?.password,
          hip_id: currentHospital?.hip_id,
          txnId: txnId,
        };
        url = apis?.registerPhonePatient;
      } else {
        payload = {
          name:
            formData?.firstname +
            " " +
            formData?.middlename +
            " " +
            formData?.lastname,
          gender: formData?.gender,
          DOB: convertDateFormat(formData?.dob, "dd-MM-yyyy"),
          age: formData.age_years,
          email: formData?.email,
          mobile_number: mobile,
          hip_id: currentHospital?.hip_id,
        };
        url = apis?.registerUser;
      }
      dispatch(registerPatient({ payload, url: url })).then((res) => {
        if (res?.error && Object.keys(res?.error)?.length > 0) {
          setShowSnackbar(true);
          return;
        }
        setUserCreated(true);
        dispatch(AppointmentPageActions.setSelectedPatientData(res?.payload));
      });
      setTimeout(()=> { navigate("/registered-patient"); }, 2000);
    }
  };

  const formatDob = (date) => {
    return format(new Date(date), "yyyy-MM-dd");
  };

  const onSnackbarClose = () => {
    setShowSnackbar(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <CustomSnackbar
        message={errorMessage || "Something went wrong"}
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
      <Grid container spacing={3}>
        <Grid item xs={12} md={5}>
          <TextField
            name="firstname"
            label="First Name"
            value={formData.firstname}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            required
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            name="middlename"
            label="Middle Name"
            value={formData.middlename}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            name="lastname"
            label="Last Name"
            value={formData.lastname}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <FormControl component="fieldset">
            <FormLabel component="legend">Gender</FormLabel>
            <RadioGroup
              aria-label="gender"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
            >
              <Grid>
                <FormControlLabel value="M" control={<Radio />} label="Male" />
                <FormControlLabel
                  value="F"
                  control={<Radio />}
                  label="Female"
                />
                <FormControlLabel
                  value="other"
                  control={<Radio />}
                  label="Other"
                />
              </Grid>
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="DOB"
            name="dob"
            value={formData.dob}
            onChange={handleChange}
            type="date"
            inputProps={{
              max: formatDob(new Date()), // Set max date to the current date
            }}
            InputLabelProps={{ shrink: true }}
            style={{ width: "50%" }}
            // required
            // fullWidth
          />
          <TextField
            label="Age(in years)"
            name="age"
            value={formData.age_years}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            style={{ width: "50%" }}
            // required
            // fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="Email Address"
            name="email"
            value={formData.email}
            onChange={handleChange}
            type="email"
            InputLabelProps={{ shrink: true }}
            // required
            fullWidth
          />
        </Grid>
        {!isForAbha && (
          <Grid item xs={12} md={5}>
            <TextField
              name="mobile"
              label="Mobile Number"
              type="number"
              value={mobile}
              error={isMobileError}
              onChange={handleNumberChange}
              InputLabelProps={{ shrink: true }}
              required
              fullWidth
            />
          </Grid>
        )}
        {isForAbha && (
          <>
            <Grid item xs={12} md={5}>
              <TextField
                placeholder="Enter ABHA Address"
                name="abhaAddress"
                error={abhaAddressError}
                value={formData.abhaAddress}
                onChange={handleChange}
                InputLabelProps={{ shrink: true }}
                required
                fullWidth
                helperText={
                  abhaAddressError
                    ? "Your ABHA Address must be 8-18 characters long, alphanumeric, and can include up to one dot (.) and/or one underscore (_) which cannot be at the beginning or end of the address"
                    : ""
                }
              />
            </Grid>
            <Grid item xs={12} md={5}>
              <TextField
                placeholder="Enter Password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                type="password"
                InputLabelProps={{ shrink: true }}
                required
                fullWidth
              />
            </Grid>
          </>
        )}
      </Grid>
      <span style={{ color: "red" }}>
        {isMobileError ? "Please enter valid number" : ""}
      </span>
      <Grid container spacing={2}>
        <Grid item xs={5}></Grid>
        <Grid item xs={12} md={5}>
          <Button variant="contained" color="primary" type="submit" fullWidth>
            Submit
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

export default PatientRegistartionForm;
