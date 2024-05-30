import React, { useEffect } from "react";
// import pdfjs from "pdfjs-dist/build/pdf";
import { List, ListItem, styled } from "@mui/material";
import { useState } from "react";
import { useRef } from "react";
import MyTable from "../../components/TableComponent";
import ArrowRight from "../../assets/arrows/arrow-right.svg";
import HealthReport from "../HealthData";

const DocViewerContainer = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 6),
}));
const Views = styled("div")(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(8),
  padding: theme.spacing(8, 0),
  minHeight: "600px",
}));
const ErrorContainer = styled("div")(({ theme }) => ({
  display: "block",
  alignSelf: "center",
  textAlign: "center",
  color: "red",
}));
const PdfContainer = styled("div")(({ theme }) => ({
  flex: "1",
  height: "100%",
}));
const SideList = styled(List)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(8),
}));

const DiagnosisDetails = styled(ListItem)(({ theme }) => ({
  padding: theme.spacing(4),
  borderRadius: theme.spacing(1),
  border: `1px solid ${theme.palette.primaryGrey}`,
  // cursor: "pointer",
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",

  "&.selected-vital": {
    border: `1px solid ${theme.palette.primaryBlue}`,
  },
}));
const DocList = styled("p")(({ theme }) => ({
  margin: "0",
}));

const DocViewer = ({ docData }) => {
  const [byteCode, setByteCode] = useState("");
  const [selectedDocument, setSelectedDocument] = useState("");
  const pdfViewerRef = useRef(null);
  const onDocClick = (selectedItem) => {
    setByteCode(selectedItem?.documentContent);
    setSelectedDocument(selectedItem?.id);
  };
  const [pdfUrl, setPdfUrl] = useState(null);
  const [consentError, setConsentError] = useState(false);
  const convertToDoc = () => {};

  useEffect(() => {
    setByteCode(docData[0]?.documentContent);
  }, []);

  useEffect(() => {
    if (byteCode) {
      const decodedByteCode = atob(byteCode);
      const byteNumbers = new Array(decodedByteCode.length);
      for (let i = 0; i < decodedByteCode.length; i++) {
        byteNumbers[i] = decodedByteCode.charCodeAt(i);
      }
      const blob = new Blob([new Uint8Array(byteNumbers)], {
        type: "application/pdf",
      });

      const pdfUrl = URL.createObjectURL(blob);
      setPdfUrl(pdfUrl);
      return () => {
        URL.revokeObjectURL(pdfUrl);
      };
    }
  }, [byteCode]);

  const columns = [
    { key: "careContext", header: "Care Context" },
    { key: "hipId", header: "HIP ID" },
    { key: "date", header: "Created At" },
    {
      key: "actions",
      header: "",
      actions: [
        {
          link: <img src={ArrowRight} />,
          type: "link",
          onClick: () => {
            setConsentError(true);
            setTimeout(() => {
              setConsentError(false);
            }, 5000);
          },
        },
      ],
    },
  ];
  return (
    <DocViewerContainer>
      <Views>
        <SideList>
          {docData?.length &&
            docData?.map(
              (item) =>
                item?.patient_name && (
                  <DiagnosisDetails
                    // onClick={() => onDocClick(item)}
                    className={
                      selectedDocument === item?.patient_name
                        ? "selected-vital"
                        : ""
                    }
                  >
                    <DocList>{item?.patient_name}</DocList>
                    {/* <img src={ArrowRight} alt={`select-${item.type}`} /> */}
                  </DiagnosisDetails>
                )
            )}
          {docData?.length && (
            <div className="table-container">
              <MyTable
                columns={columns}
                data={docData}
                tableClassName="table-class"
                searchClassName="search-class"
              />
            </div>
          )}
        </SideList>
        {consentError && (
          <ErrorContainer>
            <h3>Error retrieving health record</h3>
          </ErrorContainer>
        )}
        <PdfContainer>
          <HealthReport />
        </PdfContainer>
      </Views>
    </DocViewerContainer>
  );
};

export default DocViewer;
