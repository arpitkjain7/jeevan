import React, { useState } from "react";
import Modal from "@mui/material/Modal";
import {
  TextField,
  Select,
  MenuItem,
  Button,
  Grid,
  FormControl,
  InputLabel,
} from "@mui/material";
import { styled } from "@mui/material/styles";

const ModalContainer = styled("div")({
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  backgroundColor: "white",
  padding: "20px",
  borderRadius: "8px",
  outline: "none",
  width: "40%",
});

const Form = styled("form")({
  margin: "0 auto",
});

const FormRow = styled("div")({
  marginBottom: "20px",
});

const ConsentModal = ({
  open,
  handleClose,
  purposeOptions,
  infoTypeOptions,
}) => {
  const [formData, setFormData] = useState({
    patientIdentifier: "",
    purposeOfRequest: "",
    healthInfoFromDate: "",
    healthInfoToDate: "",
    healthInfoType: "",
    consentExpiryDate: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add your submit logic here
    console.log(formData);
  };

  return (
    <Modal open={open} onClose={handleClose}>
      <ModalContainer>
        <Form onSubmit={handleSubmit}>
          <Grid container spacing={4} sx={{ marginBottom: "16px" }}>
            <Grid item xs={6}>
              <TextField
                label="Patient Identifier"
                fullWidth
                name="patientIdentifier"
                value={formData.patientIdentifier}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Purpose of Request</InputLabel>
                <Select
                  name="purposeOfRequest"
                  value={formData.purposeOfRequest}
                  onChange={handleChange}
                >
                  {purposeOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
          <Grid container spacing={4} sx={{ marginBottom: "16px" }}>
            <Grid item xs={6}>
              <TextField
                label="Health Info From Date"
                fullWidth
                type="date"
                name="healthInfoFromDate"
                value={formData.healthInfoFromDate}
                onChange={handleChange}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="Health Info To Date"
                fullWidth
                type="date"
                name="healthInfoToDate"
                value={formData.healthInfoToDate}
                onChange={handleChange}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
          </Grid>
          <Grid container spacing={4} sx={{ marginBottom: "16px" }}>
            <Grid item xs={6}>
              {" "}
              <FormControl fullWidth>
                <InputLabel>Health Info Type</InputLabel>
                <Select
                  name="healthInfoType"
                  value={formData.healthInfoType}
                  onChange={handleChange}
                >
                  {infoTypeOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              {" "}
              <TextField
                label="Consent Expiry Date"
                fullWidth
                type="date"
                name="consentExpiryDate"
                value={formData.consentExpiryDate}
                onChange={handleChange}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
          </Grid>
          <Button variant="contained" color="primary" type="submit">
            Submit
          </Button>
        </Form>
      </ModalContainer>
    </Modal>
  );
};

export default ConsentModal;
