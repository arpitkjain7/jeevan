import { useState } from "react";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import { TextField, Typography, Grid } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { red } from "@mui/material/colors";
import { useSelector } from "react-redux";

export default function BackDropDash() {
  const [open, setOpen] = useState(true);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [isMobileError, setIsMobileError] = useState(false);

  const handleClose = () => setOpen(false);
  const handleOpen = () => setOpen(true);
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
    if (name === "mobile_number") {
      setIsMobileError(value.length !== 10);
    }
  };
  const patient = JSON.parse(sessionStorage.getItem("selectedPatient"));
  console.log(patient);

  const date = patient?.created_at
    ? patient.created_at.slice(0, 10)
    : "Not Available";

  return (
    <Backdrop
      sx={{
        color: "#fff",
        zIndex: (theme) => theme.zIndex.drawer + 1,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
      open={open}
      onClick={handleClose}
    >
      {loading ? (
        <CircularProgress color="inherit" />
      ) : (
        <Box
          sx={{
            width: "80%",
            maxWidth: 600,
            bgcolor: "background.paper",
            boxShadow: 24,
            borderRadius: 2,
            p: 4,
            overflowY: "auto",
            position: "relative",
            maxHeight: "80vh",
          }}
        >
          <Button
            onClick={handleClose}
            sx={{
              position: "absolute",
              top: 8,
              right: 8,
              color: red[500],
            }}
          >
            <CloseIcon />
          </Button>
          <Typography variant="h5" fontWeight={600} gutterBottom>
            Patient Details
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>DOB:</strong>{" "}
                {patient?.DOB ||
                  patient?.patient_details?.DOB ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Aadhaar Number:</strong>{" "}
                {patient?.aadhar_number ||
                  patient?.patient_details?.aadhar_number ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Abha Address:</strong>{" "}
                {patient?.abha_address ||
                  patient?.patient_details?.abha_address ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Abha Number:</strong>{" "}
                {patient?.abha_number ||
                  patient?.patient_details?.abha_number ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Abha S3 Location:</strong>{" "}
                {patient?.abha_s3_location ||
                  patient?.patient_details?.abha_s3_location ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Abha Status:</strong>{" "}
                {patient?.abha_status ||
                  patient?.patient_details?.abha_status ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Address:</strong>{" "}
                {patient?.address ||
                  patient?.patient_details?.address ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Age in Month:</strong>{" "}
                {patient?.age_in_months ||
                  patient?.patient_details?.age_in_months ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Age in Year:</strong>{" "}
                {patient?.age_in_years ||
                  patient?.patient_details?.age_in_years ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Created At:</strong>{" "}
                {date ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>District:</strong>{" "}
                {patient?.district ||
                  patient?.patient_details?.district ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>District Code:</strong>{" "}
                {patient?.district_code ||
                  patient?.patient_details?.district_code ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>HIP ID:</strong>{" "}
                {patient?.hip_id ||
                  patient?.patient_details?.hip_id ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Patient UID:</strong>{" "}
                {patient?.patient_uid ||
                  patient?.patient_details?.patient_uid ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Pincode:</strong>{" "}
                {patient?.pincode ||
                  patient?.patient_details?.pincode ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Primary Abha Address:</strong>{" "}
                {patient?.primary_abha_address ||
                  patient?.patient_details?.primary_abha_address ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>State Code:</strong>{" "}
                {patient?.state_code ||
                  patient?.patient_details?.state_code ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>State Name:</strong>{" "}
                {patient?.state_name ||
                  patient?.patient_details?.state_name ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Status Code:</strong>{" "}
                {patient?.status_code ||
                  patient?.patient_details?.status_code ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Town:</strong>{" "}
                {patient?.town ||
                  patient?.patient_details?.town ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Village:</strong>{" "}
                {patient?.village ||
                  patient?.patient_details?.village ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Village Code:</strong>{" "}
                {patient?.village_code ||
                  patient?.patient_details?.village_code ||
                  "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body1" color="textPrimary">
                <strong>Year of Birth:</strong>{" "}
                {patient?.year_of_birth ||
                  patient?.patient_details?.year_of_birth ||
                  "Not Available"}
              </Typography>
            </Grid>
          </Grid>
        </Box>
      )}
    </Backdrop>
  );
}
