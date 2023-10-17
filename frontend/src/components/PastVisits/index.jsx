import { List, styled } from "@mui/material";
import { PDFDownloadLink, PDFViewer } from "@react-pdf/renderer";
import React, { useEffect, useState } from "react";
import PMRPdf from "../PMRPdf";
import { fetchPMRList, fetchVistList, getDocument } from "./pastvisits.slice";
import { useDispatch, useSelector } from "react-redux";
import ArrowRight from "../../assets/arrows/arrow-right.svg";
import MyTable from "../TableComponent";
import { convertDateFormat } from "../../utils/utils";

const VisitsWrapper = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primaryWhite,
  padding: theme.spacing(0, 6),
}));
const Visits = styled("div")(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(4),
  padding: theme.spacing(8, 0),
}));
const SideList = styled("List")(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(8),
  height: "600px",
  overflow: "auto",
}));

const DiagnosisDetails = styled("ListItem")(({ theme }) => ({
  padding: theme.spacing(2, 4),
  borderRadius: theme.spacing(1),
  border: `1px solid ${theme.palette.primaryGrey}`,
}));

const PrescriptionDeatils = styled("div")(({ theme }) => ({
  flex: "1",
  backgroundColor: theme.palette.primaryGrey,
  height: "800px",
}));

const VitalsDetailsWrapper = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primaryWhite,
  padding: theme.spacing(0, 6),
}));
const VitalsDetailsContainer = styled("div")(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(4),
  padding: theme.spacing(8, 0),
}));

const VitalsList = styled("ListItem")(({ theme }) => ({}));
const VisitDate = styled("p")(({ theme }) => ({
  "&": theme.typography.customKeys,
  margin: "0",
}));
const Vitals = styled("div")(({ theme }) => ({
  flex: "1",
  backgroundColor: theme.palette.primaryWhite,
  borderRadius: theme.spacing(1),
  border: `1px solid ${theme.palette.primaryGrey}`,
}));
const VitalDetailsTable = styled("div")(({ theme }) => ({
  "&": {
    height: "600px",
    overflow: "auto",
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

const VitalsListContainer = styled("div")(({ theme }) => ({
  padding: theme.spacing(4),
  borderRadius: theme.spacing(1),
  border: `1px solid ${theme.palette.primaryGrey}`,
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  width: "250px",

  "&.selected-vital": {
    border: `1px solid ${theme.palette.primaryBlue}`,
  },
}));

const VisitListContainer = styled("div")(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(1),
  alignItems: "center",
}));

const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const PastVisits = () => {
  const [tableData, setTableData] = useState([]);
  const dataState = useSelector((state) => state);
  const dispatch = useDispatch();
  const patient = sessionStorage?.getItem("selectedPatient");
  const [visitList, setVisitList] = useState([]);
  const [pmrId, setPmrId] = useState("");
  const pdfFileName = "custom_filename.pdf";
  const selectVisit = (item) => {
    dispatch(fetchPMRList(item?.id)).then((res) => {
      const docsList = res.payload;
      console.log(docsList);
      setTableData(docsList);
    });
  };
  useEffect(() => {
    const currentPatient = JSON.parse(patient);
    if (currentPatient && Object.keys(currentPatient)?.length) {
      dispatch(fetchVistList(currentPatient?.id)).then((res) => {
        const pmrData = res.payload;
        setVisitList(pmrData);
      });
    }
  }, []);
  const columns = [
    { key: "id", header: "Document Id" },
    { key: "document_name", header: "Document Name" },
    { key: "created_at", header: "Uploaded Date" },
    { key: "document_type_code", header: "Document Code" },
  ];

  const openDoc = (row) => {
    dispatch(getDocument(row?.id)).then((res) => {
      const documentData = res.payload;
      window.open(documentData?.document_url, "_blank");
    });
  };

  return (
    <VisitsWrapper>
      <VitalsDetailsContainer>
        <SideList>
          {visitList.map((item) => (
            <VitalsListContainer
              className={pmrId === item?.id ? "selected-vital" : ""}
              onClick={() => selectVisit(item)}
            >
              <VisitListContainer>
                <VitalsList>Diagnosis</VitalsList>
                <VisitDate>
                  {convertDateFormat(item?.date_of_consultation, "dd-MM-yyyy")}
                </VisitDate>
              </VisitListContainer>

              <img
                src={ArrowRight}
                alt={`select-${item.date_of_consultation}`}
              />
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
              onRowClick={(row) => openDoc(row)}
            />
          </VitalDetailsTable>
        </Vitals>
      </VitalsDetailsContainer>
    </VisitsWrapper>
  );
};

export default PastVisits;
