import { styled } from "@mui/material";
import React, { useState } from "react";
import PatientDetailsHeader from "../../components/PatientDetailsHeader";
import CustomTabs from "../../components/Tabs";
import PastVisits from "../../components/PastVisits";
import VitalsDetails from "../../components/VitalsDetails";
import ConsentList from "../../components/ConsentList";
import GrowthChart from "../../components/GrowthChart";

const PatientDetailsWrapper = styled("div")(({ theme }) => ({
    padding: "45px 10px 10px",
  [theme.breakpoints.down('sm')]: {
    padding: "22px 10px 10px",
  }
}));

const TabsContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    borderRadius: theme.spacing(2),
    marginTop: theme.spacing(8),
    [theme.breakpoints.down('sm')]: {
      marginTop: theme.spacing(5),
    },
    "& .MuiTabs-root": {
      width: "50%",
      [theme.breakpoints.only('sm')]: {
        width: "55%"
      },
      [theme.breakpoints.down('sm')]: {
        width: "100%"
      }
    },
    "& .MuiTabs-root > .MuiTabs-scroller .MuiButtonBase-root": {
      border: 0,
    },
  },
}));

const PatientDetails = () => {
  const [tab, setTab] = useState(0);
  // const [completed, setCompleted] = useState(false);

  const handleTabChange = (newValue) => {
    setTab(newValue);
    // Perform any additional logic based on the selected tab
  };

  const tabs = [
    {
      label: "Past Visits",
      content: <PastVisits />,
    },
    {
      label: "Vitals",
      content: <VitalsDetails />,
    },
    {
      label: "Consent List",
      content: <ConsentList />,
    },
    {
      label: "Growth Chart",
      content: <GrowthChart />,
    },
  ];
  return (
    <PatientDetailsWrapper>
      <PatientDetailsHeader />
      <TabsContainer>
        <CustomTabs
          tabs={tabs}
          defaultTab={tab}
          onChange={handleTabChange}
          tab={tab}
        />
      </TabsContainer>
    </PatientDetailsWrapper>
  );
};

export default PatientDetails;
