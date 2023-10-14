import { styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import MyTable from "../TableComponent";
import { useDispatch } from "react-redux";
import { fetchConsentList } from "./consentList.slice";
import RightArrow from "../../assets/arrows/arrow-right.svg";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";

const ConsentListContainer = styled("div")(({ theme }) => ({
  padding: theme.spacing(8, 6),
}));

const TabsContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    borderRadius: theme.spacing(2),
    marginTop: theme.spacing(8),
    "& .MuiTabs-root": {
      width: "50%",
    },
    "& .MuiTabs-root > .MuiTabs-scroller .MuiButtonBase-root": {
      border: 0,
    },
  },
  ".table-class": {
    "&.MuiPaper-root": {
      borderRadius: "0",
      boxShadow: "none",
    },
    "& .MuiTableHead-root": {
      "& > tr >th": theme.typography.body2,
    },
    "& .MuiTableBody-root": {
      "& > tr >td": theme.typography.body1,
    },
  },
}));

const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const ConsentList = () => {
  const patient = sessionStorage?.getItem("selectedPatient");
  const [tableData, setTableData] = useState([]);
  const dispatch = useDispatch();

  useEffect(() => {
    const currentPatient = JSON.parse(patient);
    if (currentPatient && Object.keys(currentPatient)?.length) {
      const patientId = currentPatient?.id;
      dispatch(fetchConsentList(patientId)).then((response) => {
        const consentData = response?.payload;
        setTableData(consentData);
      });
    }
  }, []);

  const columns = [
    { key: "status", header: "Request Status" },
    { key: "created_at", header: "Consent Created On" },
    { key: "hiu_id", header: "Consent Granted on" },
    { key: "expire_at", header: "Consent Expiry On" },
    {
      key: "actions",
      header: "",
      actions: [
        {
          type: "icon",
          icon: <img src={RightArrow} alt="details" />,
          // onClick: (item) => {
          //   dispatch(AppointmentPageActions.setSelectedPatientData(item));
          //   navigate("/create-appointment");
          // },
        },
      ],
    },
  ];

  return (
    <ConsentListContainer>
      {tableData?.length && (
        <MyTable
          columns={columns}
          data={tableData}
          tableStyle={tableStyle}
          tableClassName="table-class"
          showSearch={false}
        />
      )}
    </ConsentListContainer>
  );
};

export default ConsentList;
