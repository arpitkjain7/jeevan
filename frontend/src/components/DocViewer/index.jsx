import React from "react";
import { List, ListItem, styled } from "@mui/material";
import { useState } from "react";
import MyTable from "../../components/TableComponent";
import RightArrow from "../../assets/arrows/arrow-right.svg";
import FhirDoc from "../FhirDoc";

const DocViewerContainer = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 6),
  [theme.breakpoints.down("sm")]: {
    padding: theme.spacing(0, 2),
  },
}));

const Views = styled("div")(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(8),
  padding: theme.spacing(8, 0),
  minHeight: "600px",
  flexDirection: "row",
  [theme.breakpoints.down("sm")]: {
    flexDirection: "column",
    gap: theme.spacing(2),
    padding: theme.spacing(2, 0),
  },
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
  [theme.breakpoints.down("sm")]: {
    height: "auto",
  },
}));

const SideList = styled(List)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(8),
  [theme.breakpoints.down("sm")]: {
    gap: theme.spacing(2),
  },
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
  const [consentError, setConsentError] = useState(false);
  const [showHealthReport, setShowHealthReport] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState(null);

  const columns = [
    { key: "careContext", header: "Care Context" },
    { key: "hipId", header: "HIP ID" },
    { key: "date", header: "Consultation Date" },
    {
      key: "actions",
      header: "",
      actions: [
        {
          type: "icon",
          icon: <img src={RightArrow} alt="details" />,
          onClick: (item) => {
            if (item.careContext) {
              setSelectedDoc(item.careContext);
              setShowHealthReport(true);
            } else {
              setConsentError(true);
            }
          },
        },
      ],
    },
  ];
  return (
    <DocViewerContainer>
      <Views>
        <SideList>
          {docData?.length
            ? docData?.map(
                (item, index) =>
                  item?.patient_name && (
                    <DiagnosisDetails
                      key={index}
                      className={
                        selectedDoc === item?.patient_name
                          ? "selected-vital"
                          : ""
                      }
                    >
                      <DocList>{item?.patient_name}</DocList>
                      <img src={RightArrow} alt={`select-${item.type}`} />
                    </DiagnosisDetails>
                  )
              )
            : ""}
          {docData?.length > 1 ? (
            <div className="table-container">
              <MyTable
                columns={columns}
                data={docData}
                tableClassName="table-class"
                searchClassName="search-class"
                highlightRowOnHover={true}
              />
            </div>
          ) : (
            <ErrorContainer>
              <h3>Data fetch still in progress, please try after some time</h3>
            </ErrorContainer>
          )}
        </SideList>
        {docData?.length && consentError ? (
          <ErrorContainer>
            <h3>Error retrieving health record</h3>
          </ErrorContainer>
        ) : (
          showHealthReport && (
            <PdfContainer>
              <FhirDoc selectedDoc={selectedDoc} />
            </PdfContainer>
          )
        )}
      </Views>
    </DocViewerContainer>
  );
};

export default DocViewer;
