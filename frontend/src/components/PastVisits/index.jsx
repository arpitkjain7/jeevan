import { List, styled } from "@mui/material";
import React from "react";

const VisitsWrapper = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primaryWhite,
  padding: theme.spacing(0, 6),
}));
const Visits = styled("div")(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(4),
  padding: theme.spacing(8,0)
}));
const SideList= styled("List")(({ theme }) => ({
    display:"flex",
    flexDirection:"column",
    gap: theme.spacing(8)

}));

const DiagnosisDetails = styled("ListItem")(({ theme }) => ({
    padding:theme.spacing(2, 4),
    borderRadius: theme.spacing(1),
    border :`1px solid ${theme.palette.primaryGrey}`
}));

const PrescriptionDeatils = styled("div")(({ theme }) => ({
  flex: "1",
  backgroundColor: theme.palette.primaryGrey,
}));

const PastVisits = () => {
  const list = [
    {
      type: "Diagnosis",
      date: "26 June",
      time: "9:30AM",
    },
    {
      type: "Diagnosis",
      date: "26 June",
      time: "9:30AM",
    },
    {
      type: "Diagnosis",
      date: "26 June",
      time: "9:30AM",
    },
  ];
  return (
    <VisitsWrapper>
      <Visits>
        <SideList>
          {list.map((item) => (
            <DiagnosisDetails>{item?.type}</DiagnosisDetails>
          ))}
        </SideList>
        <PrescriptionDeatils></PrescriptionDeatils>
      </Visits>
    </VisitsWrapper>
  );
};

export default PastVisits;
