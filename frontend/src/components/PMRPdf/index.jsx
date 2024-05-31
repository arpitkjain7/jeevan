import React, { useEffect, useState } from "react";
// import {
//   Page,
//   Text,
//   Document,
//   StyleSheet,
//   View,
//   Font,
// } from "@react-pdf/renderer";
// import RedHatFont from "../../assets/fonts/Red_Hat_Display/static/RedHatDisplay-Regular.ttf";
// import SourceSansFont from "../../assets/fonts/source-sans-pro/SourceSansPro-Regular.otf";
// import SourceSansFontBold from "../../assets/fonts/source-sans-pro/SourceSansPro-Bold.otf";
import { convertDateFormat } from "../../utils/utils";
import PdfFromDocumentBytes from "../PdfFromDocumentBytes";
import { previewPMR } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import { useDispatch } from "react-redux";
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf';

// Font.register({ family: "Red Hat Display", src: RedHatFont });
// Font.register({ family: "Source Sans Pro", src: SourceSansFont });
// Font.register({ family: "Source Sans Pro Bold", src: SourceSansFontBold });

// const pmrPdfStyles = StyleSheet.create({
//   document: {
//     height: "100%",
//     width: "100%",
//   },
//   pdfContainer: {
//     padding: "8px 24px",
//   },
//   page: {
//     backgroundColor: "#FFFFFF",
//   },
//   pdfHeader: {
//     display: "flex",
//     flexDirection: "row",
//     flexDirection: "row",
//     justifyContent: "space-between",
//     backgroundColor: "#0089E9",
//     borderBottom: "1px solid #ffffff",
//     padding: "8px 16px",
//   },
//   pdfHeaderLogo: {
//     display: "flex",
//     flexDirection: "row",
//     flexDirection: "row",
//     gap: "16px",
//   },
//   pdflogoText: {
//     color: "#ffffff",
//     fontFamily: "Red Hat Display",
//     fontSize: "10px",
//     fontWeight: "400",
//     alignItems: "center"
//   },
//   pdfhospitalNameText: {
//     fontFamily: "Source Sans Pro",
//     color: "#ffffff",
//     fontSize: "16px",
//     fontWeight: "400",
//   },
//   pdfDrNameText: {
//     fontFamily: "Source Sans Pro",
//     color: "#ffffff",
//     fontSize: "16px",
//     fontWeight: "400",
//   },
//   pdfPatientDetails: {
//     backgroundColor: "#0089E9",
//     borderBottom: "1px solid #ffffff",
//     padding: "4px 16px",
//   },
//   pdfPatientNameText: {
//     fontFamily: "Source Sans Pro Bold",
//     color: "#ffffff",
//     fontSize: "20px",
//     fontWeight: "400",
//   },
//   pdfPatientName: {
//     display: "flex",
//     flexDirection: "row",
//     justifyContent: "space-between",
//   },
//   pdfOuterWrapper: {
//     display: "flex",
//     justifyContent: "space-between",
//     flexDirection: "row",
//     flexWrap: "wrap",
//   },
//   pdfPatientOtherDetailsWrapper: {
//     flexDirection: "row",
//     padding: "4px 0px",
//     backgroundColor: "#0089E9",
//     gap: "6px",
//   },
//   pdfDetailsWrapper: {},
//   pdfText: {
//     fontFamily: "Source Sans Pro Bold",
//     color: "#ffffff",
//     fontSize: "12px",
//     fontWeight: "400",
//     alignSelf: "flex-end"
//   },
//   pdfVitalsWrapper: {
//     display: "flex",
//     flexDirection: "row",
//     flexWrap: "wrap",
//     flexDirection: "row",
//     padding: "12px 0px",
//     gap: "6px",
//     width: "100%",
//   },
//   pdfVital: {
//     backgroundColor: "rgba(5, 97, 160, 0.08)",
//     padding: "8px",
//     minWidth: "24px",
//     flex: 1,
//   },
//   pdfPatientOtherDetails: {
//     backgroundColor: "rgba(255, 255, 255, 0.8)",
//     padding: "4px",
//     minWidth: "70px",
//   },
//   pdfPatientidText: {
//     fontFamily: "Source Sans Pro Bold",
//     color: "#ffffff",
//     fontSize: "12px",
//     fontWeight: "400",
//   },
//   dataLabel: {
//     fontFamily: "Source Sans Pro",
//     color: "#171717",
//     fontSize: "10px",
//     fontWeight: "400",
//     textTransform: "capitalize",
//   },
//   dataValue: {
//     fontFamily: "Source Sans Pro Bold",
//     color: "#171717",
//     fontSize: "12px",
//     fontWeight: "400",
//   },
//   dataTitle: {
//     fontFamily: "Source Sans Pro",
//     color: "#5A5A5A",
//     fontSize: "14px",
//     fontWeight: "400",
//     marginBottom: "8px",
//   },
//   table: {
//     display: "table",
//     width: "100%", // Take up full width
//     borderStyle: "solid",
//     borderWidth: 1,
//     borderColor: "#000",
//     paddingBottom: 5,
//   },
//   tableHeader: {
//     flexDirection: "row",
//     alignItems: "center",
//     backgroundColor: "rgba(0, 137, 233, 0.2)",
//   },
//   tableRow: {
//     flexDirection: "row",
//     alignItems: "center",
//     margin: "auto",
//   },
//   tableCell: {
//     width: "20%", // Distribute columns evenly
//     padding: 5,
//     textAlign: "center",
//     fontFamily: "Source Sans Pro Bold",
//     color: "#171717",
//     fontSize: "12px",
//     fontWeight: "400",
//   },
//   rowCell: {
//     width: "20%", // Distribute columns evenly
//     padding: 5,
//     textAlign: "center",
//     fontFamily: "Source Sans Pro",
//     color: "#171717",
//     fontSize: "12px",
//     fontWeight: "400",
//     wordWrap: "break-word"
//   },
//   rowText: {
//     fontFamily: "Source Sans Pro",
//     color: "#171717",
//     fontSize: "12px",
//     fontWeight: "400",
//   },
//   columnText: {
//     fontFamily: "Source Sans Pro Bold",
//     color: "#171717",
//     fontSize: "12px",
//     fontWeight: "400",
//   },
//   dataWrapper: {
//     display: "flex",
//     flexDirection: "row",
//     alignItems: "center",
//     gap: "8px",
//     flexWrap: "wrap",
//   },
//   dataBox: {
//     backgroundColor: "rgba(5, 97, 160, 0.08)",
//     padding: "4px 6px",
//     maxHeight: "50px",
//     minWidth: "100px",
//   },
//   subDataContainer: {
//     display: "flex",
//     flexDirection: "row",
//     alignItems: "center",
//     gap: "2px",
//   },
// });

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height
  };
}
function useWindowDimensions() {
const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());

useEffect(() => {
  function handleResize() {
    setWindowDimensions(getWindowDimensions());
  }

  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);
return windowDimensions;
}

const PMRPdf = ({ data, setIsFinishDisabled }) => {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const dispatch = useDispatch();
  const [currentPatientData, setCurrentPatientData] = useState([]);
  const pdfDate = convertDateFormat(new Date(), "dd/MM/yyyy");
  // const [prescriptionData, setPrescriptionData] = useState([]);
  const hospitalDetails = JSON.parse(sessionStorage.getItem("selectedHospital"));
  const patientData = JSON.parse(sessionStorage.getItem("selectedPatient"));
  const pdfData = JSON.parse(sessionStorage.getItem("patientEMRDetails"));
  const [open, setOpen] = useState(false);
  const { height, width } = useWindowDimensions();
  const isMobile = window.innerWidth < 600;

  const columns = [
    { key: "medicine_name", label: "Medications" },
    { key: "frequency", label: "Frequency" },
    { key: "duration", label: "Duration" },
    { key: "dosage", label: "Dosage" },
    { key: "notes", label: "Notes" },
  ];

  const transformPdfData = (inputObject) => {
    const resultArray = [];

    const sections = {
      vital: "Vitals",
      condition: "Conditions",
      examinationFindings: "Examination Findings",
      diagnosis: "Diagnosis",
      symptom: "Symptoms",
      medication: "Medications",
      currentMedication: "Current Medications",
      lab_investigation: "Lab Investigations",
      medical_history: "Medical History",
    };

    for (const section in sections) {
      if (
        inputObject[section] &&
        inputObject[section].data &&
        inputObject[section].data.length > 0
      ) {
        const heading = sections[section];
        let data = [];
        data = inputObject[section]?.data?.map((item) => {
          const labelData = Object.entries(item).map(([label, value]) => ({
            label,
            value,
          }));
          return labelData;
        });

        resultArray.push({ heading, data });
      }
    }

    return resultArray;
  };

  // const [pmrPdfData, setPmrPdfData] = useState([]);
  const pmrId = sessionStorage.getItem("pmrID");
  const [documentBytes, setDocumentBytes] = useState("");
  const [documentId, setDocumentId] = useState("");

  const handleClose = () => {
    setOpen(false);
  };
  useEffect(() => {
    if (Object.keys(patientData)?.length) {
      const patientDetails = [
        {
          label: "Gender",
          value: patientData?.patientGender,
        },
        {
          label: "Age",
          value: (patientData?.patientAgeInYears ? patientData?.patientAgeInYears + 'Y ' : "") +
          (patientData?.patientAgeInMonths ? patientData?.patientAgeInMonths + 'M' : ""),
        },
        {
          label: "Contact Number",
          value: patientData?.patientNumber,
        },
        {
          label: "Email",
          value: patientData?.patientEmail,
        },
      ];
      setCurrentPatientData(patientDetails);
    }
  }, []);

  const onDocumentLoadSuccess = (({ numPages }) => {
    setNumPages(numPages);
  });

  return (
    <div>
        {/* {!isMobile && documentBytes && (
          <embed style={{ width: "100%", height: height }} src={`data:application/pdf;base64,${documentBytes}`}/>
        )}
        {isMobile && documentBytes && pdfUrl !== null && (
        <Document file={pdfUrl} onLoadSuccess={onDocumentLoadSuccess} >
          {Array.apply(null, Array(numPages))
            .map((x, i)=>i+1)
            .map(page =>
              <Page wrap pageNumber={page} renderTextLayer={true} width={width} height="auto" />
          )}
        </Document>
        )} */}
    </div>
  );
};

export default PMRPdf;
