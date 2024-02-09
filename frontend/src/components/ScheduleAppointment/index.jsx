import {
  Button,
  ButtonGroup,
  Card,
  CardContent,
  Grid,
  TextField,
  Typography,
  styled,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import {
  parseDateFormat,
  convertTimeSlot,
  convertToNumber,
  getDayFromString,
  customformatDate,
  convertDateFormat
} from "../../utils/utils";
import { useDispatch, useSelector } from "react-redux";
import {
  ScheduleAppointmentActions,
  createAppointment,
  fetchDoctorSlots,
} from "./scheduleAppointment.slice";
import Calendar from "../Calendar";
import RegisterationConfirmation from "../RegistrationConfirmation";
import { format } from "date-fns";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DesktopDatePicker } from "@mui/x-date-pickers";
import dayjs from "dayjs";

const isMobile = window.innerWidth < 600;
const SlotWrapper = styled("div")(({ theme }) => ({
  "&": {},
  "& .cardContentStyle": {
  [theme.breakpoints.up("sm")]: {
    minHeight: "350px",
  }
  },
  ".datepickerInputStyle .MuiOutlinedInput-root .MuiOutlinedInput-notchedOutline": {
      border: `2px solid ${theme.palette.secondaryBlue}`,
    },
  ".slot-card": {},
  ".slots-btn": {
    "&.MuiButtonBase-root": {
      display: "flex",
      padding: "4px 12px",
      width: "107px",
    },
  },
  ".date-btn": {
    "&.MuiButtonBase-root": {
      "&": theme.typography.body2,
      backgroundColor: "transparent",
      border: "0",
      borderBottom: `1px solid ${theme.palette.primaryGrey}`,
      flex: 1,
      borderRadius: "0",
      cursor: "pointer",
    },
  },
  ".selected-date-btn": {
    "&.MuiButtonBase-root": {
      "&": theme.typography.body2,
      backgroundColor: "transparent",
      border: "0",
      borderBottom: `2px solid ${theme.palette.secondaryBlue}`,
      flex: 1,
      borderRadius: "0",
      boxShadow: "none",
      cursor: "pointer",
    },
  },
  ".slots-container": {
    display: "flex",
    alignItems: "center",
    gap: "16px",
    flexWrap: "wrap",
    marginTop: "16px",
    [theme.breakpoints.down("sm")]: {
      gap: "12px",
      maxHeight: "350px",
      overflowX: "scroll",
    },
  },
  ".submit-btn": {
    "&": theme.typography.primaryButton,
    float: "right",
    marginTop: theme.spacing(8),
    width: "10%",
    marginBottom: "8px",
    [theme.breakpoints.down('sm')]: {
      marginTop: "20px",
      width: "28%",
    }
  },
  ".btn-wrapper": {
    [theme.breakpoints.down('sm')]: {
      display: "flex",
      justifyContent: "center",
    }
  },
  ".btn-date-typography": {
    width: "min-content",
    "&.MuiTypography-root": theme.typography.body1,
  },

  ".selected-date-typography": {
    width: "min-content",
    "&.MuiTypography-root": theme.typography.selectedBody1,
  },
}));
const DateContainer = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  width: "100%",
}));

const StyledCard = styled(Card)({
  minWidth: 275,
  marginTop: "24px",
  padding: "",
});

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

const DateWrapper = styled("div")(({ theme }) => ({}));

const BookingSlots = () => {
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedSlot, setSelectedSlot] = useState("");
  const [slots, setSlots] = useState([]);
  const [allTimeSlots, setAllTimeSlots] = useState([]);
  const [todaySlots, setTodaySlots] = useState([]);
  const [dates, setDates] = useState([]);
  const [calendarDate, setCalendarDate] = useState(null);
  const [appointmentDate, setAppointmentDate] = useState(false);
  const [appointmentcompleted, setAppointmentCompleted] = useState(false);
  const [cleared, setCleared] = useState(false);
  const doctorId = sessionStorage.getItem("appointment_doctor_id");
  const hospital = sessionStorage?.getItem("selectedHospital");

  const dispatch = useDispatch();
  const dataState = useSelector((state) => state);
  const doctorDetails = dataState?.appointmentSlots?.doctorSlotDetails;
  const appointmentDetails = dataState?.appointmentSlots?.appointmentDetails;
  const selectedPatient = JSON.parse(sessionStorage.getItem("selectedPatient"));
  const today = new Date();
  const current_date = parseDateFormat(today, "yyyy-MM-dd");

  const checkDoctorAvailability = (days, checkDay) => {
    const daysArray = days?.split(",")?.map((day) => day?.trim().toLowerCase());
    let doctorWorking = false;
    if (daysArray?.length) {
      return daysArray?.includes(checkDay?.toLowerCase());
    }
  };

  const handleDateSelect = (date) => {
    console.log(date);
    let first = Object.keys(doctorDetails)?.length ? false : true;
    if (date !== selectedDate) {
      let currentHospital = {};
      if (hospital && doctorId) {
        currentHospital = JSON.parse(hospital);
        const id = doctorId;
        const payload = {
          hip_id: currentHospital?.hip_id,
          appointment_date: parseDateFormat(date, "yyyy-MM-dd"),
        };
        dispatch(fetchDoctorSlots({ id, payload })).then((res) => {
          const doctorAvailable = checkDoctorAvailability(
            res.payload?.doc_working_days || "",
            getDayFromString(date)
          );
          if (!doctorAvailable) {
            dispatch(ScheduleAppointmentActions?.clearDoctorData());
          }
        });
      }
    }
    
    setSelectedDate(date);
    setSelectedSlot("");
  };

  const handleSlotSelect = (slot) => {
    setSelectedSlot(slot);
  };

  // Helper function to generate an array of dates for the current week
  const getDates = (startDate) => {
    const dates = [];
    const currentDate = new Date(startDate);

    for (let i = 0; i < 7; i++) {
      const date = convertDateFormat(currentDate, "yyyy-MM-dd");
      const day = currentDate.toLocaleDateString(undefined, {
        weekday: "long",
      })
      dates.push({date: date, day: day });
      currentDate.setDate(currentDate.getDate() + 1);
    }
    console.log(dates);
    return dates;
  };

  useEffect(() => {
    const thisWeek = getDates(today);
    console.log(thisWeek);
    setDates(thisWeek);
    if (thisWeek?.length) {
      handleDateSelect(formatDate(thisWeek[0].date));
    }
  }, []);

  const isWeekend = (date) => {
    const day = parseDateFormat(date, "yyyy-MM-dd");
    const dayFormat = parseDateFormat(date, "yyyy-MM-dd");
    const week = [];
    const currentDate = new Date();
    for (let i = 0; i < 7; i++) {
      const date = currentDate.toLocaleDateString(undefined, {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      });
      week.push(date);
      currentDate.setDate(currentDate.getDate() + 1);
    }
    return week.includes(day || dayFormat);
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

  function formatDateTime(dateTimeString) {
    const [datePart, timePart] = dateTimeString.split(" ");
    const [hour, minute] = timePart.split(":");
    const formattedTime = `${hour}:${minute}`;

    return `${datePart} ${formattedTime}`;
  }

  useEffect(() => {
    if (cleared) {
      const timeout = setTimeout(() => {
        setAppointmentDate(false);
        setCleared(false);
      }, 1500);

      return () => clearTimeout(timeout);
    }
    return () => {};
  }, [cleared]);

  useEffect(() => {
    let filledSlots = [];
    if (doctorDetails?.slots) {
      doctorDetails.slots?.map((slot) => {
        const startTime = slot.start_time;
        const endTime = slot.end_time;
        const range = `${startTime}-${endTime}`;
        filledSlots?.push(range);
      });
    }
    const slotsBooked = convertToTimeSlots(filledSlots);
    if (doctorDetails) {
      const startTime = doctorDetails?.consultation_start_time;
      const endTime = doctorDetails?.consultation_end_time;
      const duration = convertToNumber(doctorDetails?.avg_consultation_time);

      const currentTime = today.toLocaleTimeString(undefined, {
        hour12: false,
      });
      console.log(currentTime, startTime);
      if (currentTime > startTime && currentTime < endTime) {
        let currentSlotStartTime;
        allTimeSlots.map((slot) => {
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
      }
      const timeSlots = generateTimeSlots(startTime, endTime, duration);
      const removedBookedSlots = removeBookedSlots(timeSlots, slotsBooked);
      const finalSlots = removedBookedSlots.map(item => {
        return convertTimeSlot(item)
      })
      setSlots(finalSlots);
    }
  }, [doctorDetails]);

  const submitAppointment = () => {
    const timeRange = selectedSlot;
    const [startTime, endTime] = timeRange.split(" - ");
    let startTime24hour;
    let endTime24hour;
    if(startTime){
      var startTimeHour = Number(startTime.match(/^(\d+)/)[1]);
      var startTimeMinutes = Number(startTime.match(/:(\d+)/)[1]);
      var meridiem = startTime.slice(-2);
      if(meridiem === "PM" && startTimeHour < 12) startTimeHour = startTimeHour + 12;
      else if(meridiem === "AM" && startTimeHour === 12) startTimeHour = startTimeHour-12;
      var sHours = startTimeHour.toString();
      var sMinutes = startTimeMinutes.toString();
      if(startTimeHour<10) sHours = "0" + sHours;
      if(startTimeMinutes<10) sMinutes = "0" + sMinutes;
        startTime24hour = sHours + ":" + sMinutes;
    }
    if(endTime){
      var endTimeHour = Number(endTime.match(/^(\d+)/)[1]);
      var endTimeMinutes = Number(endTime.match(/:(\d+)/)[1]);
      var meridiem = endTime.slice(-2);
      if(meridiem === "PM" && endTimeHour < 12) endTimeHour = endTimeHour + 12;
      else if(meridiem === "AM" && endTimeHour === 12) endTimeHour = endTimeHour-12;
      var sHours = endTimeHour.toString();
      var sMinutes = endTimeMinutes.toString();
      if(endTimeHour<10) sHours = "0" + sHours;
      if(endTimeMinutes<10) sMinutes = "0" + sMinutes;
      endTime24hour = sHours + ":" + sMinutes;
    }
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);

      const payload = {
        doc_id: appointmentDetails?.doctorId,
        patient_id: selectedPatient?.id,
        appointment_type: appointmentDetails?.appointmentType,
        encounter_type: appointmentDetails?.encounterType,
        hip_id: currentHospital?.hip_id,
        appointment_start: formatDateTime(
          parseDateFormat(selectedDate, "yyyy-MM-dd") + " " + startTime24hour
        ),
        appointment_end: formatDateTime(
          parseDateFormat(selectedDate, "yyyy-MM-dd") + " " + endTime24hour
        ),
      };
      dispatch(createAppointment(payload)).then((res) => {
        sessionStorage.removeItem("doctorName");
        sessionStorage.removeItem("encounterTypeValue");
        sessionStorage.removeItem("appointmentTypeValue");
        sessionStorage.removeItem("visitTypeValue");
        sessionStorage.removeItem("billingTypeValue");
        if (res.payload?.appointment_id) {
          const AllPatientData = Object.assign(
            selectedPatient,
            { patientId: selectedPatient?.id },
            { doc_id: appointmentDetails?.doctorId }, 
            { appointment_id: res.payload?.appointment_id },
            { id: res.payload?.appointment_id }
          )
          sessionStorage.setItem("selectedPatient", JSON.stringify(AllPatientData));
          setAppointmentCompleted(true);
        }
      });
    }
  };

  const formatDisplayDate = (date) => {
    console.log(date);
    // const displayArr = date?.split(" ");
    return convertDateFormat(date, "dd/MM/yyyy");
  };

  const formatDate = (date) => {
    console.log(date);
    // const displayArr = date?.split(" ");
    const formatedDate = parseDateFormat(date, "yyyy-MM-dd");
    return formatedDate;
  };

  return (
    <>
      {!appointmentcompleted ? (
        <SlotWrapper>
          <StyledCard>
            <CardContent className="cardContentStyle">
              {isMobile && (
                <>
                  <Typography>Select Date</Typography>
                  <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DemoContainer components={["DatePicker"]}>
                      <DesktopDatePicker
                        slotProps={{
                          field: { clearable: true, onClear: () => setCleared(true) },
                          actionBar: {
                            actions: ['clear'],
                          },
                        }}
                        disablePast
                        defaultValue={dayjs(today)}
                        onChange={(newValue) =>
                          handleDateSelect(newValue)
                        }
                      />
                    </DemoContainer>
                  </LocalizationProvider>
                </>
              )}
              <Grid container>
                {!isMobile && (
                  <DateContainer>
                    {dates?.map((date, index) => (
                      <Button
                        key={index}
                        color="primary"
                        onClick={() => {
                          setAppointmentDate(false);
                          handleDateSelect(parseDateFormat(date.date,"yyyy-MM-dd"))
                        }}
                        className={
                          selectedDate === formatDate(date.date)
                            ? "selected-date-btn"
                            : "date-btn"
                        }
                      >
                        <DateWrapper>
                          <Typography
                            className={
                              selectedDate === formatDate(date.date)
                                ? `selected-date-typography`
                                : `btn-date-typography`
                            }
                          >
                            <span style={{  }}>{date.day}, </span>
                            <span> {formatDisplayDate(date.date)}</span>
                          </Typography>
                        </DateWrapper>
                      </Button>
                    ))}
                    {/* <Typography>Select Date</Typography> */}
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                      <DemoContainer components={["DatePicker"]}>
                        <DesktopDatePicker
                          slotProps={{
                            field: { clearable: true, onClear: () => setCleared(true) },
                            actionBar: {
                              actions: ['clear'],
                            },
                          }}
                          sx={{ padding: "10px" }}
                          disablePast
                          shouldDisableDate={isWeekend}
                          onChange={(newValue) => {
                            setAppointmentDate(true)
                            handleDateSelect(parseDateFormat(newValue,"yyyy-MM-dd"))
                          }}
                          className={
                            appointmentDate ? "datepickerInputStyle" : ""
                          }
                        />
                      </DemoContainer>
                    </LocalizationProvider>
                    {/* <Calendar
                    selectedDate={calendarDate}
                    setSelectedDate={setCalendarDate}
                  /> */}
                  </DateContainer>
                )}
                {selectedDate &&
                  (selectedDate !== current_date ? (
                    <div className="slots-container">
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
                      )) : <h4>No slots available</h4>}
                    </div>
                  ) : (
                    <div className="slots-container">
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
                      )) : <h4>No slots available</h4>}
                    </div>
                  ))}
              </Grid>
            </CardContent>
          </StyledCard>

          <div className="btn-wrapper">
            <Button className="submit-btn" onClick={submitAppointment}>
              Submit
            </Button>
          </div>
        </SlotWrapper>
      ) : (
        <RegisterationConfirmation
          isAppointment={true}
          appointmentDetails={appointmentDetails}
        />
      )}
    </>
  );
};

export default BookingSlots;
