import React, { useState } from "react";
import { TextField, Button, Grid, Autocomplete } from "@mui/material";
import { useDispatch } from "react-redux";
import { createAbhaAddress, registerAbhaPatient, registerPatient } from "../../pages/PatientRegistration/PatientRegistration.slice";
import { apis } from "../../utils/apis";
import { AppointmentPageActions } from "../../pages/AppointmentPage/AppointmentPage.slice";
import { useNavigate } from "react-router-dom";
import CustomSnackbar from "../CustomSnackbar";
import { validateAbhaAddress } from "../../utils/utils";
import { format } from "date-fns";

const AadhaarPatientRegForm = ({ setUserCreated, txnId, patientAbhaData, abhaSuggestionList, setAbhaSuggestionTxnId }) => {
  const [formData, setFormData] = React.useState({
    firstname: "",
    lastname: "",
    middlename: "",
    abhaNumber: "",
    abhaAddress: "",
    email: "",
    mobile: "",
    dob: "",
    gender: "",
    address: "",
    pincode: "",
    password: "",
  });
  const hospital = sessionStorage?.getItem("selectedHospital");
  const dispatch = useDispatch();
  const [showSnackbar, setShowSnackbar] = useState(false);
  const navigate = useNavigate();
  const [abhaAddressError, setAbhaAddressError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [abhaAddressInputValue, setAbhaAddressInputValue] = useState("");
  let combinedAbhaSuggestions = (abhaSuggestionList).concat(patientAbhaData?.phrAddress || []);
  const [abhaAddressValue, setAbhaAddressValue] = useState(combinedAbhaSuggestions[0] || "");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
    if(name === "abhaAddress"){
      if(!validateAbhaAddress(value)) {
        setAbhaAddressError(true);
      } else {
        setAbhaAddressError(false)
      }
    }
  };

  const abhaAddressInputChange = (event, newInputValue) => {
    setAbhaAddressInputValue(newInputValue);
    if(!validateAbhaAddress(newInputValue)) {
      setAbhaAddressError(true);
    } else {
      setAbhaAddressError(false)
    }
  }

  const formatDob = (date) => {
    return format(new Date(date), "yyyy-MM-dd");
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    let currentHospital = {};
    if(Object.keys(patientAbhaData).length > 0){
      if (!validateAbhaAddress(abhaAddressValue)) {
        setAbhaAddressError(true);
        setShowSnackbar(true);
        setErrorMessage("Invalid ABHA Address");
        return;
      }
    } else {
      if (!validateAbhaAddress(formData.abhaAddress)) {
        setAbhaAddressError(true);
        setShowSnackbar(true);
        setErrorMessage("Invalid ABHA Address");
        return;
      }
    }
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = Object.keys(patientAbhaData).length > 0 ? {
        name: patientAbhaData?.firstName + " " + patientAbhaData?.middleName + " " + patientAbhaData?.lastName,
        email: patientAbhaData?.email,
        mobile_number: patientAbhaData?.mobile,
        abha_address: abhaAddressValue,
        primary_abha_address: abhaAddressValue,
        password: formData?.password,
        DOB: patientAbhaData?.dob,
        gender: patientAbhaData?.gender,
        abhaNumber: patientAbhaData?.ABHANumber,
        pincode: patientAbhaData?.pinCode,
        address: patientAbhaData?.address,
        state_name: patientAbhaData?.stateName,
        district_name: patientAbhaData?.districtName,
        district_code: patientAbhaData?.districtCode,
        hip_id: currentHospital?.hip_id,
        txnId: txnId,
      } : {
        name: formData?.firstname + " " + formData?.middlename + " " + formData?.lastname,
        email: formData?.email,
        mobile_number: formData?.mobile,
        abha_address: formData?.abhaAddress,
        primary_abha_address: formData?.abhaAddress,
        password: formData?.password,
        DOB: formData?.dob,
        gender: formData?.gender,
        abhaNumber: formData?.abhaNumber,
        pincode: formData?.pincode,
        address: formData?.address,
        hip_id: currentHospital?.hip_id,
        txnId: txnId,
      }
      console.log(payload);
      const abhaAddressPayload = {
        abhaAddress: abhaAddressValue || formData?.abhaAddress,
        txnId: setAbhaSuggestionTxnId
      }
      console.log("abhaAddressPayload", abhaAddressPayload);
      dispatch(createAbhaAddress(abhaAddressPayload)).then(result => {
        console.log("createAbhaAddress", result);
        dispatch(registerAbhaPatient(payload)).then((res) => {
          console.log("register patient", res);
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            setShowSnackbar(true);
            return;
          }
          // const userDetails = Object.keys(patientAbhaData).length > 0 ? {
          //   name: patientAbhaData?.name || "",
          //   email: formData?.email,
          //   gender: formData?.gender,
          //   healthId: patientAbhaData?.preferredAbhaAddress || "",
          //   dob: patientAbhaData?.dob,
          //   gender: patientAbhaData?.gender,
          //   abhaNumber: patientAbhaData?.ABHANumber,
          //   pincode: patientAbhaData?.pincode,
          //   address: patientAbhaData?.address,
          //   password: formData?.password,
          //   hip_id: currentHospital?.hip_id,
          // } : {
          //   name: formData?.firstname + " " + formData?.lastname,
          //   email: formData?.email,
          //   gender: formData?.gender,	
          //   healthId: formData?.abhaAddress,
          //   dob: formData?.dob,
          //   gender: formData?.gender,
          //   abhaNumber: formData?.abhaNumber,
          //   pincode: formData?.pincode,
          //   address: formData?.address,
          //   password: formData?.password,
          //   hip_id: currentHospital?.hip_id,
          // };
          setUserCreated(true);
          dispatch(AppointmentPageActions.setSelectedPatientData(payload));
          navigate("/registered-patient");
        });
      });
    }
  };

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
              value={patientAbhaData?.firstName}
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
              value={patientAbhaData?.middleName}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              disabled
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Last Name"
              name="lastname"
              value={patientAbhaData?.lastName}
              onChange={handleChange}
              required
              InputLabelProps={{ shrink: true }}
              disabled
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Email Address"
              name="email"
              value={patientAbhaData?.email}
              onChange={handleChange}
              type="email"
              // required
              InputLabelProps={{ shrink: true }}
              disabled
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Mobile Number"
              name="mobile"
              value={patientAbhaData?.mobile}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              disabled
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
            {/* <TextField
              label="ABHA Address"
              name="abhaAddress"
              error={abhaAddressError}
              value={formData?.abhaAddress}
              onChange={handleChange}
              disabled
              required
              InputLabelProps={{ shrink: true }}
              fullWidth
              helperText={abhaAddressError ? "Your ABHA Address must be 8-18 characters long, alphanumeric, and can include up to one dot (.) and/or one underscore (_) which cannot be at the beginning or end of the address" : ""}
            /> */}
            <Autocomplete
              freeSolo
              name="abhaAddress"
              id="abhaAddress"
              // error={abhaAddressError}
              value={abhaAddressValue}
              options={combinedAbhaSuggestions}
              onChange={(event, newValue) => {
                setAbhaAddressValue(newValue);
              }}
              inputValue={abhaAddressInputValue}
              onInputChange={abhaAddressInputChange}
              fullWidth
              // helperText={abhaAddressError ? "Your ABHA Address must be 8-18 characters long, alphanumeric, and can include up to one dot (.) and/or one underscore (_) which cannot be at the beginning or end of the address" : ""}
              renderInput={(params) => <TextField {...params} label="Abha address"
              error={abhaAddressError}
              helperText={abhaAddressError ? "Your ABHA Address must be 8-18 characters long, alphanumeric, and can include up to one dot (.) and/or one underscore (_) which cannot be at the beginning or end of the address" : ""}/>}
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Address"
              name="address"
              value={patientAbhaData?.address}
              onChange={handleChange}
              disabled
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Pincode"
              name="pincode"
              value={patientAbhaData?.pinCode}
              onChange={handleChange}
              disabled
              InputLabelProps={{ shrink: true }}
              fullWidth
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
            label="Mobile Number"
            name="mobile"
            value={formData.mobile}
            onChange={handleChange}
            type="tel"
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
            label="Address"
            name="address"
            value={formData.address}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            fullWidth
          />
        </Grid>
        <Grid item xs={12} md={5}>
          <TextField
            label="Pincode"
            name="pincode"
            value={formData.pincode}
            onChange={handleChange}
            InputLabelProps={{ shrink: true }}
            fullWidth
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
