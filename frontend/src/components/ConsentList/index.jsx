import { Button, styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import MyTable from "../TableComponent";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchConsentList } from "./consentList.slice";
import RightArrow from "../../assets/arrows/arrow-right.svg";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import ConsentModal from "../ConsentModal";
import { convertDateFormat } from "../../utils/utils";

const ConsentListContainer = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 6),
}));

const ConsentDataWrapper = styled("div")(({ theme }) => ({}));

const ConsentTableContainer = styled("div")(({ theme }) => ({
  maxHeight: "600px",
  overflow: "auto",
  border: "1px solid rgba(224, 224, 224, 1)",
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
const ButtonWrapper = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 6),
  display: "flex",
  justifyContent: "flex-end",
  alignItems: "center",
  marginBottom: theme.spacing(5),
}));
const CustomButton = styled(Button)(({ theme }) => ({
  "&": theme.typography.tertiaryButton,
}));
const tableStyle = {
  backgroundColor: "#f1f1f1",
  // maxWidth: '600px'
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
        const formattedConsentList = consentData?.map((item) => {
          const createdAt = convertDateFormat(item?.created_at, "dd-MM-yyyy");
          const expireAt = convertDateFormat(item?.expire_at, "dd-MM-yyyy");
          const consentStatus = item?.status;
          return {
            consentStatus: consentStatus,
            createdAt: createdAt,
            expireAt: expireAt,
            ...item,
          };
        });
        setTableData(formattedConsentList);
      });
    }
  }, []);

  const columns = [
    { key: "createdAt", header: "Consent Created On"},
    { key: "consentStatus", header: "Consent Status"},
    { key: "expireAt", header: "Consent Expiry On" },
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
    { label: "Care Management", value: "Care Management" },
    { label: "Break the Glass", value: "Break the Glass" },
    { label: "Public Health", value: "Public Health" },
    { label: "Healthcare Payment", value: "Healthcare Payment" },
    {
      label: "Disease Specific Healthcare Research",
      value: "Disease Specific Healthcare Research",
    },
    { label: "Self Requested", value: "Self Requested" },
  ];

  const infoTypeOptions = [
    { label: "Prescription", value: "Prescription" },
    { label: "Diagnostic Report", value: "DiagnosticReport" },
    { label: "OP Consultation", value: "OPConsultation" },
    { label: "Discharge Summary", value: "DischargeSummary" },
    { label: "Immunization Record", value: "ImmunizationRecord" },
    { label: "Record artifact", value: "HealthDocumentRecord" },
    { label: "Wellness Record", value: "WellnessRecord" },
  ];

  return (
    <ConsentListContainer>
       <ButtonWrapper>
        <CustomButton onClick={handleModalOpen}>Request Consent</CustomButton>
      </ButtonWrapper>
      <ConsentDataWrapper>
        <ConsentModal
          open={modalOpen}
          handleClose={handleModalClose}
          purposeOptions={purposeOptions}
          infoTypeOptions={infoTypeOptions}
        />
        <ConsentTableContainer>
          {tableData?.length && (
            <MyTable
              columns={columns}
              data={tableData}
              tableStyle={tableStyle}
              tableClassName="table-class"
              showSearch={false}
            />
          )}
        </ConsentTableContainer>
      </ConsentDataWrapper>
     
    </ConsentListContainer>
  );
};

export default ConsentList;
