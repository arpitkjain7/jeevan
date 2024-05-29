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

  const Data = useSelector((state) => state.getPatientDetails.patientDetail);

  const onhandleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError(false);

      // Simulate API call
      // await someAPICall(formData);

      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
      setError(true);
    }
  };

  const date = Data?.created_at
    ? Data.created_at.slice(0, 10)
    : "Not Available";

  return (
    <Backdrop
      sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
      open={open}
      onClick={handleClose}
    >
      {loading ? (
        <CircularProgress color="inherit" />
      ) : (
        <Box
          height={500}
          width={500}
          my={4}
          display="flex"
          flexDirection="column"
          margin={"10px 10px"}
          gap={2}
          p={2}
          sx={{
            border: "2px solid grey",
            backgroundColor: "white",
            borderRadius: "2%",
            overflowY: "auto",
            position: "relative",
          }}
        >
          <Button
            onClick={handleClose}
            sx={{ position: "absolute", top: 8, right: 8, color: red[500] }}
          >
            <CloseIcon />
          </Button>
          <Grid container spacing={2} marginBottom={"15px"}>
            <Grid
              sx={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
              item
              xs={12}
            >
              <Typography sx={{ fontWeight: 600 }} variant="h1">
                Patient Details
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>DOB : {Data?.DOB || "Not Available"}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Aadhaar Number : {Data?.aadhar_number || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Abha Address : {Data?.abha_address || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Abha Number : {Data?.abha_number || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Abha S3 Location : {Data?.abha_s3_location || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Abha Status : {Data?.abha_status || "Not Available"}
              </Typography>
            </Grid>

            <Grid item xs={6}>
              <Typography>
                Address : {Data?.address || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Age in Month : {Data?.age_in_months || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Age in Year : {Data?.age_in_years || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>Created At : {date}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                District : {Data?.district || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                District Code : {Data?.district_code || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                HIP ID : {Data?.hip_id || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Patient UID : {Data?.patient_uid || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Pincode : {Data?.pincode || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Primary Abha Address :{" "}
                {Data?.primary_abha_address || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                State Code : {Data?.state_code || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                State Name : {Data?.state_name || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Status Code : {Data?.state_code || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>Town : {Data?.town || "Not Available"}</Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Village: {Data?.village || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Village Code : {Data?.village_code || "Not Available"}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography>
                Year of Birth: {Data?.year_of_birth || "Not Available"}
              </Typography>
            </Grid>
          </Grid>
        </Box>
      )}
    </Backdrop>
  );
}
