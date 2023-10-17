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
import RegisterationConfirmation from "../RegistrationConfirmation";

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
  },
  ".submit-btn": {
    "&": theme.typography.primaryButton,
    float: "right",
    marginTop: theme.spacing(8),
    width: "10%",
  },
  ".btn-date-typography": {
    "&.MuiTypography-root": theme.typography.body1,
  },

  ".selected-date-typography": {
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

const DateButton = styled(Button)(({ theme }) => ({
  "&": theme.typography.body1,
  width: "200px",
  border: `1px solid ${theme.palette.primaryGrey}`,
  padding: theme.spacing(1, 3),
  borderRadius: theme.spacing(1),
  textAlign: "center",
  backgroundColor: theme.palette.primaryWhite,
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
  const [dates, setDates] = useState([]);
  const [calendarDate, setCalendarDate] = useState(null);
  const [appointmentcompleted, setAppointmentCompleted] = useState(false);

  const doctorId = sessionStorage.getItem("appointment_doctor_id");
  const hospital = sessionStorage?.getItem("selectedHospital");

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
    if (thisWeek?.length) {
      handleDateSelect(thisWeek[0]);
    }
  }, []);

  const generateTimeSlots = (startTime, endTime, duration) => {
    const generatedSlots = [];
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
      const timeSlots = generateTimeSlots(startTime, endTime, duration);
      setSlots(removeBookedSlots(timeSlots, slotsBooked));
    }
  }, [doctorDetails]);

  const submitAppointment = () => {
    const timeRange = selectedSlot;
    const [startTime, endTime] = timeRange.split("-");
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
          convertDateFormat(selectedDate, "yyyy-MM-dd") + " " + startTime
        ),
        appointment_end: formatDateTime(
          convertDateFormat(selectedDate, "yyyy-MM-dd") + " " + endTime
        ),
      };
      dispatch(createAppointment(payload)).then((res) => {
        if (res.payload?.appointment_id) {
          setAppointmentCompleted(true);
        }
      });
    }
  };

  const formatDisplayDate = (date) => {
    const displayArr = date?.split(" ");
    return displayArr[0] + displayArr[1];
  };

  return (
    <>
      {!appointmentcompleted ? (
        <SlotWrapper>
          <StyledCard>
            <CardContent sx={{ minHeight: "350px" }}>
              <Grid container>
                <DateContainer>
                  {dates?.map((date, index) => (
                    <Button
                      key={index}
                      color="primary"
                      onClick={() => handleDateSelect(date)}
                      className={
                        selectedDate === date ? "selected-date-btn" : "date-btn"
                      }
                    >
                      <DateWrapper>
                        <Typography
                          className={
                            selectedDate === date
                              ? `selected-date-typography`
                              : `btn-date-typography`
                          }
                        >
                          {formatDisplayDate(date)}
                        </Typography>
                      </DateWrapper>
                    </Button>
                  ))}
                  {/* <Calendar
                  selectedDate={calendarDate}
                  setSelectedDate={setCalendarDate}
                /> */}
                </DateContainer>

                {selectedDate && (
                  <div className="slots-container">
                    {slots?.map((slot) => (
                      <DateButton
                        key={slot}
                        color="primary"
                        onClick={() => handleSlotSelect(slot)}
                        className={selectedSlot === slot ? "selected-btn" : ""}
                      >
                        {convertTimeSlot(slot)}
                      </DateButton>
                    ))}
                  </div>
                )}
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
