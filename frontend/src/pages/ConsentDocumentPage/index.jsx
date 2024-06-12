import { styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import DocViewer from "../../components/DocViewer";
import { fetchConsentDetails } from "../../components/ConsentList/consentList.slice";
import { useDispatch } from "react-redux";
import { convertDateFormat } from "../../utils/utils";

const ConsentDocsContainer = styled("div")(({ theme }) => ({
  padding: theme.spacing(8, 6),
}));

const ConsentDetailsWrapper = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  gap: theme.spacing(4),
  backgroundColor: theme.palette.primaryWhite,
  padding: theme.spacing(4.5, 6),
  marginBottom: theme.spacing(8),
}));

const ConsentHeader = styled("div")(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(2),
}));

const ConsentLabel = styled("div")(({ theme }) => ({
  "&": theme.typography.customKeys,
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(2),
}));
const ConsentValue = styled("div")(({ theme }) => ({
  "&": theme.typography.p,
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(2),
}));

const ConsentDocumentPage = (consentListData) => {
  const consentSelected = JSON.parse(sessionStorage.getItem("consentSelected"));
  const selectedPatient = JSON.parse(sessionStorage.getItem("selectedPatient"));
  const [documentData, setDocumentData] = useState([]);
  const selectedConsent = sessionStorage.getItem("consentSelected");
  const dispatch = useDispatch();

  const createDocumentData = (data) => {
    const doclist = [];
    const pname = { patient_name: selectedPatient?.name };
    doclist.push(pname);
    const contexts = data?.patientDataTransformed;
    if (contexts && typeof contexts === "object") {
      Object.entries(contexts).forEach(([key]) => {
        const docObj = {
          careContext: key,
          date: data?.patientDataTransformed?.[key]?.Composition[0]?.date,
          hipId: data?.hipId,
        };
        doclist.push(docObj);
      });
    }
    setDocumentData(doclist);
  };

  useEffect(() => {
    const currentConsent = JSON.parse(selectedConsent);
    if (currentConsent && Object.keys(currentConsent)?.length) {
      const consentId = currentConsent?.id;
      dispatch(fetchConsentDetails(consentId)).then((response) => {
        const consentData = response?.payload;
        const formattedConsentList = {
          consultationDate: consentData?.patient_data_transformed,
          hipId: consentData?.hip_id,
          patientDataTransformed: consentData?.patient_data_transformed,
        };
        createDocumentData(formattedConsentList);
        // console.log("consentData", formattedConsentList);
        sessionStorage.setItem(
          "FhirDocDetails",
          JSON.stringify(consentData?.patient_data_transformed)
        );
      });
    }
  }, [dispatch]);

  const details = [
    {
      key: "consentStatus",
      label: "Request Status",
      value: consentSelected?.status,
    },
    {
      key: "consentCreatedOn",
      label: "Consent Created On",
      value: convertDateFormat(consentSelected?.created_at, "dd-MM-yyyy"),
    },
    {
      key: "consentExpiryOn",
      label: "Consent Expiry On",
      value: convertDateFormat(consentSelected?.expire_at, "dd-MM-yyyy"),
    },
  ];

  return (
    <ConsentDocsContainer>
      <ConsentDetailsWrapper>
        {details?.map((item) => (
          <ConsentHeader key={item.key}>
            <ConsentLabel>{item.label}</ConsentLabel>
            <ConsentValue>{item.value}</ConsentValue>
          </ConsentHeader>
        ))}
      </ConsentDetailsWrapper>
      <DocViewer docData={documentData} />
    </ConsentDocsContainer>
  );
};

export default ConsentDocumentPage;
