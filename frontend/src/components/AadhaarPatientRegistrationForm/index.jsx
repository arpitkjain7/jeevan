import React, { useState } from "react";
import { TextField, Button, Grid } from "@mui/material";
import { useDispatch } from "react-redux";
import { registerPatient } from "../../pages/PatientRegistration/PatientRegistration.slice";
import { apis } from "../../utils/apis";
import { AppointmentPageActions } from "../../pages/AppointmentPage/AppointmentPage.slice";
import { useNavigate } from "react-router-dom";
import CustomSnackbar from "../CustomSnackbar";
import { validateAbhaAddress } from "../../utils/utils";
import { format } from "date-fns";

const AadhaarPatientRegForm = ({ setUserCreated, txnId, patientAbhaData }) => {
  const [formData, setFormData] = React.useState({
    firstname: "",
    lastname: "",
    middlename: "",
    abhaAddress: "",
    email: "",
    password: "",
    dob: "",
    gender: "",
    abhaNumber: ""
  });
  const hospital = sessionStorage?.getItem("selectedHospital");
  const dispatch = useDispatch();
  const [showSnackbar, setShowSnackbar] = useState(false);
  const navigate = useNavigate();
  const [abhaAddressError, setAbhaAddressError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
    if(name == "abhaAddress"){
      if(!validateAbhaAddress(value)) {
        setAbhaAddressError(true);
      } else {
        setAbhaAddressError(false)
      }
    }
  };

  const formatDob = (date) => {
    return format(new Date(date), "yyyy-MM-dd");
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    let currentHospital = {};
    if (!validateAbhaAddress(formData.abhaAddress)) {
      setAbhaAddressError(true);
      setShowSnackbar(true);
      setErrorMessage("Invalid ABHA Address");
      return;
    }
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = Object.keys(patientAbhaData).length > 0 ? {
        firstName: patientAbhaData?.name,
        middleName: formData?.middlename,
        lastName: formData?.lastname,
        email: formData?.email,
        healthId: patientAbhaData?.preferredAbhaAddress,
        password: formData?.password,
        dob: patientAbhaData?.dob,
        gender: patientAbhaData?.gender,
        abhaNumber: patientAbhaData?.ABHANumber,
        hip_id: currentHospital?.hip_id,
        txnId: txnId,
      } : {
        firstName: formData?.firstname,
        middleName: formData?.middlename,
        lastName: formData?.lastname,
        email: formData?.email,
        healthId: formData?.abhaAddress,
        password: formData?.password,
        dob: formData?.dob,
        gender: formData?.gender,
        abhaNumber: formData?.abhaNumber,
        hip_id: currentHospital?.hip_id,
        txnId: txnId,
      }
      dispatch(
        registerPatient({ payload, url: apis?.registerAadhaarPaient })
      ).then((res) => {
        if (res?.error && Object.keys(res?.error)?.length > 0) {
          setShowSnackbar(true);
          return;
        }
        const userDetails = Object.keys(patientAbhaData).length > 0 ? {
          name: patientAbhaData?.name || "",
          email: formData?.email,
          gender: formData?.gender,
          healthId: patientAbhaData?.preferredAbhaAddress || "",
          dob: patientAbhaData?.dob,
          gender: patientAbhaData?.gender,
          abhaNumber: patientAbhaData?.ABHANumber,
          password: formData?.password,
          hip_id: currentHospital?.hip_id,
        } : {
          name: formData?.firstname + " " + formData?.lastname,
          email: formData?.email,
          gender: formData?.gender,
          healthId: formData.abhaAddress,
          dob: formData?.dob,
          gender: formData?.gender,
          abhaNumber: formData?.abhaNumber,
          password: formData?.password,
          hip_id: currentHospital?.hip_id,
        };
        setUserCreated(true);
        dispatch(AppointmentPageActions.setSelectedPatientData(userDetails));
        navigate("/registered-patient");
      });
    }
  };

  // const formatDob = (date) => {
  //   return format(new Date(date), "yyyy-MM-dd");
  // };

  const onSnackbarClose = () => {
    setShowSnackbar(false);
  };
  return (
    Object.keys(patientAbhaData).length > 0 ? (
      <form onSubmit={handleSubmit}>
        <CustomSnackbar
          message={errorMessage || "Something went wrong"}
          open={showSnackbar}
          status={"error"}
          onClose={onSnackbarClose}
        />
        <Grid container spacing={2}>
          <Grid item xs={12} md={5}>
            <TextField
              label="First Name"
              name="firstname"
              value={patientAbhaData?.name}
              onChange={handleChange}
              disabled
              required
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Middle Name"
              name="middlename"
              value={formData.middlename}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Last Name"
              name="lastname"
              value={formData.lastname}
              onChange={handleChange}
              required
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Email Address"
              name="email"
              value={formData.email}
              onChange={handleChange}
              type="email"
              // required
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="DOB"
              name="dob"
              value={patientAbhaData?.dob}
              onChange={handleChange}
              disabled
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Gender"
              name="gender"
              value={patientAbhaData?.gender}
              onChange={handleChange}
              disabled
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="ABHA number"
              name="abhaNumber"
              value={patientAbhaData?.ABHANumber}
              onChange={handleChange}
              disabled
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="ABHA Address"
              name="abhaAddress"
              error={abhaAddressError}
              value={patientAbhaData?.preferredAbhaAddress}
              onChange={handleChange}
              disabled
              required
              InputLabelProps={{ shrink: true }}
              fullWidth
              helperText={abhaAddressError ? "Your ABHA Address must be 8-18 characters long, alphanumeric, and can include up to one dot (.) and/or one underscore (_) which cannot be at the beginning or end of the address" : ""}
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              type="password"
              required
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
        </Grid>
        <Grid container spacing={2}>
          <Grid item xs={5}></Grid>
          <Grid item xs={12} md={5}>
            <Button variant="contained" color="primary" type="submit" InputLabelProps={{ shrink: true }}
            fullWidth>
              Submit
            </Button>
          </Grid>
        </Grid>
      </form>
    ) : (
      <form onSubmit={handleSubmit}>
      <CustomSnackbar
        message={errorMessage || "Something went wrong"}
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
      <Grid container spacing={2}>
        <Grid item xs={12} md={5}>
          <TextField
            label="First Name"
            name="firstname"
            value={formData.firstname}
            onChange={handleChange}
            required
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="Middle Name"
            name="middlename"
            value={formData.middlename}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="Last Name"
            name="lastname"
            value={formData.lastname}
            onChange={handleChange}
            required
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="Email Address"
            name="email"
            value={formData.email}
            onChange={handleChange}
            type="email"
            // required
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="DOB"
            name="dob"
            value={formData?.dob}
            onChange={handleChange}
            type="date"
            inputProps={{
              max: formatDob(new Date()), // Set max date to the current date
            }}
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="Gender"
            name="gender"
            value={formData?.gender}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="ABHA number"
            name="abhaNumber"
            value={formData?.abhaNumber}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="ABHA Address"
            name="abhaAddress"
            error={abhaAddressError}
            value={formData.abhaAddress}
            onChange={handleChange}
            required
            InputLabelProps={{ shrink: true }}
            fullWidth
            helperText={abhaAddressError ? "Your ABHA Address must be 8-18 characters long, alphanumeric, and can include up to one dot (.) and/or one underscore (_) which cannot be at the beginning or end of the address" : ""}
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="Password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            type="password"
            required
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
      </Grid>
      <Grid container spacing={2}>
        <Grid item xs={5}></Grid>
        <Grid item xs={12} md={5}>
          <Button variant="contained" color="primary" type="submit" fullWidth>
            Submit
          </Button>
        </Grid>
      </Grid>
    </form>
    )
  );
};

export default AadhaarPatientRegForm;
