import React from "react";
import { DateCalendar, LocalizationProvider } from "@mui/x-date-pickers";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { Dialog, DialogContent } from "@mui/material";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";
import dayjs from "dayjs";

const Calendar = ({
  selectedDate,
  setSelectedDate,
  openCalendar,
  setOpenCalendar,
}) => {
  const handleDateChange = (date) => {
    setSelectedDate(dayjs(date).format("YYYY-MM-DD"));
    setOpenCalendar(false);
  };

  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("md"));

  const handleClose = () => {
    setOpenCalendar(false);
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Dialog
        fullScreen={fullScreen}
        open={openCalendar}
        onClose={handleClose}
        aria-labelledby="responsive-dialog-title"
      >
        <DialogContent>
          <DemoContainer components={["DateCalendar"]}>
            <DateCalendar
              value={selectedDate ? dayjs(selectedDate, "DD/MM/YYYY") : null}
              onChange={handleDateChange}
            />
          </DemoContainer>
        </DialogContent>
      </Dialog>
    </LocalizationProvider>
  );
};

export default Calendar;
