import React, { useState } from "react";
import { TextField, Button, Grid, Autocomplete, FormControlLabel, FormGroup, Checkbox } from "@mui/material";
import { useDispatch } from "react-redux";
import { createAbhaAddress, registerAbhaPatient, registerPatient } from "../../pages/PatientRegistration/PatientRegistration.slice";
import { AppointmentPageActions } from "../../pages/AppointmentPage/AppointmentPage.slice";
import { useNavigate } from "react-router-dom";
import CustomSnackbar from "../CustomSnackbar";
import { validateAbhaAddress } from "../../utils/utils";
import { format } from "date-fns";

const AadhaarPatientRegForm = ({ 
  setUserCreated, 
  txnId, 
  patientAbhaData, 
  abhaSuggestionList, 
  abhaSuggestionTxnId,
  selectedAbhaModeOption,
  patientAbhaToken,
  abhaNewMobile
 }) => {
  const [formData, setFormData] = useState({
    firstname: "",
    lastname: "",
    middlename: "",
    abhaNumber: "",
    abhaAddress: "",
    email: "",
    mobile: "",
    dob: "",
    gender: "M",
    address: "",
    pincode: "",
  });
  const hospital = sessionStorage?.getItem("selectedHospital");
  const dispatch = useDispatch();
  const [showSnackbar, setShowSnackbar] = useState(false);
  const navigate = useNavigate();
  const [abhaAddressError, setAbhaAddressError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [abhaAddressInputValue, setAbhaAddressInputValue] = useState("");
  // let combinedAbhaSuggestions = (abhaSuggestionList).concat(patientAbhaData?.phrAddress || []);
  let abhaSuggestions = patientAbhaData?.phrAddress || [];
  const [abhaAddressValue, setAbhaAddressValue] = useState(abhaSuggestions[0] || "");
  const [isNewAbha, setIsNewAbha] = useState(false);
  const [patientAddress, setPatientAddress] = useState(patientAbhaData?.address?.line ? (patientAbhaData?.address?.line !== null ? patientAbhaData?.address?.line + " " + patientAbhaData?.address?.district + " " + patientAbhaData?.address?.state : " ") : patientAbhaData?.address);
  const [patientPincode, setPatientPincode] = useState(patientAbhaData?.pinCode || patientAbhaData?.pincode || patientAbhaData?.address?.pincode || "");

  const handleNewAbhaChange = (event) => {
    setIsNewAbha(event.target.checked);
    setAbhaAddressValue("");
  };
  const handleChange = (event) => {
    const { name, value } = event.target;
    if(name === "address"){
      setPatientAddress(value);
    } else if(name === "pincode"){
      setPatientPincode(value);
    }
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
    console.log(newInputValue, event);
    if(!validateAbhaAddress(newInputValue)) {
      setAbhaAddressError(true);
    } else {
      setAbhaAddressError(false);
      setAbhaAddressValue(newInputValue);
    }
  }

  const handleExsistingAbha = (event, newValue) => {
    console.log(newValue);
    if(validateAbhaAddress(newValue))
      setAbhaAddressValue(newValue);
  }

  const handleExsistingAbhaInput = (event, newValue) => {
    console.log(newValue);
    if(validateAbhaAddress(newValue))
      setAbhaAddressValue(newValue);
  }

  const formatDob = (date) => {
    return format(new Date(date), "yyyy-MM-dd");
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    let currentHospital = {};
    console.log(abhaAddressValue, "abhaAddressValue");
    if(Object.keys(patientAbhaData).length > 0){
      if (selectedAbhaModeOption === "create_abha" && !validateAbhaAddress(abhaAddressValue)) {
        setAbhaAddressError(true);
        setShowSnackbar(true);
        setErrorMessage("Invalid ABHA Address");
        return;
      }
    } 
    // else {
    //   if (!validateAbhaAddress(formData.abhaAddress)) {
    //     setAbhaAddressError(true);
    //     setShowSnackbar(true);
    //     setErrorMessage("Invalid ABHA Address");
    //     return;
    //   }
    // }
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      if(Object.keys(patientAbhaData).length > 0){
        const payload = {
          name: patientAbhaData?.name || patientAbhaData?.firstName + " " + patientAbhaData?.middleName + " " + patientAbhaData?.lastName,
          email: patientAbhaData?.email,
          mobile_number: abhaNewMobile || patientAbhaData?.mobile || patientAbhaData?.mobile_number || patientAbhaData?.identifiers[0].value,
          abha_address: patientAbhaData?.preferredAbhaAddress || patientAbhaData?.abha_address || abhaAddressValue, // || patientAbhaData?.id,
          primary_abha_address: patientAbhaData?.preferredAbhaAddress || patientAbhaData?.abha_address || abhaAddressValue, //|| patientAbhaData?.id,
          DOB: patientAbhaData?.DOB ? format(new Date(patientAbhaData?.DOB), "dd-MM-yyyy") : ""  || patientAbhaData?.dob || `${patientAbhaData?.dayOfBirth}-${patientAbhaData?.monthOfBirth}-${patientAbhaData?.yearOfBirth}`,
          gender: patientAbhaData?.gender,
          abha_number: patientAbhaData?.ABHANumber || patientAbhaData?.abha_number || patientAbhaData?.identifiers[1].value,
          pincode: patientPincode,
          //address: patientAbhaData?.address?.line !== null ? patientAbhaData?.address?.line + " " + patientAbhaData?.address?.district + " " + patientAbhaData?.address?.state : patientAbhaData?.address?.district + " " + patientAbhaData?.address?.state || patientAbhaData?.address,
          address: patientAddress,
          state_name: patientAbhaData?.stateName || patientAbhaData?.address?.state || "",
          district_name: patientAbhaData?.districtName || patientAbhaData?.address?.district || "",
          district_code: patientAbhaData?.districtCode || "",
          hip_id: currentHospital?.hip_id,
        }
      const abhaAddressPayload = {
        abhaAddress: patientAbhaData?.preferredAbhaAddress || abhaAddressValue || formData?.abhaAddress,
        txnId: abhaSuggestionTxnId
      }
      if(isNewAbha){
        dispatch(createAbhaAddress(abhaAddressPayload)).then(result => {
          console.log("createAbhaAddress", result);
        });
      }
        dispatch(registerAbhaPatient(payload)).then((res) => {
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            setShowSnackbar(true);
            return;
          }
          const patientData = res?.payload;
          sessionStorage.setItem("selectedPatient", JSON.stringify(patientData));
          let userDetails;
          if(patientAbhaToken){
            userDetails = {
              ...patientData, 
              ...{
              id: res?.payload?.id, 
              token: patientAbhaToken
            }}
          } else {
            userDetails = {
              ...patientData, 
              ...{
              id: res?.payload?.id, 
              abhaBytes: patientAbhaData?.abha_card_bytes
            }}
          }
          setUserCreated(true);
          dispatch(AppointmentPageActions.setSelectedPatientData(userDetails));
          navigate("/registered-patient");
        });
      }
    }
  };

  const onSnackbarClose = () => {
    setShowSnackbar(false);
  };
  return (
    Object.keys(patientAbhaData).length > 0 && (
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
              value={patientAbhaData?.firstName || patientAbhaData?.name.split(" ")[0]}
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
              value={patientAbhaData?.middleName || patientAbhaData?.name.split(" ")[1]}
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
              value={patientAbhaData?.lastName || patientAbhaData?.name.split(" ")[2]}
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
              value={abhaNewMobile || patientAbhaData?.mobile || patientAbhaData?.mobile_number} //  || patientAbhaData?.identifiers[0]?.value
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
              value={patientAbhaData?.dob || patientAbhaData?.DOB || `${patientAbhaData?.dayOfBirth}-${patientAbhaData?.monthOfBirth}-${patientAbhaData?.yearOfBirth}`}
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
              value={patientAbhaData?.ABHANumber || patientAbhaData?.abha_number} // || patientAbhaData?.identifiers[1]?.value
              onChange={handleChange}
              disabled
              InputLabelProps={{ shrink: true }}
              fullWidth
            />
          </Grid>
          {selectedAbhaModeOption === "create_abha" && (
            <Grid item xs={12} md={5}>
              <FormControlLabel checked={isNewAbha} onChange={handleNewAbhaChange} control={<Checkbox />} label="Create new ABHA" />
            </Grid>
          )}
          {selectedAbhaModeOption === "create_abha" && isNewAbha && 
            <Grid item xs={12} md={5}>
              <Autocomplete
                freeSolo
                name="abhaAddress"
                id="abhaAddress"
                // error={abhaAddressError}
                value={abhaAddressValue}
                options={abhaSuggestionList}
                // onChange={(event, newValue) => {
                //   setAbhaAddressValue(newValue);
                // }}
                // inputValue={abhaAddressInputValue}
                onInputChange={abhaAddressInputChange}
                fullWidth
                renderInput={(params) => <TextField {...params} label="Abha address"
                error={abhaAddressError}
                helperText={abhaAddressError ? "Your ABHA Address must be 8-18 characters long, alphanumeric, and can include special which cannot be at the beginning or end of the address" : ""}/>}
              />
            </Grid>
          }
          {!isNewAbha && selectedAbhaModeOption === "create_abha" && 
            <Grid item xs={12} md={5}>
              <Autocomplete
                freeSolo
                name="abhaAddress"
                id="abhaAddress"
                value={abhaAddressValue}
                options={abhaSuggestions}
                onChange={handleExsistingAbha}
                onInputChange={handleExsistingAbhaInput}
                fullWidth
                renderInput={(params) => <TextField {...params} label="Abha address"
                />}
              />
            </Grid>
          }
          {selectedAbhaModeOption === "link_abha" &&
            <Grid item xs={12} md={5}>
              <TextField
                label="ABHA Address"
                name="abhaAddress"
                value={patientAbhaData?.preferredAbhaAddress || patientAbhaData[0]?.abha_address || patientAbhaData?.abha_address}
                onChange={handleChange}
                required
                disabled
                InputLabelProps={{ shrink: true }}
                fullWidth
              />
            </Grid>
          }
          <Grid item xs={12} md={5}>
            <TextField
              label="Address"
              name="address"
              value={patientAddress}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              fullWidth
            /> 
          </Grid>
          <Grid item xs={12} md={5}>
            <TextField
              label="Pincode"
              name="pincode"
              value={patientPincode}
              onChange={handleChange}
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
    // : (
    //   <form onSubmit={handleSubmit}>
    //   <CustomSnackbar
    //     message={errorMessage || "Something went wrong"}
    //     open={showSnackbar}
    //     status={"error"}
    //     onClose={onSnackbarClose}
    //   />
    //   <Grid container spacing={2}>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="First Name"
    //         name="firstname"
    //         value={formData.firstname}
    //         onChange={handleChange}
    //         required
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="Middle Name"
    //         name="middlename"
    //         value={formData.middlename}
    //         onChange={handleChange}
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="Last Name"
    //         name="lastname"
    //         value={formData.lastname}
    //         onChange={handleChange}
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="Email Address"
    //         name="email"
    //         value={formData.email}
    //         onChange={handleChange}
    //         type="email"
    //         // required
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="Mobile Number"
    //         name="mobile"
    //         value={formData.mobile}
    //         onChange={handleChange}
    //         type="tel"
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="DOB"
    //         name="dob"
    //         value={formData?.dob}
    //         onChange={handleChange}
    //         type="date"
    //         inputProps={{
    //           max: formatDob(new Date()), // Set max date to the current date
    //         }}
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="Gender"
    //         name="gender"
    //         value={formData?.gender}
    //         onChange={handleChange}
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="ABHA number"
    //         name="abhaNumber"
    //         value={formData?.abhaNumber}
    //         onChange={handleChange}
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="ABHA Address"
    //         name="abhaAddress"
    //         error={abhaAddressError}
    //         value={formData.abhaAddress}
    //         onChange={handleChange}
    //         required
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //         helperText={abhaAddressError ? "Your ABHA Address must be 8-18 characters long, alphanumeric, and can include up to one dot (.) and/or one underscore (_) which cannot be at the beginning or end of the address" : ""}
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="Address"
    //         name="address"
    //         value={formData.address}
    //         onChange={handleChange}
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //     <Grid item xs={12} md={5}>
    //       <TextField
    //         label="Pincode"
    //         name="pincode"
    //         value={formData.pincode}
    //         onChange={handleChange}
    //         InputLabelProps={{ shrink: true }}
    //         fullWidth
    //       />
    //     </Grid>
    //   </Grid>
    //   <Grid container spacing={2}>
    //     <Grid item xs={5}></Grid>
    //     <Grid item xs={12} md={5}>
    //       <Button variant="contained" color="primary" type="submit" fullWidth>
    //         Submit
    //       </Button>
    //     </Grid>
    //   </Grid>
    // </form>
    // )
  );
};

export default AadhaarPatientRegForm;
