import { List, ListItem, styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import MyTable from "../TableComponent";
import ArrowRight from "../../assets/arrows/arrow-right.svg";
import { fetchVitalDetails } from "./vitalsDetails.slice";
import { useDispatch, useSelector } from "react-redux";
import { convertDateFormat } from "../../utils/utils";

const VitalsDetailsWrapper = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primaryWhite,
  padding: theme.spacing(0, 6),
  [theme.breakpoints.down('sm')]: {
    padding: "0",
  }
}));
const VitalsDetailsContainer = styled("div")(({ theme }) => ({
  gap: theme.spacing(4),
  padding: theme.spacing(8, 0),
  [theme.breakpoints.up('sm')]: {
    display: "flex",
  }
}));
const SideList = styled(List)(({ theme }) => ({
  flex: "0.3",
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(8),
  [theme.breakpoints.down('sm')]: {
    flexDirection: "row",
    gap: "12px;",
    overflow: "auto",
    marginBottom: "10px",
  }
}));

// const VitalsList = styled("ListItem")(({ theme }) => ({}));

const Vitals = styled("div")(({ theme }) => ({
  flex: "1",
  backgroundColor: theme.palette.primaryWhite,
  borderRadius: theme.spacing(1),
  border: `1px solid ${theme.palette.primaryGrey}`,
}));
const VitalDetailsTable = styled("div")(({ theme }) => ({
  "&": {
    minHeight: "600px",
    overFlow: "auto",
  },
  ".table-class": {
    "&.MuiPaper-root": {
      borderRadius: "0",
      boxShadow: "none",
    },
    "& .MuiTableHead-root": {
      "& > tr >th": theme.typography.h3,
      [theme.breakpoints.down('md')]: {
        "&": theme.typography.body2
      },
    },
    "& .MuiTableBody-root": {
      "& > tr >td": theme.typography.body1,
    },
  },
}));

const VitalsListContainer = styled("div")(({ theme }) => ({
  padding: theme.spacing(4),
  borderRadius: theme.spacing(1),
  border: `1px solid ${theme.palette.primaryGrey}`,
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
  },

  "&.selected-vital": {
    border: `1px solid ${theme.palette.primaryBlue}`,
  },
}));

const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const VitalsDetails = () => {
  const [selectedVital, setSelectedVital] = useState("");
  const [tableData, setTableData] = useState([]);
  const dataState = useSelector((state) => state);
  const dispatch = useDispatch();
  const patient = sessionStorage?.getItem("selectedPatient");
  const list = [
    {
      type: "Body Height",
      code: "HT",
    },
    {
      type: "Body Weight",
      code: "WT",
    },
    {
      type: "Pulse Rate",
      code: "PLS",
    },
    {
      type: "Peripheral Oxy",
      code: "",
    },
    {
      type: "Body Temperature",
      code: "BT",
    },
    {
      type: "BMI",
      code: "BMI",
    },
    {
      type: "Respiration Rate",
      code: "RR",
    },
  ];

  useEffect(() => {
    const currentPatient = JSON.parse(patient);
    if (
      currentPatient &&
      Object.keys(currentPatient)?.length &&
      selectedVital
    ) {
      const payload = {
        patient_id: currentPatient?.patientId || currentPatient?.id,
        vital_type: selectedVital,
      };
      dispatch(fetchVitalDetails(payload)).then((res) => {
        const vitalData = res.payload;
        const formattedVitalList = vitalData?.map((item) => {
          const vitalDate = convertDateFormat(item?.created_date, "dd-MM-yyyy hh:mm aa");
          return {
            vitalDate: vitalDate,
            ...item,
          };
        });
        setTableData(formattedVitalList);
      });
    }
  }, [selectedVital]);
  const columns = [
    { key: "vitalDate", header: "Date" },
    { key: "pmr_id", header: "PMR Id" },
    { key: "value", header: "Value" },
  ];

  const setVitalsData = (vital) => {
    setSelectedVital(vital);
  };
  return (
    <VitalsDetailsWrapper>
      <VitalsDetailsContainer>
        <SideList>
          {list.map((item) => (
            <VitalsListContainer
              className={selectedVital === item?.code ? "selected-vital" : ""}
              onClick={() => setVitalsData(item?.code)}
            >
              <ListItem>{item?.type}</ListItem>
              <img src={ArrowRight} alt={`select-${item.type}`} />
            </VitalsListContainer>
          ))}
        </SideList>
        <Vitals>
          <VitalDetailsTable>
            <MyTable
              columns={columns}
              data={tableData}
              tableStyle={tableStyle}
              tableClassName="table-class"
              showSearch={false}
            />
          </VitalDetailsTable>
        </Vitals>
      </VitalsDetailsContainer>
    </VitalsDetailsWrapper>
  );
};

export default VitalsDetails;
