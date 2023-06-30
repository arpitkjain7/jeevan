import React from "react";
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
import { format } from "date-fns";
import { useDispatch } from "react-redux";
import { registerPatient } from "../../pages/PatientRegistration/PatientRegistration.slice";

const PatientRegistartionForm = ({setUserCreated}) => {
  const [formData, setFormData] = React.useState({
    firstname: "",
    lastname: "",
    middlename: "",
    gender: "",
    dob: "",
    mobile: "",
    email: "",
  });
  const hospital = localStorage?.getItem("selectedHospital");
  const dispatch = useDispatch();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    let currentHospital = {};

    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = {
        name:
          formData?.firstname +
          " " +
          formData?.middlename +
          " " +
          formData?.lastname,
        gender: formData?.gender,
        DOB: formData?.dob,
        mobile_number: formData?.mobile,
        hip_id: currentHospital?.hip_id,
      };
      console.log(payload);
      dispatch(registerPatient(payload)).then(res=>{
        console.log(res.payload)
        setUserCreated(true);
      });
    }
  };

  const formatDob = (date) => {
    return format(new Date(date), "yyyy-MM-dd");
  };

  return (
    <form onSubmit={handleSubmit}>
      <Grid container spacing={2}>
        <Grid item xs={5}>
          <TextField
            placeholder="First Name"
            name="firstname"
            value={formData.firstname}
            onChange={handleChange}
            required
            fullWidth
          />
        </Grid>
        <Grid item xs={5}>
          <TextField
            placeholder="Last Name"
            name="lastname"
            value={formData.lastname}
            onChange={handleChange}
            required
            fullWidth
          />
        </Grid>
        <Grid item xs={5}>
          <TextField
            placeholder="Date of Birth"
            name="dob"
            value={formData.dob}
            onChange={handleChange}
            type="date"
            inputProps={{
              max: formatDob(new Date()), // Set max date to the current date
            }}
            required
            fullWidth
          />
        </Grid>
        <Grid item xs={5}>
          <TextField
            placeholder="Mobile Number"
            name="mobile"
            value={formData.mobile}
            onChange={handleChange}
            required
            fullWidth
          />
        </Grid>
        <Grid item xs={5}>
          <TextField
            placeholder="Middle Name"
            name="middlename"
            value={formData.middlename}
            onChange={handleChange}
            fullWidth
          />
        </Grid>
        <Grid item xs={5}>
          <FormControl component="fieldset">
            <FormLabel component="legend">Gender</FormLabel>
            <RadioGroup
              aria-label="gender"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
            >
              <Grid>
                <FormControlLabel
                  value="male"
                  control={<Radio />}
                  label="Male"
                />
                <FormControlLabel
                  value="female"
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
        <Grid item xs={5}>
          <TextField
            placeholder="Email Address"
            name="email"
            value={formData.email}
            onChange={handleChange}
            type="email"
            required
            fullWidth
          />
        </Grid>
      </Grid>
      <Grid container spacing={2}>
        <Grid item xs={5}></Grid>
        <Grid item xs={5}>
          <Button variant="contained" color="primary" type="submit" fullWidth>
            Submit
          </Button>
        </Grid>
      </Grid>
    </form>
  );
};

export default PatientRegistartionForm;
