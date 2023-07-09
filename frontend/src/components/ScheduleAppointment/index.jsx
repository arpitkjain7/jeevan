import {
  Button,
  ButtonGroup,
  Card,
  CardContent,
  Grid,
  Typography,
  styled,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import {
  convertDateFormat,
  convertTimeSlot,
  convertToNumber,
  getDayFromString,
} from "../../utils/utils";
import { useDispatch, useSelector } from "react-redux";
import {
  ScheduleAppointmentActions,
  createAppointment,
  fetchDoctorSlots,
} from "./scheduleAppointment.slice";
import Calendar from "../Calendar";

const SlotWrapper = styled("div")(({ theme }) => ({
  "&": {},
  ".slot-card": {},
  ".slots-btn": {
    "&.MuiButtonBase-root": {
      display: "flex",
      padding: "4px 12px",
      width: "107px",
    },
  },
  ".date-btn": {
    "&.MuiButtonBase-root": {},
  },
  ".slots-container": {
    display: "flex",
    alignItems: "center",
    gap: "16px",
    flexWrap: "wrap",
    marginTop: "16px",
  },
  ".submit-btn": {
    "&.MuiButtonBase-root": {
      display: "flex",
      float: "right",
      justifyContent: "center",
      alignItems: "center",
      border: `1px solid ${theme.palette.primaryBlack}`,
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      backgroundColor: theme.palette.primaryBlack,
      color: theme.palette.primaryWhite,
      padding: "8px 32px",
      height: "40px",
      marginTop: "16px",
      textTransform: "capitalize",
    },
  },
}));

const StyledCard = styled(Card)({
  minWidth: 275,
  marginTop: "24px",
  padding: "",
});

const DateWrapper = styled("div")(({ theme }) => ({}));

const BookingSlots = () => {
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedSlot, setSelectedSlot] = useState("");
  const [slots, setSlots] = useState([]);
  const [dates, setDates] = useState([]);
  const [calendarDate, setCalendarDate] = useState(null);

  const doctorId = localStorage.getItem("appointment_doctor_id");
  const hospital = localStorage?.getItem("selectedHospital");

  const dispatch = useDispatch();
  const dataState = useSelector((state) => state);
  const doctorDetails = dataState?.appointmentSlots?.doctorSlotDetails;
  const appointmentDetails = dataState?.appointmentSlots?.appointmentDetails;
  const selectedPatient = dataState?.appointmentList?.patientDetails;

  const checkDoctorAvailability = (days, checkDay) => {
    const daysArray = days?.split(",")?.map((day) => day.trim().toLowerCase());
    let doctorWorking = false;
    if (daysArray?.length) {
      return daysArray?.includes(checkDay?.toLowerCase());
    }
  };

  const handleDateSelect = (date) => {
    let first = Object.keys(doctorDetails)?.length ? false : true;
    if (date !== selectedDate) {
      let currentHospital = {};

      if (hospital && doctorId) {
        currentHospital = JSON.parse(hospital);
        const id = doctorId;
        const payload = {
          hip_id: currentHospital?.hip_id,
          appointment_date: convertDateFormat(date, "yyyy-MM-dd"),
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
      const date = currentDate.toLocaleDateString(undefined, {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      });
      dates.push(date);
      currentDate.setDate(currentDate.getDate() + 1);
    }

    return dates;
  };

  useEffect(() => {
    const today = new Date();
    const thisWeek = getDates(today);
    setDates(thisWeek);
    console.log(thisWeek[0]);
    if (thisWeek?.length) {
      handleDateSelect(thisWeek[0]);
    }
  }, []);

  const generateTimeSlots = (startTime, endTime, duration) => {
    const slots = [];
    const start = new Date(`1970-01-01T${startTime}`);
    const end = new Date(`1970-01-01T${endTime}`);

    while (start < end) {
      const slotStart = start.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
      start.setMinutes(start.getMinutes() + duration);
      const slotEnd = start.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
      const slot = `${slotStart}-${slotEnd}`;
      slots.push(slot);
    }

    return slots;
  };

  useEffect(() => {
    if (doctorDetails) {
      const startTime = doctorDetails?.consultation_start_time;
      const endTime = doctorDetails?.consultation_end_time;
      const duration = convertToNumber(doctorDetails?.avg_consultation_time);
      const timeSlots = generateTimeSlots(startTime, endTime, duration);
      setSlots(timeSlots);
    }
  }, [doctorDetails]);

  const submitAppointment = () => {
    const timeRange = selectedSlot;
    const [startTime, endTime] = timeRange.split("-");
    const payload = {
      doc_id: appointmentDetails?.doctorId,
      patient_id: selectedPatient?.id,
      appointment_type: appointmentDetails?.appointmentType,
      hip_id: "123123",
      appointment_start:
        convertDateFormat(selectedDate, "yyyy-MM-dd") + " " + startTime,
      appointment_end:
        convertDateFormat(selectedDate, "yyyy-MM-dd") + " " + endTime,
    };
    dispatch(createAppointment(payload)).then((res) =>
      console.log(res.payload)
    );
    console.log(payload);
  };

  return (
    <SlotWrapper>
      <StyledCard>
        <CardContent>
          <Grid container>
            <Grid item xs={12}>
              <ButtonGroup>
                {dates?.map((date, index) => (
                  <Button
                    key={index}
                    variant={selectedDate === date ? "contained" : "outlined"}
                    color="primary"
                    onClick={() => handleDateSelect(date)}
                    className="date-btn"
                  >
                    <DateWrapper>
                      <Typography variant="body2">{date}</Typography>
                    </DateWrapper>
                  </Button>
                ))}
                {/* <Calendar
                  selectedDate={calendarDate}
                  setSelectedDate={setCalendarDate}
                /> */}
              </ButtonGroup>
            </Grid>

            {selectedDate && (
              <div className="slots-container">
                {slots?.map((slot) => (
                  <Button
                    key={slot}
                    variant={selectedSlot === slot ? "contained" : "outlined"}
                    color="primary"
                    onClick={() => handleSlotSelect(slot)}
                    className="slots-btn"
                  >
                    {convertTimeSlot(slot)}
                  </Button>
                ))}
              </div>
            )}
            {/* {selectedSlot && (
        <Grid item xs={12}>
          <Typography variant="body1">
            Selected Slot: {selectedSlot}
          </Typography>
        </Grid>
      )} */}
          </Grid>
        </CardContent>
      </StyledCard>

      <div className="btn-wrapper">
        <Button className="submit-btn" onClick={submitAppointment}>
          Save
        </Button>
      </div>
    </SlotWrapper>
  );
};

export default BookingSlots;
