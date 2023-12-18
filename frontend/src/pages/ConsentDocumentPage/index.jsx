import { styled } from "@mui/material";
import React, { useEffect, useState } from "react";
import DocViewer from "../../components/DocViewer";
import { fetchConsentDetails } from "../../components/ConsentList/consentList.slice";
import { useDispatch } from "react-redux";

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
  "&": theme.typography.h3,
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(2),
}));
const ConsentDocumentPage = () => {
  const [documentData, setDocumentData] = useState([]);
  const selectedConsent = sessionStorage.getItem("consentSelected");
  const [consentDetails, setConsentDetails] = useState([]);
  const [consentPatientId, setConsentPatientId] = useState("");
  const dispatch = useDispatch();

  const createDocumentData = (data) => {
    console.log(data);
    const doclist = [];
    // data?.map((item) => {
    //   console.log(item, "item");
    //   const docObj = {
    //     documentContent: item?.attachment?.data,
    //     type: item?.attachment?.contentType,
    //     id: item?.attachment?.id,
    //   };
    const pname = {patient_name: data?.patient};
    doclist.push(pname)
    const contexts = data?.care_contexts?.care_context;
     contexts?.map((item) => {
      const docObj = { careContext: item?.careContextReference, date: data?.created_at, hipId: data?.hip_id};
      doclist.push(docObj);
    });
    setDocumentData(doclist);
  };
  useEffect(() => {
    const currentConsent = JSON.parse(selectedConsent);
    if (currentConsent && Object.keys(currentConsent)?.length) {
      const consentId = currentConsent?.id;
      dispatch(fetchConsentDetails(consentId)).then((response) => {
        const consentData = response?.payload;
        console.log(consentData);
        setConsentPatientId(consentData?.care_contexts?.care_context[0]?.patientRefernce);
        const documentReference =
          consentData?.care_contexts?.care_context;
          // consentData?.patient_data_transformed[0]?.DocumentReference?.content;
        console.log(documentReference, "reference");
        createDocumentData(consentData);
      });
    }
  }, []);

  const details = [
    {
      label: "Request Status",
      value: "-",
    },
    {
      label: "Consent Created On",
      value: "-",
    },
    {
      label: "Consent Created On",
      value: "-",
    },
    {
      label: "Consent Enquiry On",
      value: "-",
    },
  ];

  return (
    <ConsentDocsContainer>
      <ConsentDetailsWrapper>
        {details?.map((item) => (
          <ConsentHeader>
            <ConsentLabel>{item?.label}</ConsentLabel>
            <ConsentValue>{item?.value}</ConsentValue>
          </ConsentHeader>
        ))}
      </ConsentDetailsWrapper>
      <DocViewer docData={documentData} />
    </ConsentDocsContainer>
  );
};

export default ConsentDocumentPage;
