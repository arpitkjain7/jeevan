import { Button, styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import MyTable from "../TableComponent";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { fetchConsentList } from "./consentList.slice";
import RightArrow from "../../assets/arrows/arrow-right.svg";
import ConsentModal from "../ConsentModal";
import { convertDateFormat } from "../../utils/utils";
import CustomLoader from "../CustomLoader";

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
      [theme.breakpoints.down("md")]: {
        "&": theme.typography.body2,
      },
    },
    "& .MuiTableBody-root": {
      "& > tr >td": theme.typography.body1,
      textTransform: "none",
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
const consentTableStyle = {
  backgroundColor: "#f1f1f1",
  // maxWidth: '600px'
  ".linkTypography": {
    textTransform: "none !important",
  },
};

const ConsentList = () => {
  const patient = sessionStorage?.getItem("selectedPatient");
  const [tableData, setTableData] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [showLoader, setShowLoader] = useState(false);
  const [render, setRender] = useState(false);

  useEffect(() => {
    sessionStorage.removeItem("consentSelected");
    setShowLoader(true);
    const currentPatient = JSON.parse(patient);
    if (currentPatient && Object.keys(currentPatient)?.length) {
      const patientId = currentPatient?.id;
      dispatch(fetchConsentList(patientId)).then((response) => {
        setShowLoader(false);
        const consentData = response?.payload;
        const formattedConsentList = consentData?.map((item) => {
          const createdAt = convertDateFormat(
            item?.created_at,
            "dd-MM-yyyy hh:mm aaaaa'm'"
          );
          const updatedAt = convertDateFormat(
            item?.updated_at,
            "dd-MM-yyyy hh:mm aaaaa'm'"
          );
          const expireAt = convertDateFormat(
            item?.expire_at,
            "dd-MM-yyyy hh:mm aaaaa'm'"
          );
          const fromDate = convertDateFormat(
            item?.date_range?.from,
            "dd-MM-yyyy hh:mm aaaaa'm'"
          );
          const toDate = convertDateFormat(
            item?.date_range?.to,
            "dd-MM-yyyy hh:mm aaaaa'm'"
          );
          const requested_Hi = item?.hi_type?.requested_hi_types
            ? item?.hi_type?.requested_hi_types.join(", ")
            : "";
          const granted_Hi = item?.hi_type?.granted_hi_types
            ? item?.hi_type?.granted_hi_types.join(", ")
            : "";
          const consentStatus = item?.status;
          return {
            consentStatus: consentStatus,
            createdAt: createdAt,
            updatedAt: updatedAt,
            expireAt: expireAt,
            fromDate: fromDate,
            toDate: toDate,
            requested_Hi: requested_Hi,
            granted_Hi: granted_Hi,
            ...item,
          };
        });
        setTableData(formattedConsentList);
      });
    }
  }, [dispatch, patient, render]);

  const columns = [
    { key: "abha_address", header: "ABHA Address" },
    { key: "createdAt", header: "Consent Created On" },
    { key: "consentStatus", header: "Consent Status" },
    { key: "updatedAt", header: "Consent Updated On" },
    { key: "fromDate", header: "Consent from Date" },
    { key: "toDate", header: "Consent to Date" },
    { key: "requested_Hi", header: "Requested HI Types" },
    { key: "granted_Hi", header: "Granted HI Types" },
    { key: "expireAt", header: "Consent Expiry On" },
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
    "Prescription",
    "Diagnostic Report",
    "OP Consultation",
    "Discharge Summary",
    "Immunization Record",
    "Record artifact",
    "Wellness Record",
  ];

  return (
    <ConsentListContainer>
      <CustomLoader open={showLoader} />
      <ButtonWrapper>
        <CustomButton
          onClick={handleModalOpen}
          sx={{ marginTop: { xs: " 20px", sm: "0px" } }}
        >
          Request Consent
        </CustomButton>
      </ButtonWrapper>
      <ConsentDataWrapper>
        <ConsentModal
          open={modalOpen}
          handleClose={handleModalClose}
          purposeOptions={purposeOptions}
          infoTypeOptions={infoTypeOptions}
          render={render}
          setRender={setRender}
        />
        <ConsentTableContainer>
          {tableData?.length && (
            <MyTable
              columns={columns}
              data={tableData}
              consentTableStyle={consentTableStyle}
              tableClassName="table-class"
              showSearch={false}
              tableStyle={{ cursor: "pointer" }}
              highlightRowOnHover={true}
              onRowClick={(item) => {
                sessionStorage.setItem("consentSelected", JSON.stringify(item));
                navigate("/consent-detail");
              }}
            />
          )}
        </ConsentTableContainer>
      </ConsentDataWrapper>
    </ConsentListContainer>
  );
};

export default ConsentList;
