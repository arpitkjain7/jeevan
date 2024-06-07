import { useState } from "react";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import { TextField, Typography } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { red } from "@mui/material/colors";
import axios from "axios";
import { BASE_URL } from "../../utils/request";
import { apis } from "../../utils/apis";

export default function CustomBackdrop() {
  const [open, setOpen] = useState(true);
  const [formData, setFormData] = useState({
    channel: "whatsapp",
    doc_name: "Dr.Prasad Gurjar",
    app_date: "",
    patient_name: "",
    mobile_number: "",
    destination_mobile_number: "8275330450",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [isMobileError, setIsMobileError] = useState(false);

  const handleClose = () => setOpen(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
    if (name === "mobile_number") {
      if (value.length !== 10) {
        setIsMobileError(true);
      } else {
        setIsMobileError(false);
      }
    }
  };

  const onhandleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError(false);
      await axios.post(`${BASE_URL}/${apis?.sentAppointmentList}`, formData, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      setLoading(false);
      setFormData({
        channel: "whatsapp",
        mobile_number: "",
        patient_name: "",
        app_date: "",
        doc_name: "Dr.Prasad Gurjar",
        destination_mobile_number: "8275330450",
      });
    } catch (error) {
      console.log(error);
      setLoading(false);
      setError(true);
    }
  };

  return (
    <Backdrop
      sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
      open={open}
    >
      {loading ? (
        <CircularProgress color="inherit" />
      ) : (
        <Box
          height={400}
          width={320}
          my={4}
          display="flex"
          flexDirection="column"
          gap={2}
          p={2}
          sx={{
            border: "2px solid grey",
            backgroundColor: "white",
            borderRadius: "2%",
          }}
        >
          <Box
            height="25px"
            width="25px"
            component="span"
            sx={{
              backgroundColor: "black",
              marginLeft: "auto",
              borderRadius: "50%",
              padding: "2px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              cursor: "pointer",
            }}
            onClick={handleClose}
          >
            <CloseIcon />
          </Box>
          <form onSubmit={onhandleSubmit}>
            <Typography>Full Name</Typography>
            <TextField
              onChange={handleChange}
              fullWidth
              variant="outlined"
              placeholder="Enter Your fullname"
              value={formData.patient_name}
              required
              id="patient_name"
              name="patient_name"
              sx={{ marginBottom: "10px" }}
            />
            <Typography>Mobile Number</Typography>
            <TextField
              onChange={handleChange}
              fullWidth
              variant="outlined"
              value={formData.mobile_number}
              required
              id="mobile_number"
              name="mobile_number"
              placeholder="Enter Your Mobile Number"
              sx={{ marginBottom: "10px" }}
              error={isMobileError}
              helperText={
                isMobileError
                  ? "Please enter a valid 10-digit mobile number"
                  : ""
              }
            />
            <Typography>Enter Your Appointment Date</Typography>
            <TextField
              onChange={handleChange}
              fullWidth
              variant="outlined"
              value={formData.app_date}
              required
              type="date"
              id="app_date"
              name="app_date"
              sx={{ marginBottom: "10px" }}
            />
            {error && (
              <Typography sx={{ fontSize: "13px" }} color={red[500]}>
                Error Occurred
              </Typography>
            )}
            <Button
              sx={{ width: "100%", marginTop: 2 }}
              variant="contained"
              color="success"
              type="submit"
            >
              Submit
            </Button>
          </form>
        </Box>
      )}
    </Backdrop>
  );
}
