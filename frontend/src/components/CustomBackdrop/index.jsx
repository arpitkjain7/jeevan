import { useEffect, useState } from "react";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  TextField, 
  Typography,
  styled,
  IconButton,
  Grid,
  RadioGroup,
  FormControlLabel,
  Radio,
  FormControl,
  FormLabel,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { red } from "@mui/material/colors";
import axios from "axios";
import { BASE_URL } from "../../utils/request";
import { apis } from "../../utils/apis";
import { format } from "date-fns";
import { convertTimeSlot, convertToNumber, parseDateFormat } from "../../utils/utils";

const SlotsWrapper = styled("div")(({theme}) =>({
  "&": { 
    border: "1px solid grey", 
    padding: "10px"
  },
  ".slots_wrapper_container": {
    maxHeight: "160px", 
    overflow: "hidden scroll", 
    scrollbarWidth: "thin"
  }
}));

const SlotsContainer = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    alignItems: "center",
    gap: "15px",
    flexWrap: "wrap",
    marginTop: "8px",
    justifyContent: "space-around",
    [theme.breakpoints.down("sm")]: {
      gap: "12px",
      maxHeight: "350px",
      overflowX: "scroll",
    },
  }
}));

const DateButton = styled("button")(({ theme }) => ({
  "&": theme.typography.body1,
  width: "180px",
  border: `1px solid ${theme.palette.primaryGrey}`,
  padding: theme.spacing(2, 4),
  borderRadius: theme.spacing(1),
  textAlign: "center",
  backgroundColor: theme.palette.primaryWhite,
  [theme.breakpoints.down("sm")]: {
    width: "140px",
    padding: theme.spacing(2, 1.5),
  },
  [theme.breakpoints.down("350")]: {
    width: "114px",
  },
  "&.selected-btn": {
    backgroundColor: theme.palette.secondaryOpacityBlue,
    border: `1px solid ${theme.palette.secondaryBlue}`,
  },
}));

export default function CustomBackdrop(doctorDetails) {
  const today = new Date();
  const date_today = parseDateFormat(today, "yyyy-MM-dd");
  const [open, setOpen] = useState(true);
  const [formData, setFormData] = useState({
    channel: "whatsapp",
    doc_name: "Dr.Prasad Gurjar",
    app_date: selectedDate,
    patient_name: "",
    mobile_number: "",
    gender: "M",
    dob: "",
    destination_mobile_number: "8275330450",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [isMobileError, setIsMobileError] = useState(false);
  const [selectedSlot, setSelectedSlot] = useState("");
  const [selectedDate, setSelectedDate] = useState(date_today);
  const [slots, setSlots] = useState([]);
  const [todaySlots, setTodaySlots] = useState([]);
  const [allTimeSlots, setAllTimeSlots] = useState([]);
  const [openSlotsSection, setOpenSlotsSection] = useState(false);

  const handleSlotSelect = (slot) => {
    setSelectedSlot(slot);
  };

  const generateTimeSlots = (startTime, endTime, duration) => {
    const generatedSlots = [];
    const start = new Date(`1970-01-01T${startTime}`);
    const end = new Date(`1970-01-01T${endTime}`);
    while (start < end) {
      const meridiemSlotStart = start.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
      const slotStart = start.toLocaleTimeString(undefined, {
        hour12: false,
        hour: "numeric",
        minute: "numeric",
      });
      start.setMinutes(start.getMinutes() + duration);
      const slotEnd = start.toLocaleTimeString(undefined, {
        hour12: false,
        hour: "numeric",
        minute: "numeric",
      });
      const meridiemSlotEnd = start.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      setAllTimeSlots((allTimeSlots) => [
        ...allTimeSlots,
        `${slotStart}-${slotEnd}`,
      ]);
      const slot = `${slotStart}-${slotEnd}`;
      generatedSlots.push(slot);
    }

    return generatedSlots;
  };

  function convertToTimeSlots(bookedSlots) {
    // Convert the booked time slots to the format 'HH:mm-HH:mm'
    return bookedSlots.map((slot) => {
      const [startTime, endTime] = slot.split("-");
      return `${startTime.slice(0, 5)}-${endTime.slice(0, 5)}`;
    });
  }

  function removeBookedSlots(originalSlots, bookedSlots) {
    // Convert booked slots to the 'HH:mm-HH:mm' format
    const bookedSlotsFormatted = convertToTimeSlots(bookedSlots);

    // Remove booked time slots from the original slots
    const availableSlots = originalSlots.filter(
      (slot) => !bookedSlotsFormatted.includes(slot)
    );
    return availableSlots;
  }

  useEffect(() => {
    let filledSlots = [];
    if (doctorDetails?.doctorDetails) {
      // doctorDetails?.slots?.map((slot) => {
      //   const startTime = slot.start_time;
      //   const endTime = slot.end_time;
      //   const range = `${startTime}-${endTime}`;
      //   filledSlots?.push(range);
      // });
    
      // const slotsBooked = convertToTimeSlots(filledSlots);
      const slotsBooked = [];
      const startTime = doctorDetails?.doctorDetails?.consultation_start_time;
      const endTime = doctorDetails?.doctorDetails?.consultation_end_time;
      const duration = convertToNumber(doctorDetails?.doctorDetails?.avg_consultation_time);
      
      const timeSlots = generateTimeSlots(startTime, endTime, duration);
      const currentTime = today.toLocaleTimeString(undefined, {
        hour12: false,
      });
      if (currentTime > startTime && currentTime < endTime) {
        let currentSlotStartTime;
        timeSlots.map((slot) => {
          const [slotStartTime, slotEndTime] = slot.split("-");
          const current_time = today.toLocaleTimeString(undefined, {
            hour12: false,
            hour: "numeric",
            minute: "numeric",
          });
          if (current_time > slotStartTime && current_time < slotEndTime) {
            currentSlotStartTime = slotEndTime;
          }
        });
        const todayTimeSlots = generateTimeSlots(
          currentSlotStartTime,
          endTime,
          duration
        );
        const todayRemovedBookedSlots = removeBookedSlots(todayTimeSlots, slotsBooked);
        const todayFinalSlots = todayRemovedBookedSlots.map(item => {
          return convertTimeSlot(item)
        })
        setTodaySlots(todayFinalSlots);
      } else if (startTime > currentTime && currentTime < endTime){
        const todayRemovedBookedSlots = removeBookedSlots(timeSlots, slotsBooked);
        const todayFinalSlots = todayRemovedBookedSlots.map(item => {
          return convertTimeSlot(item)
        })
        setTodaySlots(todayFinalSlots);
      }
      const removedBookedSlots = removeBookedSlots(timeSlots, slotsBooked);
      const finalSlots = removedBookedSlots.map(item => {
        return convertTimeSlot(item)
      });
      setSlots(finalSlots);
    }
  }, [doctorDetails]);

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
    if (name === "app_date") {
      setSelectedDate(value);
    }
  };

  const onhandleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError(false);
      await axios.post(`${BASE_URL}/${apis?.sendAppointmentList}`, formData, {
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
        <Dialog
          // height={400}
          // width="70%"
          // my={4}
          // display="flex"
          // flexDirection="column"
          // gap={2}
          // p={4}
          open={open}
          onClose={handleClose}
          maxWidth="450px"
          // sx={{
          //   border: "2px solid grey",
          //   backgroundColor: "white",
          //   borderRadius: "2%",
          // }}
        >
          {/* <Box
            // height="25px"
            // width="25px"
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
          </Box> */}
        <DialogTitle >
          Book an Appointment
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
        <DialogContent dividers>
          <form onSubmit={onhandleSubmit}>
            <Grid container spacing={4}>
              <Grid item xs={12} md={6}>
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
              </Grid>
              <Grid item xs={12} md={6}>
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
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography>DOB</Typography>
                <TextField
                  name="dob"
                  value={formData.dob}
                  onChange={handleChange}
                  type="date"
                  inputProps={{
                    max: format(new Date(), "yyyy-MM-dd"), // Set max date to the current date
                  }}
                  InputLabelProps={{ shrink: true }}
                  // required
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={6}>
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
              <Grid item xs={12} md={6}>
                <Typography>Enter Your Appointment Date</Typography>
                <TextField
                  fullWidth
                  variant="outlined"
                  value={selectedDate}
                  onChange={handleChange}
                  required
                  type="date"
                  inputProps={{
                    min: format(new Date(), "yyyy-MM-dd"), // Set max date to the current date
                  }}
                  // id="app_date"
                  name="app_date"
                  sx={{ marginBottom: "10px" }}
                />
              </Grid>
            </Grid>
            {/* <Button 
              variant="outlined"
              onClick={handleSelectSlot}
              disabled={formData.app_date === "" ? true : false}
              fullWidth
            >
              Select slot
            </Button> */}
            <br/>
            <Typography>Available Slots:</Typography> 
            {
                selectedDate === date_today 
              ? 
              (
                <SlotsWrapper>
                <Box className="slots_wrapper_container">
                <SlotsContainer>
                  {todaySlots.length > 0 ? todaySlots?.map((todayslot) => (
                    <DateButton
                      key={todayslot}
                      color="primary"
                      onClick={() => handleSlotSelect(todayslot)}
                      className={
                        selectedSlot === todayslot ? "selected-btn" : ""
                      }
                    >
                      {todayslot}
                    </DateButton>
                  )) : <h4 color="black">No slots available</h4>}
                </SlotsContainer>
                </Box>
                </SlotsWrapper>
              )
              :
              (
                <SlotsWrapper>
                <Box className="slots_wrapper_container">
                <SlotsContainer>
                  {slots.length > 0 ? slots.map((slot) => (
                    <DateButton
                      key={slot}
                      color="primary"
                      onClick={() => handleSlotSelect(slot)}
                      className={
                        selectedSlot === slot ? "selected-btn" : ""
                      }
                    >
                      {slot}
                    </DateButton>
                  )) : <h4 color="black">No slots available</h4>}
                </SlotsContainer>
                </Box>
                </SlotsWrapper>
              )
            }    
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
          </DialogContent>
        </Dialog>
      )}
    </Backdrop>
  );
}
