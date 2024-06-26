import { PDFDownloadLink, PDFViewer } from "@react-pdf/renderer";
import React, { useEffect, useState } from "react";
import PMRPdf from "../PMRPdf";
import {
  fetchPMRList,
  fetchVistList,
  getDocument,
  getDocumentBytes,
} from "./pastvisits.slice";
import { useDispatch, useSelector } from "react-redux";
import ArrowRight from "../../assets/arrows/arrow-right.svg";
import MyTable from "../TableComponent";
import {
  List,
  ListItem,
  styled,
  Dialog,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Slide,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { convertDateFormat } from "../../utils/utils";
import PdfFromDocumentBytes from "../PdfFromDocumentBytes";
import CustomLoader from "../CustomLoader";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const VisitsWrapper = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primaryWhite,
  padding: theme.spacing(0, 6),
}));
const Visits = styled("div")(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(4),
  padding: theme.spacing(8, 0),
}));
const SideList = styled(List)(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(8),
  height: "100vh",
  overflow: "auto",
  [theme.breakpoints.up("sm")]: {
    flexDirection: "column",
  },
  [theme.breakpoints.down("sm")]: {
    gap: theme.spacing(4),
    height: "auto",
  },
}));

// const DiagnosisDetails = styled("ListItem")(({ theme }) => ({
//   padding: theme.spacing(2, 4),
//   borderRadius: theme.spacing(1),
//   border: `1px solid ${theme.palette.primaryGrey}`,
// }));

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

// const VitalsList = styled("listItem")(({ theme }) => ({}));
const VisitDate = styled("div")(({ theme }) => ({
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
    [theme.breakpoints.down("sm")]: {
      height: "auto",
      marginTop: "15px",
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
      "& > tr >td:active": {
        borderStyle: "inset",
        backgroundColor: "#bde4ff",
      },
      [theme.breakpoints.down("sm")]: {
        "& > tr >td": {
          padding: "10px",
        },
      },
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
  [theme.breakpoints.down("sm")]: {
    width: "auto",
  },

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

const PastVisits = ({ isPatientHistory }) => {
  const [tableData, setTableData] = useState([]);
  // const dataState = useSelector((state) => state);
  const [documentType, setDocumentType] = useState("");
  const [base64data, setbase64data] = useState("");
  const [open, setOpen] = useState(false);
  const dispatch = useDispatch();
  const patient = sessionStorage?.getItem("selectedPatient");
  const [visitList, setVisitList] = useState([]);
  const [documentPopup, setDocumentPopup] = useState(false);
  const [pmrId, setPmrId] = useState("");
  const [showLoader, setShowLoader] = useState(false);
  const isMobile = window.innerWidth < 600;
  // const pdfFileName = "custom_filename.pdf";

  const selectVisit = (item) => {
    dispatch(fetchPMRList(item?.id)).then((res) => {
      if (isMobile) {
        setDocumentPopup(true);
      }
      setPmrId(item?.id);
      const docsList = res.payload;
      const formattedDocsList = docsList?.map((item) => {
        const DocDate = convertDateFormat(
          item?.updated_at,
          "dd-MM-yyyy hh:mm aa"
        );
        return {
          document_date: DocDate,
          ...item,
        };
      });
      setTableData(formattedDocsList);
    });
  };
  useEffect(() => {
    setShowLoader(true);
    const currentPatient = JSON.parse(patient);
    if (currentPatient && Object.keys(currentPatient)?.length) {
      dispatch(
        fetchVistList(currentPatient?.patientId || currentPatient?.id)
      ).then((res) => {
        if (res.payload) {
          const pmrData = res.payload
            .sort((a, b) => {
              return (
                new Date(a.updated_at).getTime() -
                new Date(b.updated_at).getTime()
              );
            })
            .reverse();
          setVisitList(pmrData);
        }
      });
    }
    setShowLoader(false);
  }, []);
  const columns = [
    { key: "id", header: "Document Id" },
    {
      key: "actions",
      header: "Document Name",
      actions: [
        {
          // link: {document_name},
          key: "document_name",
          type: "link",
          onClick: (row) => {
            openDoc(row)
          },
        },
      ],
    },
    { key: "document_date", header: "Uploaded Date" },
    { key: "document_type_code", header: "Document Code" },
  ];

  const handleClose = () => {
    setOpen(false);
  };

  const handleDocPopupClose = () => {
    setDocumentPopup(false);
  };
  const openDoc = (row) => {
    // if(isPatientHistory){
    dispatch(getDocumentBytes(row?.id)).then((res) => {
      if (res.payload != undefined) {
        setDocumentType(row.document_mime_type);
        setbase64data(res?.payload.data);
        setOpen(true);
      } else {
        console.log("Error retrieving data");
      }
    });
    // } else {
    //   dispatch(getDocument(row?.id)).then((res) => {
    //     const documentData = res.payload;
    //     window.open(documentData?.document_url, "_blank");
    //   });
    // }
  };

  return (
    <VisitsWrapper>
      <CustomLoader
        open={showLoader}
      />
      <VitalsDetailsContainer>
        <SideList>
          {visitList.map((item, index) => (
            <VitalsListContainer
              className={pmrId === item?.id ? "selected-vital" : ""}
              onClick={() => selectVisit(item)}
              key={index}
            >
              <VisitListContainer>
                <ListItem>
                  {item?.diagnosis_name != ""
                    ? item?.diagnosis_name
                    : "Diagnosis"}
                </ListItem>
                <VisitDate>
                  <p>
                    {convertDateFormat(item?.updated_at, "dd-MM-yyyy")}
                  </p>
                  <Typography
                      style={{
                        color:
                          `${item?.consultation_status}` === "Completed"
                            ? "green"
                            : "red",
                      }}
                    >
                      {item?.consultation_status}
                  </Typography>
                </VisitDate>
              </VisitListContainer>
              <img
                src={ArrowRight}
                alt={`select-${item.date_of_consultation}`}
              />
            </VitalsListContainer>
          ))}
        </SideList>
        {!isMobile && (
          <Vitals>
            <VitalDetailsTable>
              <MyTable
                columns={columns}
                data={tableData}
                tableStyle={tableStyle}
                tableClassName="table-class"
                showSearch={false}
                // onRowClick={(row) => openDoc(row)}
              />
            </VitalDetailsTable>
          </Vitals>
        )}
        {isMobile && (
          <Dialog
            fullScreen
            open={documentPopup}
            onClose={handleDocPopupClose}
            TransitionComponent={Transition}
          >
            <AppBar sx={{ position: "relative" }}>
              <Toolbar>
                <Typography
                  sx={{ ml: 2, flex: 1 }}
                  variant="h6"
                  component="div"
                >
                  Document Details
                </Typography>
                <IconButton
                  edge="end"
                  color="inherit"
                  onClick={handleDocPopupClose}
                  aria-label="close"
                >
                  <CloseIcon />
                </IconButton>
              </Toolbar>
            </AppBar>
            <Vitals>
              <VitalDetailsTable>
                <MyTable
                  columns={columns}
                  data={tableData}
                  tableStyle={tableStyle}
                  tableClassName="table-class"
                  showSearch={false}
                  // onRowClick={(row) => openDoc(row)}
                />
              </VitalDetailsTable>
            </Vitals>
          </Dialog>
        )}
      </VitalsDetailsContainer>
      {base64data && (
        <PdfFromDocumentBytes
          open={open}
          handleClose={handleClose}
          documentType={documentType}
          docBytes={base64data}
        />
      )}
    </VisitsWrapper>
  );
};

export default PastVisits;
