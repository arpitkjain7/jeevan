import React, { useState } from "react";
import CustomTabs from "../../components/Tabs";
import AppointmentForm from "../../components/AppointmentForm";
import BookingSlots from "../../components/ScheduleAppointment";
import { Typography, styled } from "@mui/material";
import AppointmentIcon from "../../assets/icons/prescription-icon.svg";
import CalendarIcon from "../../assets/icons/calendar-icon.svg";

const AppointmentWrapper = styled("div")(({ theme }) => ({
  padding: "40px 10px 10px"
}));

const PageTitle = styled(Typography)(({ theme }) => ({
  "&": theme.typography.h1,
  [theme.breakpoints.down('md')]: {
    "&": theme.typography.h4,
  },
}));

const PageSubText = styled(Typography)(({ theme }) => ({
  "&": theme.typography.h2,
  marginBottom: theme.spacing(8),
}));

function CreateAppointment() {
  const [tab, setTab] = useState(0);
  const [completed, setCompleted] = useState(false);

  const handleTabChange = (newValue) => {
    setTab(newValue);
    // Perform any additional logic based on the selected tab
  };

  const tabs = [
    {
      label: "Encounter",
      icon: AppointmentIcon,
      content: (
        <AppointmentForm
          handleTabChange={handleTabChange}
          setTab={setTab}
          setCompleted={setCompleted}
        />
      ),
    },
    {
      label: "Select Slot",
      icon: CalendarIcon,
      content: (
        <BookingSlots handleTabChange={handleTabChange} setTab={setTab} />
      ),
      disable: !completed,
    },
  ];

  return (
    <AppointmentWrapper>
      <PageTitle>New Appointment</PageTitle>
      <PageSubText>Schedule an appointment</PageSubText>
      <CustomTabs
        tabs={tabs}
        defaultTab={tab}
        onChange={handleTabChange}
        tab={tab}
        addSteps={true}
      />
    </AppointmentWrapper>
  );
}

export default CreateAppointment;
