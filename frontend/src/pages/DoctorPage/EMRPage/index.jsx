import React, { useEffect, useRef } from "react";
import AutoSearch from "../../../components/AutoSearch";
import PatientDetailsHeader from "../../../components/PatientDetailsHeader";
import {
  Typography,
  styled,
  TextField,
  Grid,
  Autocomplete,
  Modal,
  Box,
  Toolbar,
  IconButton,
} from "@mui/material";
import { TextareaAutosize as BaseTextareaAutosize } from "@mui/base/TextareaAutosize";
import { Delete, Assignment } from "@mui/icons-material";
import CloseIcon from "@mui/icons-material/Close";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  getEMRId,
  getPatientAuth,
  postEMR,
  searchVitalsDetails,
  syncPMR,
  verifyDemographics,
} from "./EMRPage.slice";
import { gatewayInteraction } from "../../PatientRegistration/PatientRegistration.slice";
import CustomAutoComplete from "../../../components/CustomAutoComplete";
import { PDFViewer, pdf } from "@react-pdf/renderer";
import PMRPdf from "../../../components/PMRPdf";
import { submitPdf } from "../../../components/PMRPdf/pmrPdf.slice";
import { useNavigate } from "react-router-dom";
import { calculateBMI, convertDateFormat } from "../../../utils/utils";
import CustomizedDialogs from "../../../components/Dialog";
import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf";
import CustomLoader from "../../../components/CustomLoader";
import { format } from "date-fns";
import SendPMR from "../SendPMR";
import CustomSnackbar from "../../../components/CustomSnackbar";

const isMobile = window.innerWidth < 1000;

const TextareaAutosize = styled(BaseTextareaAutosize)(
  ({ theme }) => `
  width: 320px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 0.875rem;
  font-weight: 400;
  line-height: 1.5;
  padding: 8px 12px;
  border-radius: 8px;

  // firefox
  &:focus-visible {
    outline: 0;
  }
`
);

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "350px",
  bgcolor: "background.paper",
  border: "1px solid #696969",
  boxShadow: 24,
  padding: "0 16px 16px",
};

const PatientEMRWrapper = styled("div")(({ theme }) => ({
  // position: "absolute",
  padding: "20px 10px 2px",
  [theme.breakpoints.down("sm")]: {
    padding: "10px 4px 0",
  },
}));

const EMRFormWrapper = styled("div")(({ theme }) => ({
  position: "absolute",
  paddingRight: "15px",
  [theme.breakpoints.down("sm")]: {
    paddingRight: "8px",
  },
}));
const EMRFormInnerWrapper = styled("div")(({ theme }) => ({
    // height: "500px",
    // overflow: "scroll",
}));

const VitalsContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    marginTop: theme.spacing(4),
    padding: theme.spacing(6),
    borderRadius: theme.spacing(1),
    [theme.breakpoints.down("sm")]: {
      padding: theme.spacing(4, 2),
    },
  },
  "& .notes-field": {
    "&.MuiFormControl-root": {
      width: "100%",
      "& > .MuiInputBase-root ": {
        minHeight: theme.spacing(43),
      },
    },
  },
  "& .textareaAutoSizeStyle": {
    height: "165px", 
    minHeight: "165px", 
    maxHeight: "165px", 
    width: "100%", 
    minWidth: "100%",
    maxWidth: "100%",
    [theme.breakpoints.down("sm")]: {
      maxWidth: "430px",
    },
  },
}));

const TextFieldWrapper = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    alignItems: "center",
  },
  ".emr-input-field": {
    "&.MuiFormControl-root  > .MuiInputBase-root": {
      height: "54px",
      borderRadius: "0",
    },
  },
}));

const BPTextFieldWrapper = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    alignItems: "center",
  },
}));

const VitalValue = styled("div")(({ theme }) => ({
  "&": {
    padding: theme.spacing(3.5),
    border: `1px solid ${theme.palette.primaryGrey}`,
    textAlign: "center",
  },
}));

const CommentSection = styled("div")(({ theme }) => ({
  "&": {
    padding: theme.spacing(3),
    border: `1px solid ${theme.palette.primaryGrey}`,
    textAlign: "center",
  },
}));
const FieldSpecsContainer = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    marginTop: theme.spacing(4),
    justifyContent: "space-between",
    gap: theme.spacing(4),
    [theme.breakpoints.down("sm")]: {
      gap: theme.spacing(2),
      alignItems: "center",
      border: "1px solid #ccccccb8",
      flexWrap: "wrap",
      padding: "2px",
    },
  },
}));

const EMRFooter = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginTop: theme.spacing(2),
    border: `1px solid ${theme.palette.primaryBlue}`,
    backgroundColor: "#b2d6f0",
    padding: theme.spacing(2, 8),
    position: "relative",
    bottom: 0,
    zIndex: 1,
  },
  [theme.breakpoints.down("sm")]: {
    padding: "8px 5px",
  },
}));

const PDFViewerWrapper = styled("div")(({ theme }) => ({
  height: "800px",
  marginBottom: "32px",
  flex: "1",
  [theme.breakpoints.down("md")]: {
    height: "auto",
    marginBottom: "0",
  },
}));

const PDFButtonWrapper = styled("div")(({ theme }) => ({
  display: "flex", 
  justifyContent: "center",
  gap: "16px", 
  position: "sticky", 
  bottom: 0,  
  border: `1px solid ${theme.palette.primaryBlue}`,
  backgroundColor: "#b2d6f0",
  padding: theme.spacing(2, 2),
  zIndex: 1,
}));

const PrimaryButton = styled("button")(({ theme }) => ({
  "&": theme.typography.primaryButton,
  float: "right",
  [theme.breakpoints.down("sm")]: {
    padding: "5px 7px",
  },
}));

const SecondaryButton = styled("button")(({ theme }) => ({
  "&": theme.typography.secondaryButton,
  [theme.breakpoints.down("sm")]: {
    padding: "5px 10px",
  },
}));

const SectionHeader = styled(Typography)(({ theme }) => ({
  "&": theme.typography.sectionBody,
  marginBottom: theme.spacing(4),
}));

const RecordLayout = styled("div")(({ theme }) => ({
  textAlign: "left",
  padding: theme.spacing(3, 4),
  border: `1px solid ${theme.palette.primaryGrey}`,
  flex: 1,
  // height: theme.spacing(13),
  borderRadius: theme.spacing(1.5),
  height: "min-content",
  [theme.breakpoints.down("sm")]: {
    height: "max-content",
    padding: "10px 8px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },
  "&.addMinWidth": {
    [theme.breakpoints.down("sm")]: {
      minWidth: "90px",
    },
  },
}));

const TextBoxLayout = styled("div")(({ theme }) => ({
  flex: 1,
  "&.desktopTextBoxLayout": {
    [theme.breakpoints.down("sm")]: {
      display: "none",
    },
  },
  "&.mobileTextBoxLayout": {
    [theme.breakpoints.up("sm")]: {
      display: "none",
    },
    "&.frequencyInput": {
      minWidth: "90px",
    },
  },
  "&.addMinWidth": {
    [theme.breakpoints.down("sm")]: {
      minWidth: "90px",
      ".MuiOutlinedInput-root": {
        padding: "6px",
      },
    },
  },
  ".MuiAutocomplete-input": {
    textOverflow: "clip",
  },
  "& .textareaAutoSizeStyle": {
    minWidth: "100%",
    maxWidth: "100%",
    maxHeight: "81px",
  },
}));

const RecordTextField = styled(TextField)(({ theme }) => ({
  width: "100%",
}));

const NotesWrapper = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
  },
  ".desktop": {
    [theme.breakpoints.down("sm")]: {
      display: "none",
    },
  },
}));

const DeleteWrapper = styled("div")(({ theme }) => ({
  flex: 1,
  display: "flex",
  alignItems: "center",
  ".mobile": {
    display: "flex",
    [theme.breakpoints.up("sm")]: {
      display: "none",
    },
  },
}));

const SelectedRecord = styled(Typography)(({ theme }) => ({
  "&": theme.typography.body1,
  marginBottom: theme.spacing(4),
  marginBottom: "0",
  [theme.breakpoints.down("sm")]: {
    marginBottom: "0",
  },
}));

const NotesField = styled(Assignment)(({ theme }) => ({
  height: "30px",
  width: "30px",
}));

const DeleteField = styled(Delete)(({ theme }) => ({
  height: "30px",
  width: "30px",
}));

const PageTitle = styled(Typography)(({ theme }) => ({
  "&": theme.typography.h1,
  marginBottom: theme.spacing(2),
}));
const PageSubText = styled(Typography)(({ theme }) => ({
  "&": theme.typography.h2,
  marginBottom: theme.spacing(8),
}));

const PdfDisplayWrapper = styled("div")(({ theme }) => ({
  // display: "flex",
  // alignItems: "center",
  // gap: theme.spacing(10),
}));

const BPWrapper = styled("div")(({ theme }) => ({
  display: "flex",
  border: "1px solid rgba(0,0,0,0.23)",
  height: "51px",
  textAlign: "center",
}));
const RowWrapper = styled("div")(({ theme }) => ({
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  padding: theme.spacing(4),
}));
const DiastolicTextField = styled(TextField)(({ theme }) => ({
  "&.MuiFormControl-root > .MuiInputBase-root > fieldset": {
    border: "none",
  },
}));

const SystolicTextField = styled(TextField)(({ theme }) => ({
  "&.MuiFormControl-root > .MuiInputBase-root > fieldset": {
    border: "none",
  },
}));

const Divider = styled("div")(({ theme }) => ({
  padding: "10px",
  display: "flex",
  alignItems: "center",
  fontSize: "18px",
  fontWeight: "bold",
}));

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height,
  };
}
function useWindowDimensions() {
  const [windowDimensions, setWindowDimensions] = useState(
    getWindowDimensions()
  );

  useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  return windowDimensions;
}

const PatientEMRDetails = (props) => {
  const { height, width } = useWindowDimensions();
  const [existingConditionsOpts, setExistingConditionOpts] = useState([]);
  const [symptomsOpts, setSymptomsOpts] = useState([]);
  const [examFindingsOpts, setExamFindingsOpts] = useState([]);
  const [diagnosisOpts, setDiagnosisOpts] = useState([]);
  const [medicationsOpts, setMedicationsOpts] = useState([]);
  const [labInvestigationsOpts, setLabInvestigationsOpts] = useState([]);
  const [medicalHistoryOpts, setMedicalHistoryOpts] = useState([]);
  const [existingConditions, setExistingCondition] = useState([]);
  const [symptoms, setSymptoms] = useState([]);
  const [medicalHistory, setMedicalHistory] = useState([]);
  const [examFindings, setExamFinding] = useState([]);
  const [diagnosis, setDiagnosis] = useState([]);
  const [medications, setMedications] = useState([]);
  const [labInvestigation, setLabInvestigation] = useState([]);
  const [prescriptionComment, setPrescriptionComment] = useState("");
  const [advices, setAdvices] = useState("");
  const [showSeveritySymptomps, setShowSeveritySymptomps] = useState(false);
  const [showMedicalHistory, setShowMedicalHistory] = useState(false);
  const [optionTextValues, setOptionTextValues] = useState({});
  const [existingConditionSpecs, setExistingConditionsSpecs] = useState({});
  const [symptomsSpecs, setSymptomsSpecs] = useState({});
  const [medicalHistorySpecs, setMedicalHistorySpecs] = useState({});
  const [examinationSpecs, setExaminationSpecs] = useState({});
  const [diagnosisSpecs, setDiagnosisSpecs] = useState({});
  const [medicationsSpecs, setMedicationsSpecs] = useState({});
  const [labInvestigationSpecs, setLabInvestigationSpecs] = useState({});
  const [bodyMassIndex, setBodyMassIndex] = useState("");
  const medicalHistoryRef = useRef();
  const patient = sessionStorage?.getItem("selectedPatient");
  const [pmrFinished, setPmrFinished] = useState(false);
  const [pdfData, setPdfData] = useState({});
  const [submitEMRPayload, setSubmitEMRPayload] = useState({});
  const dataState = useSelector((state) => state);
  const [patientData, setPatientData] = useState({});
  const [step, setStep] = useState("create");
  const [number, setNumber] = useState("");
  const [symptomNumber, setSymptomNumber] = useState("");
  const [medicalHistoryNumber, setMedicalHistoryNumber] = useState("");
  const [dose, setDose] = useState("");
  const [documents, setDocuments] = useState(true);
  const navigate = useNavigate();
  const currentPatient = JSON.parse(patient);
  const [emrId, setEMRId] = useState("");
  const [showLoader, setShowLoader] = useState(false);
  const [cleared, setCleared] = useState(false);
  const [symptomOptions, setSymptomOptions] = useState("");
  const [medicalHistoryOptions, setMedicalHistoryOptions] = useState("");
  const [diagnosisOptions, setDiagnosisOptions] = useState("");
  const [examinationFindingOptions, setExaminationFindingOptions] = useState("");
  const [medicationOptions, setMedicationOptions] = useState("");
  const [labInvestigationOptions, setLabInvestigationOptions] = useState("");
  const [notifyModal, setNotifyModal] = useState(false);
  const [documentId, setDocumentId] = useState("");
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const userRole = sessionStorage?.getItem("userRole");
  const [formValues, setFormValues] = useState({
    pulseRate: "",
    oxygenSaturation: "",
    bloodPressure: "",
    respiratoryRate: "",
    bodyTemp: "",
    bodyHeight: "",
    bodyWeight: "",
    bodyMass: "",
    systolicBP: "",
    diastolicaBP: "",
  });
  const [followUp, setFollowUp] = useState("");
  const [pmrDialogOpen, setPmrDialogOpen] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [functionCalled, setFunctionCalled] = useState(false); 
  const [gatewayRequestId, setGatewayRequestId]= useState("");
  
  useEffect(() => { 
    console.log(retryCount, "retryCount", functionCalled);
    if (functionCalled && retryCount < 4) { 
      const fetchGatewayData = async () => { 
          try { 
            console.log("gatewayRequestId", gatewayRequestId);
            dispatch(gatewayInteraction(gatewayRequestId)).then(response => {
              console.log("gateway response", response);
              if(response?.error && Object.keys(response?.error)?.length > 0) {
                setShowSnackbar(true);
                return;
              }
              else if(response?.payload?.request_status === "SUCESS"){
                setFunctionCalled(false);
                setNotifyModal(true);
              } else {
                // if (retryCount < 4) { 
                  setTimeout(() => {
                    fetchGatewayData()
                    setRetryCount(retryCount + 1); 
                  }, 5000);
                // } else {
                //   setShowSnackbar(true);
                //   setFunctionCalled(false);
                //   return;
                // }
              }
            })
          } catch (error) { console.error(error); } 
      };
      fetchGatewayData();
    } else if (functionCalled && retryCount > 4) {
      setShowSnackbar(true);
      setFunctionCalled(false);
      // return;
    }
}, [retryCount, functionCalled]); 

  useEffect(() => {
    if (cleared) {
      const timeout = setTimeout(() => {
        setCleared(false);
      }, 1500);

      return () => clearTimeout(timeout);
    }
    return () => {};
  }, [cleared]);

  const handlePmrDialogClose = () => {
    setPmrDialogOpen(false);
  };
  const dispatch = useDispatch();
  const [initialWidth, setInitialWidth] = useState(null);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  useEffect(() => {
    setShowLoader(true);
    // const queryParams = {
    //   term: "hea",
    //   state: "active",
    //   semantictag: "finding",
    //   acceptability: "preferred",
    //   returnlimit: 15,
    // };

    // dispatch(searchVitalsDetails(queryParams)).then((res) => {
    //   console.log("vitals:", res);
    // });

    // if (!sessionStorage.getItem("pmrID")) {
    const currentPatient = JSON.parse(patient);
    if (Object.keys(currentPatient)?.length) {
      const emrPayload = {
        patient_id: currentPatient?.patientId,
        doc_id: currentPatient?.doc_id,
        appointment_id: currentPatient?.id,
        hip_id: currentPatient?.hip_id,
        consultation_status: "InProgress",
      };
      dispatch(getEMRId(emrPayload)).then((res) => {
        setShowLoader(false);
        setEMRId(res.payload?.pmr_details.id);
        sessionStorage.setItem("pmrID", res.payload?.pmr_details.id);
        const pmrDetails = res.payload?.pmr_details.pmr_data;
        setAdvices(res.payload?.pmr_details?.advices);
        setPrescriptionComment(res.payload?.pmr_details?.notes);       
        // { res.payload?.appointment_details?.followup_date !== null ? 
        //   setFollowUp(dayjs(res.payload?.appointment_details?.followup_date)) : setFollowUp(null)
        // }
        setFollowUp(res.payload?.appointment_details?.followup_date);
        if (pmrDetails) {
          if (pmrDetails.vital) {
            setFormValues({
              pulseRate: pmrDetails.vital.pulse,
              oxygenSaturation: pmrDetails.vital.oxygen_saturation,
              bloodPressure: pmrDetails.vital.blood_pressure,
              respiratoryRate: pmrDetails.vital.respiratory_rate,
              bodyTemp: pmrDetails.vital.body_temperature,
              bodyHeight: pmrDetails.vital.height,
              bodyWeight: pmrDetails.vital.weight,
              bodyMass: pmrDetails.vital.body_mass_index,
              systolicBP: pmrDetails.vital.systolic_blood_pressure,
              diastolicaBP: pmrDetails.vital.diastolic_blood_pressure,
            });
          }
          if (pmrDetails.symptom.data.length > 0) {
            const symptomList = pmrDetails?.symptom.data;
            symptomList.map((symptomsData) => {
              setSymptoms((symptoms) => [
                ...symptoms,
                {
                  label: symptomsData.symptom,
                  value: symptomsData.symptom,
                  snowmed_code: symptomsData.snowmed_code,
                  snowmed_display: symptomsData.snowmed_display,
                },
              ]);
              setSymptomsSpecs((prevState) => ({
                ...prevState,
                [symptomsData.symptom]: {
                  since: symptomsData.duration || null,
                  severity: symptomsData.severity,
                  notes: symptomsData.notes,
                },
              }));
            });
          }
          if (pmrDetails.medical_history.data.length > 0) {
            const medicalHistoryList = pmrDetails?.medical_history.data;
            medicalHistoryList.map((medicalHistoryData) => {
              setMedicalHistory((medicalHistory) => [
                ...medicalHistory,
                {
                  label: medicalHistoryData.medical_history,
                  value: medicalHistoryData.medical_history,
                  snowmed_code: medicalHistoryData.snowmed_code,
                  snowmed_display: medicalHistoryData.snowmed_display,
                },
              ]);
              setOptionTextValues((prevState) => ({
                ...prevState,
                [medicalHistoryData.medical_history]: {
                  since: medicalHistoryData.since || null,
                  relationship: medicalHistoryData.relationship,
                  severity: medicalHistoryData.severity,
                  notes: medicalHistoryData.notes,
                },
              }));
            });
          }
          if (pmrDetails.examination_findings.data.length > 0) {
            const examinationFindingsList =
              pmrDetails?.examination_findings.data;
            examinationFindingsList.map((findingsData) => {
              setExamFinding((examFindings) => [
                ...examFindings,
                {
                  label: findingsData.disease,
                  value: findingsData.disease,
                  snowmed_code: findingsData.snowmed_code,
                  snowmed_display: findingsData.snowmed_display,
                },
              ]);
              setExaminationSpecs((prevState) => ({
                ...prevState,
                [findingsData.disease]: {
                  notes: findingsData.notes,
                },
              }));
            });
          }
          if (pmrDetails.diagnosis.data.length > 0) {
            const diagnosisList = pmrDetails?.diagnosis.data;
            diagnosisList.map((diagnosisData) => {
              setDiagnosis((diagnosis) => [
                ...diagnosis,
                {
                  label: diagnosisData.disease,
                  value: diagnosisData.disease,
                  snowmed_code: diagnosisData.snowmed_code,
                  snowmed_display: diagnosisData.snowmed_display,
                },
              ]);
              setDiagnosisSpecs((prevState) => ({
                ...prevState,
                [diagnosisData.disease]: {
                  since: diagnosisData.status || null,
                  severity: diagnosisData.diagnosis_type,
                  notes: diagnosisData.notes,
                },
              }));
            });
          }
          if (pmrDetails.lab_investigation.data.length > 0) {
            const labInvestigationList = pmrDetails?.lab_investigation.data;
            labInvestigationList.map((labInvestigationData) => {
              setLabInvestigation((labInvestigation) => [
                ...labInvestigation,
                {
                  label: labInvestigationData.name,
                  value: labInvestigationData.name,
                  snowmed_code: labInvestigationData.snowmed_code,
                  snowmed_display: labInvestigationData.snowmed_display,
                },
              ]);
              setLabInvestigationSpecs((prevState) => ({
                ...prevState,
                [labInvestigationData.name]: {
                  notes: labInvestigationData.notes,
                },
              }));
            });
          }
          if (pmrDetails.medication.data.length > 0) {
            const medicationList = pmrDetails?.medication?.data;
            medicationList.map((medicationData) => {
              setMedications((medications) => [
                ...medications,
                {
                  label: medicationData.medicine_name,
                  value: medicationData.medicine_name,
                  snowmed_code: medicationData.snowmed_code,
                  snowmed_display: medicationData.snowmed_display,
                },
              ]);
              setMedicationsSpecs((prevState) => ({
                ...prevState,
                [medicationData.medicine_name]: {
                  severity: medicationData?.frequency,
                  timing: medicationData?.time_of_day,
                  dose: medicationData?.dosage,
                  since: medicationData?.duration,
                  notes: medicationData?.notes
                },
              }));
            });
          }
        }
      });
    }
    // }
  }, []);
  
  useEffect(() => {
    if (symptomOptions.length >= 2) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: symptomOptions,
        state: "active",
        semantictag: "finding",
        acceptability: "all",
        groupbyconcept: "true",
        returnlimit: 15,
      };

      dispatch(searchVitalsDetails(queryParams)).then((res) => {
        const customData = [];
        const resData = res.payload?.data;
        if(resData.length > 0){
          resData?.map((item) => {
            const customItem = {
              label: item?.term,
              value: item?.term,
              snowmed_code: item?.conceptId,
              snowmed_display: item?.conceptFsn,
            };
            customData.push(customItem);
          });
          setSymptomsOpts(customData);
        } else {
          const customItem = {
            label: symptomOptions,
            value: symptomOptions,
            snowmed_code: "",
            snowmed_display: "",
          };
          customData.push(customItem);
          setSymptomsOpts(customData);
        }
      });
    } else {
      setSymptomsOpts([]);
    }
  }, [symptomOptions])

  useEffect(() => {
    if (medicalHistoryOptions.length >= 2) {
      const queryParams = {
        term: medicalHistoryOptions,
        state: "active",
        semantictag: "situation",
        acceptability: "all",
        returnlimit: 15,
      };
      dispatch(searchVitalsDetails(queryParams)).then((res) => {
        const customData = [];
        const resData = res.payload?.data;
        if(resData.length > 0){
          resData?.map((item) => {
            const customItem = {
              label: item?.term,
              value: item?.term,
              snowmed_code: item?.conceptId,
              snowmed_display: item?.conceptFsn,
            };
            customData.push(customItem);
          });
          setMedicalHistoryOpts(customData);
        } else {
          const customItem = {
            label: medicalHistoryOptions,
            value: medicalHistoryOptions,
            snowmed_code: "",
            snowmed_display: "",
          };
          customData.push(customItem);
          setMedicalHistoryOpts(customData);
        }
      });
    } else {
      setMedicalHistoryOpts([]);
    }
  }, [medicalHistoryOptions])

  useEffect(() => {
    if (examinationFindingOptions.length >= 2) {
      const queryParams = {
        term: examinationFindingOptions,
        state: "active",
        semantictag: "finding++observable entity++morphologic abnormality",
        acceptability: "all",
        groupbyconcept: "true",
        returnlimit: 15,
      };

      dispatch(searchVitalsDetails(queryParams)).then((res) => {
        const customData = [];
        const resData = res.payload?.data;
        if(resData.length > 0){
          resData?.map((item) => {
            const customItem = {
              label: item?.term,
              value: item?.term,
              snowmed_code: item?.conceptId,
              snowmed_display: item?.conceptFsn,
            };
            customData.push(customItem);
          });
          setExamFindingsOpts(customData);
        } else {
          const customItem = {
            label: examinationFindingOptions,
            value: examinationFindingOptions,
            snowmed_code: "",
            snowmed_display: "",
          };
          customData.push(customItem);
          setExamFindingsOpts(customData);
        }
      });
    } else {
      setExamFindingsOpts([]);
    }
  }, [examinationFindingOptions])

  useEffect(() => {
    if (diagnosisOptions.length >= 2) {
      const queryParams = {
        term: diagnosisOptions,
        state: "active",
        semantictag: "disorder",
        acceptability: "all",
        groupbyconcept: "true",
        returnlimit: 15,
      };

      dispatch(searchVitalsDetails(queryParams)).then((res) => {
        const customData = [];
        const resData = res.payload?.data;
        if(resData.length > 0){
          resData?.map((item) => {
            const customItem = {
              label: item?.term,
              value: item?.term,
              snowmed_code: item?.conceptId,
              snowmed_display: item?.conceptFsn,
            };
            customData.push(customItem);
          });
          setDiagnosisOpts(customData);
        } else {
          const customItem = {
            label: diagnosisOptions,
            value: diagnosisOptions,
            snowmed_code: "",
            snowmed_display: "",
          };
          customData.push(customItem);
          setDiagnosisOpts(customData);
        }
      });
    } else {
      setDiagnosisOpts([]);
    }
  }, [diagnosisOptions])

  useEffect(() => {
    if (labInvestigationOptions.length >= 2) {
      const queryParams = {
        term: labInvestigationOptions,
        state: "active",
        semantictag: "procedure",
        acceptability: "all",
        groupbyconcept: "true",
        returnlimit: 15,
      };

      dispatch(searchVitalsDetails(queryParams)).then((res) => {
        const customData = [];
        const resData = res.payload?.data;
        if(resData.length > 0){
          resData?.map((item) => {
            const customItem = {
              label: item?.term,
              value: item?.term,
              snowmed_code: item?.conceptId,
              snowmed_display: item?.conceptFsn,
            };
            customData.push(customItem);
          });
          setLabInvestigationsOpts(customData);
        } else {
          const customItem = {
            label: labInvestigationOptions,
            value: labInvestigationOptions,
            snowmed_code: "",
            snowmed_display: "",
          };
          customData.push(customItem);
          setLabInvestigationsOpts(customData);
        }
      });
    } else {
      setLabInvestigationsOpts([]);
    }
  }, [labInvestigationOptions])

  useEffect(() => {
    if (medicationOptions.length >= 2) {
      const queryParams = {
        term: medicationOptions,
        state: "active",
        semantictag: "real clinical drug++substance++product name",
        acceptability: "all",
        groupbyconcept: "true",
        returnlimit: 15,
      };

      dispatch(searchVitalsDetails(queryParams)).then((res) => {
        const customData = [];
        const resData = res.payload?.data;
        if(resData.length > 0){
          resData?.map((item) => {
            const customItem = {
              label: item?.term,
              value: item?.term,
              snowmed_code: item?.conceptId,
              snowmed_display: item?.conceptFsn,
            };
            customData.push(customItem);
          });
          setMedicationsOpts(customData);
        } else {
          const customItem = {
            label: medicationOptions,
            value: medicationOptions,
            snowmed_code: "",
            snowmed_display: "",
          };
          customData.push(customItem);
          setMedicationsOpts(customData);
        }
      });
    } else {
      setMedicationsOpts([]);
    }
  }, [medicationOptions])

  const handleMeidcalHistoryChange = async (event) => {
    setTimeout(() => {
      setMedicalHistoryOptions(event.target.value); 
    }, 1000);
  };
  const handleExistingConditionsChange = async (event) => {
    const inputValue = event.target.value;

    if (inputValue.length >= 2) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: inputValue,
        state: "active",
        semantictag: "finding",
        acceptability: "preferred",
        returnlimit: 15,
      };

      dispatch(searchVitalsDetails(queryParams)).then((res) => {
        const customData = [];
        const resData = res.payload?.data;
        resData?.map((item) => {
          const customItem = {
            label: item?.term,
            value: item?.term,
            snowmed_code: item?.conceptId,
            snowmed_display: item?.conceptFsn,
          };
          customData.push(customItem);
        });
        setExistingConditionOpts(customData);
      });
    } else {
      setExistingConditionOpts([]);
    }
  };
  const handleSymptompsChange = async (event) => {
    setTimeout(() => {
      setSymptomOptions(event.target.value);
    }, 1000)
  };
  const handleExamFindingsChange = async (event) => {
    setTimeout(() => {
      setExaminationFindingOptions(event.target.value);
    }, 1000)
  };
  const handleDiagnosisChange = async (event) => {
    setTimeout(() => {
      setDiagnosisOptions(event.target.value);
    }, 1000)
  };
  const handleMedicationsChange = async (event) => {
    setTimeout(() => {
      setMedicationOptions(event.target.value);
    }, 1000)
  };
  const handleLabInvestigationsChange = async (event) => {
    setTimeout(() => {
      setLabInvestigationOptions(event.target.value);
    }, 1000)
  };

  const clearMedicalHistoryOptions = (event) => {
    setMedicalHistoryOpts([]);
  }
  const handleMedicalHistoryValue = (event, value) => {
    if (value) {
      // setShowMedicalHistory(true);
      const fieldValue = value;
      setOptionTextValues({
        ...optionTextValues,
        [value?.label || value]: {
          since: "",
          relationship: "",
          severity: "",
          notes: "",
        },
      });
      if(value?.label){
        setMedicalHistory([...medicalHistory, fieldValue]);
      } else {
        setMedicalHistory((medicalHistory) => [...medicalHistory, {
          label: fieldValue,
          value: fieldValue,
          snowmed_code: "",
          snowmed_display: "",
        }]);
      }
      setMedicalHistoryOpts([]);
    }
  };
  const handleExistingConditions = (event, value) => {
    if (value) {
      const fieldValue = value;
      setExistingConditionsSpecs({
        ...existingConditionSpecs,
        [value?.label]: { since: "", severity: "", notes: "" },
      });
      setExistingCondition([...existingConditions, fieldValue]);
    }
  };
  const clearSymptomsOptions = (event) => {
    setSymptomsOpts([]);
  }
  const handleSymptoms = (event, value) => {
    if (value) {
      const fieldValue = value;
      setSymptomsSpecs({
        ...symptomsSpecs,
        [value?.label || value]: { since: "", severity: "", notes: "" },
      });
      if(value?.label){
        setSymptoms([...symptoms, fieldValue]);
      } else {
        setSymptoms((symptoms) => [...symptoms, {
          label: fieldValue,
          value: fieldValue,
          snowmed_code: "",
          snowmed_display: "",
        }]);
      }
      setSymptomsOpts([]);
    }
  };
  // const handleMedicalHistory = (event, value) => {
  //   if (value) {
  //     const fieldValue = value;
  //     setMedicalHistorySpecs({
  //       ...medicalHistorySpecs,
  //       [value]: { since: "", severity: "", notes: "" },
  //     });
  //     setMedicalHistory([...medicalHistory, fieldValue]);
  //   }
  // };
  const clearExaminationFindingOptions = (event) => {
    setExamFindingsOpts([]);
  }
  const handleExaminationFindings = (event, value) => {
    if (value) {
      const fieldValue = value;
      setExaminationSpecs({
        ...symptomsSpecs,
        [value?.label || value]: { notes: "" },
      });

      if(value?.label){
        setExamFinding([...examFindings, fieldValue]);
      } else {
        setExamFinding((examFindings) => [...examFindings, {
          label: fieldValue,
          value: fieldValue,
          snowmed_code: "",
          snowmed_display: "",
        }]);
      }
      // handleExaminationTextChange(value, "notes", "");
      setExamFindingsOpts([]);
    }
  };
  const clearDiagnosisOptions = (event) => {
    setDiagnosisOpts([]);
  }
  const handleDiagnosis = (event, value) => {
    if (value) {
      const fieldValue = value;
      setDiagnosisSpecs({
        ...diagnosisSpecs,
        [value?.label || value]: { since: "", severity: "", notes: "" },
      });

      if(value?.label){
        setDiagnosis([...diagnosis, fieldValue]);
      } else {
        setDiagnosis((diagnosis) => [...diagnosis, {
          label: fieldValue,
          value: fieldValue,
          snowmed_code: "",
          snowmed_display: "",
        }]);
      }
      setDiagnosisOpts([]);
    }
  };
  const clearMedicationOptions = (event) => {
    setMedicationsOpts([]);
  }
  const handleMedications = (event, value) => {
    if (value) {
      const fieldValue = value;
      setMedicationsSpecs({
        ...medicationsSpecs,
        [value?.label || value]: { since: "", severity: "", notes: "" },
      });
     
      if(value?.label){
        setMedications([...medications, fieldValue]);
      } else {
        setMedications((medications) => [...medications, {
          label: fieldValue,
          value: fieldValue,
          snowmed_code: "",
          snowmed_display: "",
        }]);
      }
      setMedicationsOpts([]);
    }
  };
  const clearLabInvestigationOptions = (event) => {
    setLabInvestigationsOpts([]);
  }
  const handleLabInvestigations = (event, value) => {
    if (value) {
      const fieldValue = value;
      setLabInvestigationSpecs({
        ...labInvestigationSpecs,
        [value?.label || value]: { since: "", severity: "", notes: "" },
      });
      
      if(value?.label){
        setLabInvestigation([...labInvestigation, fieldValue]); 
      } else {
        setLabInvestigation((labInvestigation) => [...labInvestigation, {
          label: fieldValue,
          value: fieldValue,
          snowmed_code: "",
          snowmed_display: "",
        }]);
      }
      // handleLabTextChange(value, "notes", "");
      setLabInvestigationsOpts([]);
    }
  };

  const prescriptionCommentChange = (event) => {
    setPrescriptionComment(event.target.value);
  };

  const adviceChange = (event) => {
    setAdvices(event.target.value);
  };

  const handleTextFieldChange = (option, textField, newValue) => {
    setOptionTextValues({
      ...optionTextValues,
      [option?.label]: {
        ...optionTextValues[option?.label],
        [textField]: newValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
  };

  const handleOptionRemove = (optionToRemove) => () => {
    setMedicalHistory(
      medicalHistory.filter((option) => option?.label !== optionToRemove)
    );
    setOptionTextValues((prevState) => {
      const { [optionToRemove]: _, ...restOptionTextValues } = prevState;
      return restOptionTextValues;
    });
  };

  const exisitingConditionsTextChange = (option, textField, newValue) => {
    setExistingConditionsSpecs({
      ...existingConditionSpecs,
      [option?.label]: {
        ...existingConditionSpecs[option?.label],
        [textField]: newValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
  };

  const handleExistingConditionsSpecDelete = (optionToRemove) => () => {
    setExistingCondition(
      existingConditions.filter((option) => option?.label !== optionToRemove)
    );
    setExistingConditionsSpecs((prevState) => {
      const { [optionToRemove]: _, ...restOptionTextValues } = prevState;
      return restOptionTextValues;
    });
  };

  const handleSymtomsTextChange = (option, textField, newValue) => {
    setSymptomsSpecs({
      ...symptomsSpecs,
      [option?.label]: {
        ...symptomsSpecs[option?.label],
        [textField]: newValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
  };

  const handleSymptomsSpecsDelete = (optionToRemove) => () => {
    setSymptoms(symptoms.filter((option) => option?.label !== optionToRemove));
    setSymptomsSpecs((prevState) => {
      const { [optionToRemove]: _, ...restOptionTextValues } = prevState;
      return restOptionTextValues;
    });
  };

  const handleExaminationTextChange = (option, textField, newValue) => {
    setExaminationSpecs({
      ...examinationSpecs,
      [option?.label]: {
        ...examinationSpecs[option?.label],
        [textField]: newValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
  };

  const handleExaminationSpecsDelete = (optionToRemove) => () => {
    setExamFinding(
      examFindings.filter((option) => option?.label !== optionToRemove)
    );
    setExaminationSpecs((prevState) => {
      const { [optionToRemove]: _, ...restOptionTextValues } = prevState;
      return restOptionTextValues;
    });
  };

  const handleDiagnosisTextChange = (option, textField, newValue) => {
    setDiagnosisSpecs({
      ...diagnosisSpecs,
      [option?.label]: {
        ...diagnosisSpecs[option?.label],
        [textField]: newValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
  };

  const handleDiagnosisSpecsDelete = (optionToRemove) => () => {
    setDiagnosis(
      diagnosis.filter((option) => option?.label !== optionToRemove)
    );
    setDiagnosisSpecs((prevState) => {
      const { [optionToRemove]: _, ...restOptionTextValues } = prevState;
      return restOptionTextValues;
    });
  };
  const handleMedicationsTextChange = (option, textField, newValue) => {
    let inputValue;
    if(textField === "severity"){
      const severityValue = newValue.trim().replace(/[^0-9]/g, "");
      if (severityValue.length < 3) {
        inputValue = severityValue.replace(/(\d{1})(\d{1})/, "$1-$2");
      } else if (severityValue.length < 6) {
        inputValue = severityValue.replace(/(\d{1})(\d{1})(\d{1})/, "$1-$2-$3");
      } else inputValue = ""
    } else inputValue = newValue;
    setMedicationsSpecs({
      ...medicationsSpecs,
      [option?.label]: {
        ...medicationsSpecs[option?.label],
        [textField]: inputValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
  };

  const handleMedicationsSpecsDelete = (optionToRemove) => () => {
    setMedications(
      medications.filter((option) => option?.label !== optionToRemove)
    );
    setMedicationsSpecs((prevState) => {
      const { [optionToRemove]: _, ...restOptionTextValues } = prevState;
      return restOptionTextValues;
    });
  };
  const handleLabTextChange = (option, textField, newValue) => {
    setLabInvestigationSpecs({
      ...labInvestigationSpecs,
      [option?.label]: {
        ...labInvestigationSpecs[option?.label],
        [textField]: newValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
  };

  const handleLabSpecsDelete = (optionToRemove) => () => {
    setLabInvestigation(
      labInvestigation.filter((option) => option?.label !== optionToRemove)
    );
    setLabInvestigationSpecs((prevState) => {
      const { [optionToRemove]: _, ...restOptionTextValues } = prevState;
      return restOptionTextValues;
    });
  };

  const diagnosisObj = (inputObject) => {
    const result = [];

    for (const key in inputObject) {
      const value = inputObject[key];
      if (
        JSON.stringify(value) === JSON.stringify({}) ||
        JSON.stringify(value) === "[object Object]"
      ) {
        continue;
      }

      if (key === "array") {
        continue;
      }
      const objectDetails = inputObject[key];
      const transformedItem = {
        disease: key,
        status: objectDetails.since,
        diagnosis_type: objectDetails.severity,
        notes: objectDetails.notes,
        snowmed_code: objectDetails?.snowmed_code,
        snowmed_display: objectDetails?.snowmed_display,
      };

      result.push(transformedItem);
    }
    const filteredResult = result.filter(
      (item) => item.disease !== "[object Object]"
    );
    return filteredResult;
  };

  const diseaseObject = (inputObject) => {
    const result = [];

    for (const key in inputObject) {
      const value = inputObject[key];
      if (
        JSON.stringify(value) === JSON.stringify({}) ||
        JSON.stringify(value) === "[object Object]"
      ) {
        continue;
      }

      if (key === "array") {
        continue;
      }
      const objectDetails = inputObject[key];
      const transformedItem = {
        disease: key,
        notes: objectDetails.notes,
        snowmed_code: objectDetails?.snowmed_code,
        snowmed_display: objectDetails?.snowmed_display,
      };

      result.push(transformedItem);
    }
    const filteredResult = result.filter(
      (item) => item.disease !== "[object Object]"
    );
    return filteredResult;
  };
  const conditonObject = (inputObject) => {
    const result = [];

    for (const key in inputObject) {
      const value = inputObject[key];
      if (
        JSON.stringify(value) === JSON.stringify({}) ||
        JSON.stringify(value) === "[object Object]"
      ) {
        continue;
      }

      if (key === "array") {
        continue;
      }

      const objectDetails = inputObject[key];
      const transformedItem = {
        condition: key,
        status: objectDetails.severity,
        start_date: "2023/08/08",
        notes: objectDetails.notes,
        snowmed_code: objectDetails?.snowmed_code,
        snowmed_display: objectDetails?.snowmed_display,
      };

      result.push(transformedItem);
    }
    const filteredResult = result.filter(
      (item) => item.condition !== "[object Object]"
    );
    return filteredResult;
  };

  const symptomObj = (inputObject) => {
    const result = [];
    for (const key in inputObject) {
      const value = inputObject[key];
      if (
        JSON.stringify(value) === JSON.stringify({}) ||
        JSON.stringify(value) === "[object Object]"
      ) {
        continue;
      }
      if (key === "array") {
        continue;
      }

      const objectDetails = inputObject[key];

      result.push({
        symptom: key,
        duration: objectDetails.since,
        start_date: "2023/08/08",
        severity: objectDetails.severity,
        notes: objectDetails.notes,
        snowmed_code: objectDetails?.snowmed_code,
        snowmed_display: objectDetails?.snowmed_display,
      });
    }
    const filteredResult = result.filter(
      (item) => item.symptom !== "[object Object]"
    );
    return filteredResult;
  };
  const medicationObj = (inputObject) => {
    const result = [];

    for (const key in inputObject) {
      const value = inputObject[key];
      if (
        JSON.stringify(value) === JSON.stringify({}) ||
        JSON.stringify(value) === "[object Object]"
      ) {
        continue;
      }

      if (key === "array") {
        continue;
      }

      const objectDetails = inputObject[key];

      const transformedItem = {
        medicine_name: key,
        frequency: objectDetails.severity,
        dosage: objectDetails.dose,
        time_of_day: objectDetails.timing,
        duration: objectDetails.since,
        notes: objectDetails.notes,
        snowmed_code: objectDetails?.snowmed_code,
        snowmed_display: objectDetails?.snowmed_display,
      };

      result.push(transformedItem);
    }

    const filteredResult = result.filter(
      (item) => item.medicine_name !== "[object Object]"
    );
    return filteredResult;
  };

  const currentMedicationObj = (inputObject) => {
    const result = [];

    for (const key in inputObject) {
      const value = inputObject[key];
      if (
        JSON.stringify(value) === JSON.stringify({}) ||
        JSON.stringify(value) === "[object Object]"
      ) {
        continue;
      }

      if (key === "array") {
        continue;
      }
      const objectDetails = inputObject[key];

      const transformedItem = {
        medicine_name: key,
        start_date: "2023/08/08",
        status: objectDetails.severity,
        notes: objectDetails.notes,
        snowmed_code: objectDetails?.snowmed_code,
        snowmed_display: objectDetails?.snowmed_display,
      };

      result.push(transformedItem);
    }
    const filteredResult = result.filter(
      (item) => item.medicine_name !== "[object Object]"
    );
    return filteredResult;
  };

  const labInvestigationObj = (inputObject) => {
    const result = [];

    for (const key in inputObject) {
      const value = inputObject[key];
      if (
        JSON.stringify(value) === JSON.stringify({}) ||
        JSON.stringify(value) === "[object Object]"
      ) {
        continue;
      }

      if (key === "array") {
        continue;
      }

      const objectDetails = inputObject[key];

      const transformedItem = {
        name: key,
        snowmed_code: objectDetails?.snowmed_code,
        snowmed_display: objectDetails?.snowmed_display,
      };

      result.push(transformedItem);
    }
    const filteredResult = result.filter(
      (item) => item.name !== "[object Object]"
    );
    return filteredResult;
  };

  const medicalHistoryObj = (inputObject) => {
    const result = [];

    for (const key in inputObject) {
      const value = inputObject[key];

      if (
        JSON.stringify(value) === JSON.stringify({}) ||
        JSON.stringify(value) === "[object Object]"
      ) {
        continue;
      }

      if (key === "array") {
        continue;
      }
      const objectDetails = inputObject[key];
      const transformedItem = {
        medical_history: key,
        relationship: objectDetails.relationship,
        since: objectDetails.since,
        notes: objectDetails.notes,
        snowmed_code: objectDetails?.snowmed_code || "",
        snowmed_display: objectDetails?.snowmed_display || "",
      };
      result.push(transformedItem);
    }
    const filteredResult = result.filter(
      (item) => item.medical_history !== "[object Object]"
    );
    return filteredResult;
  };

  const createPayload = (key, valueArr) => {
    const payload = submitEMRPayload;
    if (key !== "vital") {
      const payloadData = {
        data: valueArr,
      };
      payload[key] = payloadData;
    }
    if (key === "vital") {
      payload[key] = valueArr;
    }

    setSubmitEMRPayload(payload);
  };

  const createPdfBlob = async (patientDetails) => {
    const pdfBlob = await pdf(
      <PMRPdf patientData={patientDetails || patientData} />
    ).toBlob();

    const pdfFile = new File([pdfBlob], "patient_record.pdf", {
      type: "application/pdf",
    });

    return pdfFile;
  };
  const handleNotifyModalClose = () => {
    setNotifyModal(false);
  };

  const postPMR = async () => {
    setShowLoader(true);
    const pmr_request = pdfData;
    pmr_request["pmr_id"] = emrId;
    pmr_request["advice"] = advices;
    pmr_request["notes"] = prescriptionComment;

    const pdfPayload = {
      mode: "digital",
      pmr_id: emrId,
    };
    const current_patient = JSON.parse(patient);
    let appointment_request;
    if (followUp) {
      appointment_request = {
        appointment_id: current_patient?.id,
        followup_date: followUp, //convertDateFormat(followUp, "yyyy-MM-dd"),
        consultation_status: "Completed",
      };
    } else {
      appointment_request = {
        appointment_id: current_patient?.id,
        consultation_status: "Completed",
      };
    }
    const allData = {
      pmr_request,
      appointment_request,
    };
    const blob = await createPdfBlob();
    dispatch(submitPdf({ blob, pdfPayload }))
      .then((pdfResponse) => {
        dispatch(postEMR(allData))
          .then((res) => {
            setShowLoader(false);
            if (res.meta.requestStatus === "rejected") {
              setPmrDialogOpen(true);
            } else {
              setDocumentId(pdfResponse?.payload?.data?.document_id);
              if(currentPatient?.patient_details?.abha_number || currentPatient?.abha_number){
                const payload = {
                  // abha_number: currentPatient?.patient_details?.abha_number || currentPatient?.abha_number,
                  patient_id: currentPatient?.patient_details?.patientId || currentPatient?.patientId,
                  purpose: "KYC_AND_LINK",
                  auth_mode: "DEMOGRAPHICS", //event.target.value,
                  // hip_id: currentPatient?.patient_details?.hip_id || currentPatient?.hip_id,
                };
                dispatch(verifyDemographics(payload)).then((patientAuthResponse) => {
                  setGatewayRequestId(patientAuthResponse?.payload?.request_id);
                  setFunctionCalled(true); 
                  setRetryCount((prevCount) => prevCount + 1);
                  // setTxnId(res.payload?.txn_id);
                  // const demographicsPayload = {
                  //   txnId: patientAuthResponse.payload?.txn_id,
                  //   pid: currentPatient?.patient_details?.patientId || currentPatient?.patientId,
                  // };
                  // dispatch(verifyDemographics(demographicsPayload)).then((deographicResponse) => {
                  //   if(deographicResponse?.payload?.request_id){
                  //     const syncPMRPayload = {
                  //       hip_id: currentPatient?.patient_details?.hip_id || currentPatient?.hip_id,
                  //       pmr_id: sessionStorage.getItem("pmrID"),
                  //     };
                  //     dispatch(syncPMR(syncPMRPayload)).then((syncPMRResponse) => {
                  //       // sessionStorage.removeItem("pmrId");
                  //       // navigate("/appointment-list");
                  //       if(syncPMRResponse?.payload?.status === "success"){
                  //         setNotifyModal(true);
                  //       } else {
                  //         setErrorMessage("Sync ABHA failed");
                  //         setShowSnackbar(true);
                  //       }
                  //     });
                  //   }
                  // });
                });
              } else {
                setNotifyModal(true);
              }
            }
          })
          .catch((error) => {
            console.log(error);
          })
        }
      )
      .catch((error) => {
        console.log(error);
      });
    // const currentPatient = JSON.parse(
    //   sessionStorage.getItem("selectedPatient")
    // );
    // if (
    //   userRole === "ADMIN" &&
    //   currentPatient?.patient_details?.abha_number &&
    //   currentPatient?.patient_details?.abha_number !== ""
    // ) {
    //   setShowSync(true);
    // }
  };

  const filterVitals = (vitalsArr) => {
    const filteredvital = [];
    vitalsArr?.map((item) => {
      const filteredEntry = {};
      for (const key in item) {
        if (item[key]?.length > 0) {
          filteredEntry[key] = item[key];
        }
      }
      filteredvital?.push(filteredEntry);
    });
    return filteredvital;
  };
  const [pdfUrl, setPdfUrl] = useState(null);
  const submitEMR = async () => {
    const symptomsEMR = symptomObj(symptomsSpecs);
    const diagnosisEMR = diagnosisObj(diagnosisSpecs);
    const conditionEMR = conditonObject(existingConditionSpecs);
    const examinEMR = diseaseObject(examinationSpecs);
    const medicationEMR = medicationObj(medicationsSpecs);
    const currentMedicationEMR = currentMedicationObj();
    const labInvestigationEMR = labInvestigationObj(labInvestigationSpecs);
    const medicalHistoryEMR = medicalHistoryObj(optionTextValues);

    const payloadArr = [
      {
        key: "vital",
        dataArr: {
          height: formValues?.bodyHeight,
          weight: formValues?.bodyWeight,
          pulse: formValues?.pulseRate,
          blood_pressure: formValues?.bloodPressure,
          body_temperature: formValues?.bodyTemp,
          oxygen_saturation: formValues?.oxygenSaturation,
          respiratory_rate: formValues?.respiratoryRate,
          systolic_blood_pressure: formValues?.systolicBP,
          diastolic_blood_pressure: formValues?.diastolicaBP,
          body_mass_index: bodyMassIndex,
        },
      },
      {
        key: "condition",
        dataArr: conditionEMR,
      },
      {
        key: "examination_findings",
        dataArr: examinEMR,
      },
      {
        key: "symptom",
        dataArr: symptomsEMR,
      },
      {
        key: "diagnosis",
        dataArr: diagnosisEMR,
      },
      {
        key: "medication",
        dataArr: medicationEMR,
      },
      {
        key: "lab_investigation",
        dataArr: labInvestigationEMR,
      },
      {
        key: "medical_history",
        dataArr: medicalHistoryEMR,
      },
    ];

    payloadArr?.forEach((item) => {
      createPayload(item?.key, item?.dataArr);
    });
    const hospital = sessionStorage?.getItem("selectedHospital");
    // const patient = sessionStorage?.getItem("selectedPatient");
    let patientDetails = {};
    if (hospital) {
      const currentHospital = JSON.parse(hospital);
      // const currentPatient = JSON.parse(patient);
      patientDetails = {
        hospitalName: currentHospital?.name || "-",
        patientName:
          currentPatient?.patient_details?.name || currentPatient?.name || "-",
        doctorName: currentPatient?.doc_name || "-",
        patientEmail:
          currentPatient?.patient_details?.email ||
          currentPatient?.email ||
          "-",
        patientGender:
          currentPatient?.patient_details?.gender ||
          currentPatient?.gender ||
          "-",
        patientNumber:
          currentPatient?.mobileNumber || currentPatient?.mobile_number || "-",
        patientId: currentPatient?.patientId || "-",
        patientAgeInYears: currentPatient?.patient_details?.age_in_years || currentPatient?.age_in_years,
        patientAgeInMonths: currentPatient?.patient_details?.age_in_months || currentPatient?.age_in_months
      };
    }
    const pdfFormattedData = submitEMRPayload;
    pdfFormattedData["advice"] = advices;
    pdfFormattedData["notes"] = prescriptionComment;
    if(followUp){
      pdfFormattedData["followup"] = followUp;
    }
    setPdfData(pdfFormattedData);
    setPatientData(patientDetails);

    sessionStorage.setItem("patientDetailsPdf", JSON.stringify(patientDetails));
    sessionStorage.setItem(
      "patientEMRDetails",
      JSON.stringify(pdfFormattedData)
    );

    setPmrFinished(true);
    setStep("preview");
    pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
    let pdf_data = await createPdfBlob(patientDetails);
    const pdfUrls = URL.createObjectURL(pdf_data);
    setPdfUrl(pdfUrls);
  };

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  const resetEMRForm = () => {
    setMedicalHistory([]);
    setExistingCondition([]);
    setSymptoms([]);
    setExamFinding([]);
    setDiagnosis([]);
    setMedications([]);
    setLabInvestigation([]);
    setOptionTextValues({});
    setExistingConditionsSpecs({});
    setExaminationSpecs({});
    setSymptomsSpecs({});
    setDiagnosisSpecs({});
    setMedicationsSpecs({});
    setLabInvestigationSpecs({});
    setPrescriptionComment(" ");
    setAdvices(" ");
  };

  const saveEMR = () => {
    const symptomsEMR = symptomObj(symptomsSpecs);
    const diagnosisEMR = diagnosisObj(diagnosisSpecs);
    const conditionEMR = conditonObject(existingConditionSpecs);
    const examinEMR = diseaseObject(examinationSpecs);
    const medicationEMR = medicationObj(medicationsSpecs);
    const labInvestigationEMR = labInvestigationObj(labInvestigationSpecs);
    const medicalHistoryEMR = medicalHistoryObj(optionTextValues);

    const payloadArr = [
      {
        key: "vital",
        dataArr: {
          height: formValues?.bodyHeight,
          weight: formValues?.bodyWeight,
          pulse: formValues?.pulseRate,
          blood_pressure: formValues?.bloodPressure,
          body_temperature: formValues?.bodyTemp,
          oxygen_saturation: formValues?.oxygenSaturation,
          respiratory_rate: formValues?.respiratoryRate,
          systolic_blood_pressure: formValues?.systolicBP,
          diastolic_blood_pressure: formValues?.diastolicaBP,
          body_mass_index: bodyMassIndex,
        },
      },
      {
        key: "condition",
        dataArr: conditionEMR,
      },
      {
        key: "examination_findings",
        dataArr: examinEMR,
      },
      {
        key: "symptom",
        dataArr: symptomsEMR,
      },
      {
        key: "diagnosis",
        dataArr: diagnosisEMR,
      },
      {
        key: "medication",
        dataArr: medicationEMR,
      },
      {
        key: "lab_investigation",
        dataArr: labInvestigationEMR,
      },
      {
        key: "medical_history",
        dataArr: medicalHistoryEMR,
      },
    ];
    payloadArr?.forEach((item) => {
      createPayload(item?.key, item?.dataArr);
    });
    const pmr_request = submitEMRPayload;
    pmr_request["pmr_id"] = emrId;
    // pmr_request["advice"] = {
    //   advices: advices,
    // };
    pmr_request["advice"] = advices;
    pmr_request["notes"] = prescriptionComment;

    let appointment_request;
    const current_patient = JSON.parse(patient);
    if (followUp) {
      appointment_request = {
        appointment_id: current_patient?.id,
        followup_date: followUp, //convertDateFormat(followUp, "yyyy-MM-dd"),
        consultation_status: "InProgress",
      };
    } else {
      appointment_request = {
        appointment_id: current_patient?.id,
        consultation_status: "InProgress",
      };
    }
    const allData = {
      pmr_request,
      appointment_request,
    };

    dispatch(postEMR(allData)).then((res) => {
      // if (
      //   !(
      //     currentPatient?.patient_details?.abha_number &&
      //     currentPatient?.patient_details?.abha_number !== ""
      //   )
      // ) {
        navigate("/appointment-list");
        sessionStorage.removeItem("pmrID");
      // }
    });
  };

  const editPMR = () => {
    setStep("create");
  };
  const relationshipOptions = [
    "self",
    "father",
    "mother",
    "sister",
    "daughter",
  ];
  const diagnosisStatusOpts = ["Suspected", "Confirmed", "Ruled out"];
  const diagnosisTypeOpts = ["Primary Diagnosis", "Differential Diagnosis"];
  const timeOptions = ["Days", "Weeks", "Months", "Years"];
  const doseOptions = ["Tablet", "ML"];
  const timingOptions = [
    "After Meal",
    "Before Meal",
    "With Meal",
    "Empty Stomach",
    "Before breakfast",
    "After breakfast",
    "Before lunch",
    "After lunch",
    "Before dinner",
    "After dinner",
    "Along with food",
    "At bed time",
    "On waking up",
  ];

  const handleRelationshipChange = (option, newValue) => {
    handleTextFieldChange(option, "relationship", newValue);
  };

  const handleDiganosisOptionChange = (option, newValue, key) => {
    handleDiagnosisTextChange(option, key, newValue);
  };

  useEffect(() => {
    if (formValues?.bodyHeight !== "" && formValues.bodyWeight !== "") {
      const bmi = calculateBMI(formValues?.bodyHeight, formValues.bodyWeight);
      if (typeof bmi === "number") {
        setBodyMassIndex(bmi.toFixed(2));
      } else {
        setBodyMassIndex("");
      }
    }
  }, [formValues?.bodyHeight, formValues.bodyWeight]);

  const handleNumberOptions = (event, value) => {
    const isValidInput = /^([1-9]\d{0,2}(Days|Weeks|Months)?)?$/.test(value);
    if (isValidInput) {
      setNumber(value);
    }
  };

  const handleSymptomNumberOptions = (event, value) => {
    const isValidInput = /^([1-9]\d{0,2}(Days|Weeks|Months)?)?$/.test(value);
    if (isValidInput) {
      setSymptomNumber(value);
    }
  };

  const handleHistoryNumberOptions = (event, value) => {
    const isValidInput = /^([1-9]\d{0,2}(Days|Weeks|Months)?)?$/.test(value);
    if (isValidInput) {
      setMedicalHistoryNumber(value);
    }
  };
  const handleDoseOptions = (event, value) => {
    const isValidInput = /^([1-9]\d{0,2}(Tablet)?)?$/.test(value);
    if (isValidInput) {
      setDose(value);
    }
  };

  const generateOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);
    if (isNaN(parsedNumber) || !item) {
      return [];
    }
    const sinceValue = medicationsSpecs[item]?.since;
    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return timeOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }
    return [];
  };

  const generateSymptomsOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);

    if (isNaN(parsedNumber) || !item) {
      return [];
    }

    const sinceValue = symptomsSpecs[item]?.since;

    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return timeOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }
    return [];
  };

  const generateHistoryOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);
    if (isNaN(parsedNumber) || !item) {
      return [];
    }
    const sinceValue = optionTextValues[item]?.since;
    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return timeOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }
    return [];
  };

  const generateSymptomsOptionChange = (option, newValue, key) => {
    handleSymtomsTextChange(option, key, newValue);
  };

  const generateMedicalHistoryOptionChange = (option, newValue) => {
    handleTextFieldChange(option, "since", newValue);
  };

  const generateDoseOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);

    if (isNaN(parsedNumber) || !item) {
      return [];
    }

    const sinceValue = medicationsSpecs[item]?.dose || "";

    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return doseOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }

    return [];
  };

  const handleMedicationOptionsChange = (option, newValue, key) => {
    handleMedicationsTextChange(option, key, newValue);
  };

  // Notes Popup Settings
  const [openComplaintNotes, setOpenComplaintNotes] = React.useState(false);
  const handleOpenComplaintNotes = () => setOpenComplaintNotes(true);
  const handleCloseComplaintNotes = () => setOpenComplaintNotes(false);

  const [openMedicalHistory, setOpenMedicalHistory] = React.useState(false);
  const handleOpenMedicalHistory = () => setOpenMedicalHistory(true);
  const handleCloseMedicalHistory = () => setOpenMedicalHistory(false);

  const [openFindingNotes, setOpenFindingNotes] = React.useState(false);
  const handleOpenFindingNotes = () => setOpenFindingNotes(true);
  const handleCloseFindingNotes = () => setOpenFindingNotes(false);

  const [openDiagnosisNotes, setOpenDiagnosisNotes] = React.useState(false);
  const handleOpenDiagnosisNotes = () => setOpenDiagnosisNotes(true);
  const handleCloseDiagnosisNotes = () => setOpenDiagnosisNotes(false);

  const [openLabNotes, setOpenLabNotes] = React.useState(false);
  const handleOpenLabNotes = () => setOpenLabNotes(true);
  const handleCloseLabNotes = () => setOpenLabNotes(false);

  const [openMedicationNotes, setOpenMedicationNotes] = React.useState(false);
  const handleOpenMedicationNotes = () => setOpenMedicationNotes(true);
  const handleCloseMedicationNotes = () => setOpenMedicationNotes(false);

  const handleDateChange = (event) => {
    setFollowUp(event.target.value);
  };

  const onSnackbarClose = () => {
    setShowSnackbar(false);
  };

  return (
    <PatientEMRWrapper>
      <CustomSnackbar
        message={errorMessage || "Something went wrong"}
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
      <CustomLoader
        open={showLoader}
      />
      <CustomizedDialogs
        open={pmrDialogOpen}
        handleClose={handlePmrDialogClose}
      />
      {step === "create" && (
        <div>
          <PatientDetailsHeader documents={documents} />
          <EMRFormWrapper>
            <EMRFormInnerWrapper>
              <VitalsContainer>
                <SectionHeader>Vitals</SectionHeader>
                <form>
                  <Grid container spacing={{ xs: 6, md: 8 }}>
                    <Grid item xs={12} sm={6} md={4} lg={3}>
                      <Typography variant="subtitle1">Pulse Rate</Typography>
                      <TextFieldWrapper>
                        <Grid item xs={8}>
                          <TextField
                            fullWidth
                            type="number"
                            variant="outlined"
                            name="pulseRate"
                            value={formValues.pulseRate}
                            onChange={handleInputChange}
                            className="emr-input-field"
                          />
                        </Grid>
                        <Grid item xs={4}>
                          <VitalValue>/min</VitalValue>
                        </Grid>
                      </TextFieldWrapper>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={3}>
                      <Typography variant="subtitle1">
                        Peripheral oxygen saturation
                      </Typography>
                      <TextFieldWrapper>
                        <Grid item xs={8}>
                          <TextField
                            fullWidth
                            type="number"
                            variant="outlined"
                            name="oxygenSaturation"
                            value={formValues.oxygenSaturation}
                            onChange={handleInputChange}
                            className="emr-input-field"
                          />
                        </Grid>
                        <Grid item xs={4}>
                          <VitalValue>%</VitalValue>
                        </Grid>
                      </TextFieldWrapper>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={3}>
                      <Typography variant="subtitle1">Blood Pressure</Typography>
                      <BPTextFieldWrapper>
                        <Grid item xs={8}>
                          <BPWrapper>
                          <SystolicTextField
                              fullWidth
                              type="number"
                              variant="outlined"
                              name="systolicBP"
                              value={formValues.systolicBP}
                              onChange={handleInputChange}
                              className="emr-input-field"
                            />
                            <Divider>/</Divider>
                            <DiastolicTextField
                              fullWidth
                              type="number"
                              variant="outlined"
                              name="diastolicaBP"
                              value={formValues.diastolicaBP}
                              onChange={handleInputChange}
                              className="emr-input-field"
                            />                           
                          </BPWrapper>
                        </Grid>
                        <Grid item xs={4}>
                          <VitalValue>mmHg</VitalValue>
                        </Grid>
                      </BPTextFieldWrapper>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={3}>
                      <Typography variant="subtitle1">
                        Respiratory rate
                      </Typography>
                      <TextFieldWrapper>
                        <Grid item xs={8}>
                          <TextField
                            fullWidth
                            type="number"
                            variant="outlined"
                            name="respiratoryRate"
                            value={formValues.respiratoryRate}
                            onChange={handleInputChange}
                            className="emr-input-field"
                          />
                        </Grid>
                        <Grid item xs={4}>
                          <VitalValue>/min</VitalValue>
                        </Grid>
                      </TextFieldWrapper>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={3}>
                      <Typography variant="subtitle1">
                        Body Temperature
                      </Typography>
                      <TextFieldWrapper>
                        <Grid item xs={8}>
                          <TextField
                            fullWidth
                            type="number"
                            variant="outlined"
                            name="bodyTemp"
                            value={formValues.bodyTemp}
                            onChange={handleInputChange}
                            className="emr-input-field"
                          />
                        </Grid>
                        <Grid item xs={4}>
                          <VitalValue>°C</VitalValue>
                        </Grid>
                      </TextFieldWrapper>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={3}>
                      <Typography variant="subtitle1">Body height</Typography>
                      <TextFieldWrapper>
                        <Grid item xs={8}>
                          <TextField
                            fullWidth
                            type="number"
                            variant="outlined"
                            name="bodyHeight"
                            value={formValues.bodyHeight}
                            onChange={handleInputChange}
                            className="emr-input-field"
                          />
                        </Grid>
                        <Grid item xs={4}>
                          <VitalValue>Cms</VitalValue>
                        </Grid>
                      </TextFieldWrapper>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={3}>
                      <Typography variant="subtitle1">Body weight</Typography>
                      <TextFieldWrapper>
                        <Grid item xs={8}>
                          <TextField
                            fullWidth
                            type="number"
                            variant="outlined"
                            name="bodyWeight"
                            value={formValues.bodyWeight}
                            onChange={handleInputChange}
                            className="emr-input-field"
                          />
                        </Grid>
                        <Grid item xs={4}>
                          <VitalValue>Kgs</VitalValue>
                        </Grid>
                      </TextFieldWrapper>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={3}>
                      <Typography variant="subtitle1">Body mass index</Typography>
                      <TextFieldWrapper>
                        <Grid item xs={8}>
                          <BPWrapper>
                            <RowWrapper>{bodyMassIndex}</RowWrapper>
                          </BPWrapper>
                        </Grid>
                        <Grid item xs={4}>
                          <VitalValue>Kg/m2</VitalValue>
                        </Grid>
                      </TextFieldWrapper>
                    </Grid>
                  </Grid>
                </form>
              </VitalsContainer>
              {(userRole === "DOCTOR" || userRole === "ADMIN") && (
                <>
                  <VitalsContainer>
                    <SectionHeader>Complaints</SectionHeader>
                    <CustomAutoComplete
                      options={symptomsOpts}
                      handleInputChange={handleSymptompsChange}
                      setOptions={setSymptomsOpts}
                      handleOptionChange={handleSymptoms}
                      handleClearOptions={clearSymptomsOptions}
                    />
                    {symptoms?.length > 0 && (
                      <div>
                        {symptoms
                          ?.slice(0)
                          .reverse()
                          .map((item) => (
                            <FieldSpecsContainer>
                              <RecordLayout>
                                <SelectedRecord>
                                  {item?.label || item}
                                </SelectedRecord>
                              </RecordLayout>
                              <TextBoxLayout className="addMinWidth">
                                <Autocomplete
                                  className="sinceAutocomplete"
                                  options={generateSymptomsOptions(
                                    symptomNumber,
                                    item
                                  )}
                                  value={symptomsSpecs[item?.label]?.since || ""}
                                  onChange={(e, newValue) =>
                                    generateSymptomsOptionChange(
                                      item,
                                      newValue,
                                      "since"
                                    )
                                  }
                                  // inputValue={symptomNumber}
                                  onInputChange={(e, newValue) =>
                                    handleSymptomNumberOptions(item, newValue)
                                  }
                                  renderInput={(params) => (
                                      <TextField
                                        {...params}
                                        type="tel"
                                        label="Since"
                                        variant="outlined"
                                      />
                                  )}
                                />
                              </TextBoxLayout>
                              <NotesWrapper>
                                <TextBoxLayout className="desktop">
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={
                                      symptomsSpecs[item?.label]?.notes || ""
                                    }
                                    onChange={(e) =>
                                      handleSymtomsTextChange(
                                        item,
                                        "notes",
                                        e.target.value
                                      )
                                    }
                                    label="Notes"
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </NotesWrapper>
                              <DeleteWrapper>
                                <p
                                  onClick={handleOpenComplaintNotes}
                                  className="mobile"
                                >
                                  <NotesField />
                                </p>
                                <Modal
                                  open={openComplaintNotes}
                                  onClose={handleCloseComplaintNotes}
                                  aria-labelledby="modal-modal-title"
                                  aria-describedby="modal-modal-description"
                                >
                                  <Box sx={style}>
                                    <div style={{ position: "relative" }}>
                                      <Toolbar>
                                        <Typography
                                          id="modal-modal-title"
                                          sx={{ flex: 1 }}
                                          variant="h3"
                                        >
                                          Complaints Note
                                        </Typography>
                                        <IconButton
                                          edge="end"
                                          color="inherit"
                                          onClick={handleCloseComplaintNotes}
                                          aria-label="close"
                                        >
                                          <CloseIcon />
                                        </IconButton>
                                      </Toolbar>
                                    </div>
                                    <Typography sx={{ mt: 2 }}>
                                      <TextBoxLayout>
                                        <TextareaAutosize
                                          maxRows={3}
                                          className="textareaAutoSizeStyle"
                                          placeholder="Notes"
                                          value={
                                            symptomsSpecs[item?.label]?.notes ||
                                            ""
                                          }
                                          onChange={(e) =>
                                            handleSymtomsTextChange(
                                              item,
                                              "notes",
                                              e.target.value
                                            )
                                          }
                                          variant="outlined"
                                        />
                                      </TextBoxLayout>
                                    </Typography>
                                    <PrimaryButton
                                      onClick={handleCloseComplaintNotes}
                                      sx={{ marginTop: "10px", float: "right" }}
                                    >
                                      Submit
                                    </PrimaryButton>
                                  </Box>
                                </Modal>

                                <DeleteField
                                  onClick={handleSymptomsSpecsDelete(item?.label)}
                                >
                                  Delete
                                </DeleteField>
                              </DeleteWrapper>
                            </FieldSpecsContainer>
                          ))}
                      </div>
                    )}
                  </VitalsContainer>
                  <VitalsContainer>
                    <SectionHeader>Patient Medical History</SectionHeader>
                    <CustomAutoComplete
                      options={medicalHistoryOpts}
                      handleInputChange={handleMeidcalHistoryChange}
                      setOptions={setMedicalHistoryOpts}
                      handleOptionChange={handleMedicalHistoryValue}
                      handleClearOptions={clearMedicalHistoryOptions}
                      autocompleteRef={medicalHistoryRef}
                    />
                    {medicalHistory?.length > 0 && (
                      <div>
                        {medicalHistory
                          ?.slice(0)
                          .reverse()
                          .map((item) => (
                            <FieldSpecsContainer>
                              <RecordLayout className="addMinWidth">
                                <SelectedRecord>
                                  {item?.label || item}
                                </SelectedRecord>
                              </RecordLayout>
                              <TextBoxLayout className="addMinWidth">
                                <Autocomplete
                                  options={generateHistoryOptions(
                                    medicalHistoryNumber,
                                    item
                                  )}
                                  value={
                                    optionTextValues[item?.label]?.since || ""
                                  }
                                  onChange={(e, newValue) =>
                                    generateMedicalHistoryOptionChange(
                                      item,
                                      newValue
                                    )
                                  }
                                  // inputValue={symptomNumber}
                                  onInputChange={(e, newValue) =>
                                    handleHistoryNumberOptions(item, newValue)
                                  }
                                  renderInput={(params) => (
                                    <TextField
                                      type="tel"
                                      {...params}
                                      label="Since"
                                      variant="outlined"
                                    />
                                  )}
                                />
                              </TextBoxLayout>
                              <TextBoxLayout className="addMinWidth">
                                <Autocomplete
                                  options={relationshipOptions}
                                  value={
                                    optionTextValues[item?.label]?.relationship ||
                                    ""
                                  }
                                  onChange={(e, newValue) =>
                                    handleRelationshipChange(item, newValue)
                                  }
                                  renderInput={(params) => (
                                    <TextField
                                      {...params}
                                      label="Relationship"
                                      variant="outlined"
                                    />
                                  )}
                                />
                              </TextBoxLayout>
                              <NotesWrapper>
                                <TextBoxLayout className="desktop">
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={
                                      optionTextValues[item?.label]?.notes || ""
                                    }
                                    onChange={(e) =>
                                      handleTextFieldChange(
                                        item,
                                        "notes",
                                        e.target.value
                                      )
                                    }
                                    label="Notes"
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </NotesWrapper>
                              <DeleteWrapper>
                                <p
                                  onClick={handleOpenMedicalHistory}
                                  className="mobile"
                                >
                                  <NotesField />
                                </p>
                                <Modal
                                  open={openMedicalHistory}
                                  onClose={handleCloseMedicalHistory}
                                  aria-labelledby="modal-modal-title"
                                  aria-describedby="modal-modal-description"
                                >
                                  <Box sx={style}>
                                    <div style={{ position: "relative" }}>
                                      <Toolbar>
                                        <Typography
                                          id="modal-modal-title"
                                          sx={{ flex: 1 }}
                                          variant="h3"
                                        >
                                          Patient Medical History Notes
                                        </Typography>
                                        <IconButton
                                          edge="end"
                                          color="inherit"
                                          onClick={handleCloseMedicalHistory}
                                          aria-label="close"
                                        >
                                          <CloseIcon />
                                        </IconButton>
                                      </Toolbar>
                                    </div>
                                    <Typography
                                      id="modal-modal-description"
                                      sx={{ mt: 2 }}
                                    >
                                      <TextBoxLayout>
                                        <TextareaAutosize
                                          maxRows={3}
                                          className="textareaAutoSizeStyle"
                                          placeholder="Notes"
                                          value={
                                            optionTextValues[item?.label]
                                              ?.notes || ""
                                          }
                                          onChange={(e) =>
                                            handleTextFieldChange(
                                              item,
                                              "notes",
                                              e.target.value
                                            )
                                          }
                                          variant="outlined"
                                        />
                                      </TextBoxLayout>
                                    </Typography>
                                    <PrimaryButton
                                      onClick={handleCloseMedicalHistory}
                                      sx={{ marginTop: "10px", float: "right" }}
                                    >
                                      Submit
                                    </PrimaryButton>
                                  </Box>
                                </Modal>
                                <DeleteField
                                  onClick={handleOptionRemove(item?.label)}
                                >
                                  Delete
                                </DeleteField>
                              </DeleteWrapper>
                            </FieldSpecsContainer>
                          ))}
                      </div>
                    )}
                  </VitalsContainer>
                  <VitalsContainer>
                    <SectionHeader>Examination Findings</SectionHeader>
                    <CustomAutoComplete
                      options={examFindingsOpts}
                      handleInputChange={handleExamFindingsChange}
                      setOptions={setExamFindingsOpts}
                      handleOptionChange={handleExaminationFindings}
                      handleClearOptions={clearExaminationFindingOptions}
                    />
                    {examFindings?.length > 0 && (
                      <div>
                        {examFindings
                          ?.slice(0)
                          .reverse()
                          .map((item) => (
                            <FieldSpecsContainer>
                              <RecordLayout>
                                <SelectedRecord>
                                  {item?.label || item}
                                </SelectedRecord>
                              </RecordLayout>
                              <NotesWrapper>
                                <TextBoxLayout className="desktop">
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={
                                      examinationSpecs[item?.label]?.notes || ""
                                    }
                                    onChange={(e) =>
                                      handleExaminationTextChange(
                                        item,
                                        "notes",
                                        e.target.value
                                      )
                                    }
                                    label="Notes"
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </NotesWrapper>
                              <DeleteWrapper>
                                <p
                                  onClick={handleOpenFindingNotes}
                                  className="mobile"
                                >
                                  <NotesField />
                                </p>
                                <Modal
                                  open={openFindingNotes}
                                  onClose={handleCloseFindingNotes}
                                  aria-labelledby="modal-modal-title"
                                  aria-describedby="modal-modal-description"
                                >
                                  <Box sx={style}>
                                    <div style={{ position: "relative" }}>
                                      <Toolbar>
                                        <Typography
                                          id="modal-modal-title"
                                          sx={{ flex: 1 }}
                                          variant="h3"
                                        >
                                          Examination Finding Notes
                                        </Typography>
                                        <IconButton
                                          edge="end"
                                          color="inherit"
                                          onClick={handleCloseFindingNotes}
                                          aria-label="close"
                                        >
                                          <CloseIcon />
                                        </IconButton>
                                      </Toolbar>
                                    </div>
                                    <Typography
                                      id="modal-modal-description"
                                      sx={{ mt: 2 }}
                                    >
                                      <TextBoxLayout>
                                        <TextareaAutosize
                                          maxRows={3}
                                          className="textareaAutoSizeStyle"
                                          placeholder="Notes"
                                          value={
                                            examinationSpecs[item?.label]
                                              ?.notes || ""
                                          }
                                          onChange={(e) =>
                                            handleExaminationTextChange(
                                              item,
                                              "notes",
                                              e.target.value
                                            )
                                          }
                                          variant="outlined"
                                        />
                                      </TextBoxLayout>
                                    </Typography>
                                    <PrimaryButton
                                      onClick={handleCloseFindingNotes}
                                      sx={{ marginTop: "10px", float: "right" }}
                                    >
                                      Submit
                                    </PrimaryButton>
                                  </Box>
                                </Modal>
                                <DeleteField
                                  onClick={handleExaminationSpecsDelete(
                                    item?.label
                                  )}
                                >
                                  Delete
                                </DeleteField>
                              </DeleteWrapper>
                            </FieldSpecsContainer>
                          ))}
                      </div>
                    )}
                  </VitalsContainer>
                  <VitalsContainer>
                    <SectionHeader>Diagnosis</SectionHeader>
                    <CustomAutoComplete
                      options={diagnosisOpts}
                      handleInputChange={handleDiagnosisChange}
                      setOptions={setDiagnosisOpts}
                      handleOptionChange={handleDiagnosis}
                      handleClearOptions={clearDiagnosisOptions}
                    />
                    {diagnosis?.length > 0 && (
                      <div>
                        {diagnosis
                          ?.slice(0)
                          .reverse()
                          .map((item) => (
                            <FieldSpecsContainer>
                              <RecordLayout className="addMinWidth">
                                <SelectedRecord>
                                  {item?.label || item}
                                </SelectedRecord>
                              </RecordLayout>
                              <TextBoxLayout className="addMinWidth">
                                <Autocomplete
                                  options={diagnosisStatusOpts}
                                  value={diagnosisSpecs[item?.label]?.since || ""}
                                  onChange={(e, newValue) =>
                                    handleDiganosisOptionChange(
                                      item,
                                      newValue,
                                      "since"
                                    )
                                  }
                                  renderInput={(params) => (
                                    <TextField
                                      {...params}
                                      label="Status"
                                      variant="outlined"
                                    />
                                  )}
                                />
                              </TextBoxLayout>
                              <TextBoxLayout className="addMinWidth">
                                <Autocomplete
                                  options={diagnosisTypeOpts}
                                  value={
                                    diagnosisSpecs[item?.label]?.severity || ""
                                  }
                                  onChange={(e, newValue) =>
                                    handleDiganosisOptionChange(
                                      item,
                                      newValue,
                                      "severity"
                                    )
                                  }
                                  renderInput={(params) => (
                                    <TextField
                                      {...params}
                                      label="Type"
                                      variant="outlined"
                                    />
                                  )}
                                />
                              </TextBoxLayout>
                              <NotesWrapper>
                                <TextBoxLayout className="desktop">
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={
                                      diagnosisSpecs[item?.label]?.notes || ""
                                    }
                                    onChange={(e) =>
                                      handleDiagnosisTextChange(
                                        item,
                                        "notes",
                                        e.target.value
                                      )
                                    }
                                    label="Notes"
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </NotesWrapper>
                              <DeleteWrapper>
                                <p
                                  onClick={handleOpenDiagnosisNotes}
                                  className="mobile"
                                >
                                  <NotesField />
                                </p>
                                <Modal
                                  open={openDiagnosisNotes}
                                  onClose={handleCloseDiagnosisNotes}
                                  aria-labelledby="modal-modal-title"
                                  aria-describedby="modal-modal-description"
                                >
                                  <Box sx={style}>
                                    <div style={{ position: "relative" }}>
                                      <Toolbar>
                                        <Typography
                                          id="modal-modal-title"
                                          sx={{ flex: 1 }}
                                          variant="h3"
                                        >
                                          Diagnosis Notes
                                        </Typography>
                                        <IconButton
                                          edge="end"
                                          color="inherit"
                                          onClick={handleCloseDiagnosisNotes}
                                          aria-label="close"
                                        >
                                          <CloseIcon />
                                        </IconButton>
                                      </Toolbar>
                                    </div>
                                    <Typography
                                      id="modal-modal-description"
                                      sx={{ mt: 2 }}
                                    >
                                      <TextBoxLayout>
                                        <TextareaAutosize
                                          maxRows={3}
                                          className="textareaAutoSizeStyle"
                                          placeholder="Notes"
                                          value={
                                            diagnosisSpecs[item?.label]?.notes ||
                                            ""
                                          }
                                          onChange={(e) =>
                                            handleDiagnosisTextChange(
                                              item,
                                              "notes",
                                              e.target.value
                                            )
                                          }
                                          variant="outlined"
                                        />
                                      </TextBoxLayout>
                                    </Typography>
                                    <PrimaryButton
                                      onClick={handleCloseDiagnosisNotes}
                                      sx={{ marginTop: "10px", float: "right" }}
                                    >
                                      Submit
                                    </PrimaryButton>
                                  </Box>
                                </Modal>
                                <DeleteField
                                  onClick={handleDiagnosisSpecsDelete(
                                    item?.label
                                  )}
                                >
                                  Delete
                                </DeleteField>
                              </DeleteWrapper>
                            </FieldSpecsContainer>
                          ))}
                      </div>
                    )}
                  </VitalsContainer>
                  <VitalsContainer>
                    <SectionHeader>Lab Investigations</SectionHeader>
                    <CustomAutoComplete
                      options={labInvestigationsOpts}
                      handleInputChange={handleLabInvestigationsChange}
                      setOptions={setLabInvestigationsOpts}
                      handleOptionChange={handleLabInvestigations}
                      handleClearOptions={clearLabInvestigationOptions}
                    />
                    {labInvestigation?.length > 0 && (
                      <div>
                        {labInvestigation
                          ?.slice(0)
                          .reverse()
                          .map((item) => (
                            <FieldSpecsContainer>
                              <RecordLayout>
                                <SelectedRecord>
                                  {item?.label || item}
                                </SelectedRecord>
                              </RecordLayout>
                              <NotesWrapper>
                                <TextBoxLayout className="desktop">
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={
                                      labInvestigationSpecs[item?.label]?.notes ||
                                      ""
                                    }
                                    onChange={(e) =>
                                      handleLabTextChange(
                                        item,
                                        "notes",
                                        e.target.value
                                      )
                                    }
                                    label="Notes"
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </NotesWrapper>
                              <DeleteWrapper>
                                <p
                                  onClick={handleOpenLabNotes}
                                  className="mobile"
                                >
                                  <NotesField />
                                </p>
                                <Modal
                                  open={openLabNotes}
                                  onClose={handleCloseLabNotes}
                                  aria-labelledby="modal-modal-title"
                                  aria-describedby="modal-modal-description"
                                >
                                  <Box sx={style}>
                                    <div style={{ position: "relative" }}>
                                      <Toolbar>
                                        <Typography
                                          id="modal-modal-title"
                                          sx={{ flex: 1 }}
                                          variant="h3"
                                        >
                                          Lab Investigation Notes
                                        </Typography>
                                        <IconButton
                                          edge="end"
                                          color="inherit"
                                          onClick={handleCloseLabNotes}
                                          aria-label="close"
                                        >
                                          <CloseIcon />
                                        </IconButton>
                                      </Toolbar>
                                    </div>
                                    <Typography
                                      id="modal-modal-description"
                                      sx={{ mt: 2 }}
                                    >
                                      <TextBoxLayout>
                                        <TextareaAutosize
                                          maxRows={3}
                                          className="textareaAutoSizeStyle"
                                          placeholder="Notes"
                                          value={
                                            labInvestigationSpecs[item?.label]
                                              ?.notes || ""
                                          }
                                          onChange={(e) =>
                                            handleLabTextChange(
                                              item,
                                              "notes",
                                              e.target.value
                                            )
                                          }
                                          variant="outlined"
                                        />
                                      </TextBoxLayout>
                                    </Typography>
                                    <PrimaryButton
                                      onClick={handleCloseLabNotes}
                                      sx={{ marginTop: "10px", float: "right" }}
                                    >
                                      Submit
                                    </PrimaryButton>
                                  </Box>
                                </Modal>
                                <DeleteField
                                  onClick={handleLabSpecsDelete(item?.label)}
                                >
                                  Delete
                                </DeleteField>
                              </DeleteWrapper>
                            </FieldSpecsContainer>
                          ))}
                      </div>
                    )}
                  </VitalsContainer>
                  <VitalsContainer>
                    <SectionHeader>Medications</SectionHeader>
                    <CustomAutoComplete
                      options={medicationsOpts}
                      handleInputChange={handleMedicationsChange}
                      setOptions={setMedicationsOpts}
                      handleOptionChange={handleMedications}
                      handleClearOptions={clearMedicationOptions}
                    />
                    {medications?.length > 0 && (
                      <div>
                        {medications
                          ?.slice(0)
                          .reverse()
                          .map((item) => (
                            <FieldSpecsContainer>
                              <RecordLayout>
                                <SelectedRecord>
                                  {item?.label || item}
                                </SelectedRecord>
                              </RecordLayout>
                              <TextBoxLayout className="desktopTextBoxLayout" style={{ minWidth: "90px" }}>
                                <RecordTextField
                                  placeholder="Frequency"
                                  value={
                                    medicationsSpecs[item?.label]?.severity || ""
                                  }
                                  onChange={(e) =>
                                    handleMedicationsTextChange(
                                      item,
                                      "severity",
                                      e.target.value
                                    )
                                  }                                  
                                  type="tel"
                                  inputProps={{ maxLength: 5}}
                                  label="Frequency"
                                  variant="outlined"
                                />
                              </TextBoxLayout>
                              <TextBoxLayout className="desktopTextBoxLayout">
                                <Autocomplete
                                  options={timingOptions} // Replace with your actual timing options
                                  value={
                                    medicationsSpecs[item?.label]?.timing 
                                  }
                                  onChange={(event, newValue) =>
                                    handleMedicationsTextChange(
                                      item,
                                      "timing",
                                      newValue
                                    )
                                  }
                                  renderInput={(params) => (
                                    <TextField
                                      {...params}
                                      label="Timing"
                                      variant="outlined"
                                    />
                                  )}
                                />
                              </TextBoxLayout>
                              <TextBoxLayout className="addMinWidth">
                                <Autocomplete
                                  options={generateDoseOptions(dose, item)}
                                  value={
                                    medicationsSpecs[item?.label]?.dose || ""
                                  }
                                  onChange={(e, newValue) =>
                                    handleMedicationOptionsChange(
                                      item,
                                      newValue,
                                      "dose"
                                    )
                                  }
                                  // inputValue={dose}
                                  onInputChange={(e, newVal) =>
                                    handleDoseOptions(e, newVal)
                                  }
                                  renderInput={(params) => (
                                    <TextField
                                      {...params}
                                      type="tel"
                                      label="Dose"
                                      variant="outlined"
                                    />
                                  )}
                                />
                              </TextBoxLayout>
                              <TextBoxLayout className="addMinWidth">
                                <Autocomplete
                                  options={generateOptions(number, item)}
                                  value={
                                    medicationsSpecs[item?.label]?.since || ""
                                  }
                                  onChange={(e, newValue) =>
                                    handleMedicationOptionsChange(
                                      item,
                                      newValue,
                                      "since"
                                    )
                                  }
                                  // inputValue={number}
                                  onInputChange={(e, newValue) =>
                                    handleNumberOptions(item, newValue)
                                  }
                                  renderInput={(params) => (
                                    <TextField
                                      {...params}
                                      type="tel"
                                      label="Duration"
                                      variant="outlined"
                                    />
                                  )}
                                />
                              </TextBoxLayout>
                              <TextBoxLayout className="mobileTextBoxLayout frequencyInput">
                                <RecordTextField
                                  placeholder="Frequency"
                                  type="tel"
                                  value={
                                    medicationsSpecs[item?.label]?.severity || ""
                                  }
                                  onChange={(e) =>
                                    handleMedicationsTextChange(
                                      item,
                                      "severity",
                                      e.target.value
                                    )
                                  }
                                  inputProps={{ maxLength: 5}}
                                  label="Frequency"
                                  variant="outlined"
                                />
                              </TextBoxLayout>
                              <TextBoxLayout className="mobileTextBoxLayout addMinWidth">
                                <Autocomplete
                                  options={timingOptions} // Replace with your actual timing options
                                  value={
                                    medicationsSpecs[item?.label]?.timing || null
                                  }
                                  onChange={(event, newValue) =>
                                    handleMedicationsTextChange(
                                      item,
                                      "timing",
                                      newValue
                                    )
                                  }
                                  renderInput={(params) => (
                                    <TextField
                                      {...params}
                                      label="Timing"
                                      variant="outlined"
                                    />
                                  )}
                                />
                              </TextBoxLayout>
                              <NotesWrapper>
                                <TextBoxLayout className="desktop">
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={
                                      medicationsSpecs[item?.label]?.notes || ""
                                    }
                                    onChange={(e) =>
                                      handleMedicationsTextChange(
                                        item,
                                        "notes",
                                        e.target.value
                                      )
                                    }
                                    label="Notes"
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </NotesWrapper>
                              <DeleteWrapper>
                              <p
                                  onClick={handleOpenMedicationNotes}
                                  className="mobile"
                                >
                                  <NotesField />
                                </p>
                                <Modal
                                  open={openMedicationNotes}
                                  onClose={handleCloseMedicationNotes}
                                  aria-labelledby="modal-modal-title"
                                  aria-describedby="modal-modal-description"
                                >
                                  <Box sx={style}>
                                    <div style={{ position: "relative" }}>
                                      <Toolbar>
                                        <Typography
                                          id="modal-modal-title"
                                          sx={{ flex: 1 }}
                                          variant="h3"
                                        >
                                          Medication Notes
                                        </Typography>
                                        <IconButton
                                          edge="end"
                                          color="inherit"
                                          onClick={handleCloseMedicationNotes}
                                          aria-label="close"
                                        >
                                          <CloseIcon />
                                        </IconButton>
                                      </Toolbar>
                                    </div>
                                    <Typography
                                      id="modal-modal-description"
                                      sx={{ mt: 2 }}
                                    >
                                      <TextBoxLayout>
                                        <TextareaAutosize
                                          maxRows={3}
                                          className="textareaAutoSizeStyle"
                                          placeholder="Notes"
                                          value={
                                            medicationsSpecs[item?.label]?.notes || ""
                                          }
                                          onChange={(e) =>
                                            handleMedicationsTextChange(
                                              item,
                                              "notes",
                                              e.target.value
                                            )
                                          }
                                          variant="outlined"
                                        />
                                      </TextBoxLayout>
                                    </Typography>
                                    <PrimaryButton
                                      onClick={handleCloseMedicationNotes}
                                      sx={{ marginTop: "10px", float: "right" }}
                                    >
                                      Submit
                                    </PrimaryButton>
                                  </Box>
                                </Modal>
                                <DeleteField
                                  onClick={handleMedicationsSpecsDelete(
                                    item?.label
                                  )}
                                >
                                  Delete
                                </DeleteField>
                              </DeleteWrapper>
                            </FieldSpecsContainer>
                          ))}
                      </div>
                    )}
                  </VitalsContainer>

                  <VitalsContainer>
                    <SectionHeader>Follow Up</SectionHeader>
                    <TextField
                      sx={{ width: "100%" }}
                      placeholder="Select Date"
                      type="date"
                      inputProps={{
                        min: format(new Date(), "yyyy-MM-dd"), // Set max date to the current date
                      }}
                      value={followUp}
                      onChange={handleDateChange}
                      />
                    {/* <LocalizationProvider dateAdapter={AdapterDayjs}>
                      <DemoContainer components={["DatePicker"]}>
                        <MobileDatePicker
                          sx={{ width: "100%" }}
                          disablePast
                          value={followUp}
                          onChange={(newValue) => setFollowUp(newValue)}
                        />
                      </DemoContainer>
                    </LocalizationProvider> */}
                  </VitalsContainer>

                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <VitalsContainer>
                        <SectionHeader>Notes</SectionHeader>
                        <div>
                          <TextareaAutosize
                            className="textareaAutoSizeStyle"
                            minRows={7}
                            maxRows={7}
                            placeholder="Add your notes here"
                            onChange={prescriptionCommentChange}
                            value={prescriptionComment}
                          />
                        </div>
                      </VitalsContainer>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <VitalsContainer>
                        <SectionHeader>Advices</SectionHeader>
                        <div>
                          <TextareaAutosize
                            className="textareaAutoSizeStyle"
                            minRows={7}
                            maxRows={7}
                            placeholder="Add your advices here"
                            onChange={adviceChange}
                            value={advices}
                          />
                        </div>
                      </VitalsContainer>
                    </Grid>
                  </Grid>
                </>
              )}
            </EMRFormInnerWrapper>
            <EMRFooter style={{ position: "sticky", bottom: 0 }}>
              <SecondaryButton
                onClick={resetEMRForm}
                style={{ padding: "5px 16px" }}
              >
                Clear
              </SecondaryButton>
              <PrimaryButton onClick={saveEMR}>Save</PrimaryButton>
              <PrimaryButton onClick={submitEMR}>
                Review Prescription
              </PrimaryButton>
            </EMRFooter>
          </EMRFormWrapper>
        </div>
      )}
      {pmrFinished && step === "preview" && (
        <PdfDisplayWrapper>
          {/* <PageTitle>Preview</PageTitle>
          <PageSubText>
            Closely Review the Details Before Confirming
          </PageSubText> */}
          <SendPMR
            notifyModal={notifyModal}
            handleNotifyModalClose={handleNotifyModalClose}
            documentId={documentId}
          />          
          {!isMobile && (
            <div style={{ position: "absolute", width: "-webkit-fill-available"}}>
              <PDFViewerWrapper>
                <PDFViewer style={{ width: "100%", height: "100%" }} zoom={1}>
                  <PMRPdf patientData={patientData} />
                </PDFViewer>
              </PDFViewerWrapper>
              <PDFButtonWrapper>
                <SecondaryButton onClick={editPMR} style={{ padding: "8px 16px" }}>Edit</SecondaryButton>
                <PrimaryButton onClick={postPMR}>
                  Finish Prescription
                </PrimaryButton>
              </PDFButtonWrapper>
            </div>
          )}
          {isMobile && (
            <>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "16px",
                  marginBottom: "10px",
                }}
              >
                <SecondaryButton onClick={editPMR}>Edit</SecondaryButton>
                <PrimaryButton onClick={postPMR}>
                  Finish Prescription
                </PrimaryButton>
              </div>
              <PDFViewerWrapper>
                <Document
                  file={pdfUrl}
                  onLoadSuccess={onDocumentLoadSuccess}
                >
                   {Array.apply(null, Array(numPages))
                  .map((x, i)=>i+1)
                  .map(page =>
                    <Page
                      pageNumber={page}
                      renderTextLayer={true}
                      width={width - 15}
                    />
                  )}
                </Document>
              </PDFViewerWrapper>
            </>
          )}
        </PdfDisplayWrapper>
      )}
    </PatientEMRWrapper>
  );
};

export default PatientEMRDetails;
