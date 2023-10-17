import { Button, styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import MyTable from "../TableComponent";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchConsentList } from "./consentList.slice";
import RightArrow from "../../assets/arrows/arrow-right.svg";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ConsentModal from "../ConsentModal";

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

const CustomButton = styled(Button)(({ theme }) => ({
  "&": theme.typography.secondaryButton,
}));
const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const ConsentList = () => {
  const patient = sessionStorage?.getItem("selectedPatient");
  const [tableData, setTableData] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    sessionStorage.removeItem("consentSelected");
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
          onClick: (item) => {
            sessionStorage.setItem("consentSelected", JSON.stringify(item));
            navigate("/consent-detail");
          },
        },
      ],
    },
  ];

  const handleModalOpen = () => {
    setModalOpen(true);
  };

  const handleModalClose = () => {
    setModalOpen(false);
  };

  const purposeOptions = [
    { label: "Option 1", value: "option1" },
    { label: "Option 2", value: "option2" },
    // Add more options as needed
  ];

  const infoTypeOptions = [
    { label: "Type A", value: "typeA" },
    { label: "Type B", value: "typeB" },
    // Add more options as needed
  ];

  return (
    <ConsentListContainer>
      <ConsentModal
        open={modalOpen}
        handleClose={handleModalClose}
        purposeOptions={purposeOptions}
        infoTypeOptions={infoTypeOptions}
      />
      {tableData?.length && (
        <MyTable
          columns={columns}
          data={tableData}
          tableStyle={tableStyle}
          tableClassName="table-class"
          showSearch={false}
        />
      )}
      <CustomButton onClick={handleModalOpen}>Request Consent</CustomButton>
    </ConsentListContainer>
  );
};

export default ConsentList;
