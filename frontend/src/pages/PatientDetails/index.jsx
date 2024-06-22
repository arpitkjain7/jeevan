import { styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import PatientDetailsHeader from "../../components/PatientDetailsHeader";
import CustomTabs from "../../components/Tabs";
import PastVisits from "../../components/PastVisits";
import VitalsDetails from "../../components/VitalsDetails";
import ConsentList from "../../components/ConsentList";

const PatientDetailsWrapper = styled("div")(({ theme }) => ({
  padding: "45px 10px 10px",
  [theme.breakpoints.down("sm")]: {
    padding: "22px 10px 10px",
  },
}));

const TabsContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    borderRadius: theme.spacing(2),
    marginTop: theme.spacing(8),
    [theme.breakpoints.down("sm")]: {
      marginTop: theme.spacing(5),
    },
    "& .MuiTabs-root": {
      width: "50%",
      [theme.breakpoints.only("sm")]: {
        width: "55%",
      },
      [theme.breakpoints.down("sm")]: {
        width: "100%",
      },
    },
    "& .MuiTabs-root > .MuiTabs-scroller .MuiButtonBase-root": {
      border: 0,
    },
  },
}));

const PatientDetails = () => {
  const [tab, setTab] = useState(() => {
    const patientDetailsTab = sessionStorage.getItem("Tabs");
    return patientDetailsTab !== null ? Number(patientDetailsTab) : 0;
  });

  useEffect(() => {
    sessionStorage.setItem("Tabs", tab);
  }, [tab]);

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
