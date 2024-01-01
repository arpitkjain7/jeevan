import React, { useEffect, useRef } from "react";
import AutoSearch from "../../../components/AutoSearch";
import PatientDetailsHeader from "../../../components/PatientDetailsHeader";
import {
  Typography,
  styled,
  TextField,
  Grid,
  filledInputClasses,
  Autocomplete,
  Modal,
  Box
} from "@mui/material";
import { Delete, Assignment } from "@mui/icons-material";
import { Unstable_Popup as BasePopup } from '@mui/base/Unstable_Popup';
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  getEMRId,
  getPatientAuth,
  postEMR,
  searchVitalsDetails,
} from "./EMRPage.slice";
import CustomAutoComplete from "../../../components/CustomAutoComplete";
import { Button } from "@mui/base";
import { PDFViewer, pdf } from "@react-pdf/renderer";
import PMRPdf from "../../../components/PMRPdf";
import { submitPdf } from "../../../components/PMRPdf/pmrPdf.slice";
import { useNavigate } from "react-router-dom";
import SyncAabha from "../SyncAabha";
import { calculateBMI, convertDateFormat } from "../../../utils/utils";
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const PatientEMRWrapper = styled("div")(({ theme }) => ({
  padding: "40px 10px 10px",
  [theme.breakpoints.down('sm')]: {
    padding: "10px 4px 0",
  }
}));

const EMRFormWrapper = styled("div")(({ theme }) => ({}));

const VitalsContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    marginTop: theme.spacing(4),
    padding: theme.spacing(6),
    borderRadius: theme.spacing(1),
    [theme.breakpoints.down('sm')]: {
      padding: theme.spacing(4, 2),
    }
  },
  "& .notes-field": {
    "&.MuiFormControl-root": {
      width: "100%",
      "& > .MuiInputBase-root ": {
        minHeight: theme.spacing(43),
      },
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
    [theme.breakpoints.down('sm')]: {
      gap: theme.spacing(2),
      alignItems: "center",
      border: "1px solid #ccccccb8",
      flexWrap: "wrap",
      padding: "2px"
    }
  },
}));

const EMRFooter = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginTop: theme.spacing(6),
    border: `1px solid ${theme.palette.primaryBlue}`,
    backgroundColor: theme.palette.primaryOpacityBlue,
    padding: theme.spacing(4.5, 8),
  },
}));

const PDFViewerWrapper = styled("div")(({ theme }) => ({
  height: "800px",
  marginBottom: "32px",
  flex: "1",
  [theme.breakpoints.down('sm')]: {
    height: "500px",
    marginBottom: "0"
  }
}))

const PrimaryButton = styled("button")(({ theme }) => ({
  "&": theme.typography.primaryButton,
}));

const SecondaryButton = styled("button")(({ theme }) => ({
  "&": theme.typography.secondaryButton,
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
  [theme.breakpoints.down('sm')]: {
    height: "max-content",
    padding: "10px 8px",
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
  },
  "&.addMaxWidth": {
    [theme.breakpoints.down('sm')]: {
      maxWidth: "110px",
    }
  },
}));

const TextBoxLayout = styled("div")(({ theme }) => ({
  flex: 1,
  "&.desktopTextBoxLayout": {
    [theme.breakpoints.down('sm')]: {
      display: "none",
    }
  },
  "&.mobileTextBoxLayout": {
    [theme.breakpoints.up('sm')]: {
      display: "none",
    }
  },
  "&.addMaxWidth": {
    [theme.breakpoints.down('sm')]: {
      maxWidth: "95px",
      ".MuiOutlinedInput-root": {
        padding: "6px",
      }
    }
  },
  ".MuiAutocomplete-input": {
    textOverflow: "clip",
  }
}));

const RecordTextField = styled(TextField)(({ theme }) => ({
  width: "100%",
}));

const NotesWrapper = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
  },
  ".desktop": {
    [theme.breakpoints.down('sm')]: {
      display: "none"
    }
  },
  // ".mobile": {
  //   display: "flex",
  //   alignItems: "center",
  //   [theme.breakpoints.up('sm')]: {
  //     display: "none"
  //   }
  // }
}));

const DeleteWrapper = styled("div")(({ theme }) => ({
  flex: 1,
  display: "flex",
  alignItems: "center",
  ".mobile": {
    display: "flex",
    [theme.breakpoints.up('sm')]: {
      display: "none"
    }
  }
}));

const SelectedRecord = styled(Typography)(({ theme }) => ({
  "&": theme.typography.body1,
  marginBottom: theme.spacing(4),
  marginBottom: "0",
  [theme.breakpoints.down('sm')]: {
    marginBottom: "0"
  }
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
  display: "flex",
  alignItems: "center",
  gap: theme.spacing(10),
  [theme.breakpoints.down('sm')]: {
    display: "block"
  }
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

const PatientEMRDetails = () => {
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
  const [emrId, setEMRId] = useState("");
  const [pmrFinished, setPmrFinished] = useState(false);
  const [pdfData, setPdfData] = useState({});
  const [submitEMRPayload, setSubmitEMRPayload] = useState({});
  const dataState = useSelector((state) => state);
  const [patientData, setPatientData] = useState({});
  const [step, setStep] = useState("create");
  const [showSync, setShowSync] = useState("");
  const [selectedAuthOption, setSelectedAuthOption] = useState("");
  const [number, setNumber] = useState("");
  const [symptomNumber, setSymptomNumber] = useState("");
  const [medicalHistoryNumber, setMedicalHistoryNumber] = useState("");
  const [dose, setDose] = useState("");
  const [documents, setDocuments] = useState(true);
  const navigate = useNavigate();
  const currentPatient = JSON.parse(patient);
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
  const [followUp, setFollowUp] = useState(null);
  const dispatch = useDispatch();

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  useEffect(() => {
    const queryParams = {
      term: "hea",
      state: "active",
      semantictag: "finding",
      acceptability: "preferred",
      returnlimit: 5,
    };

    dispatch(searchVitalsDetails(queryParams)).then((res) => {
      console.log("vitals:", res);
    });
    const currentPatient = JSON.parse(patient);
    if (Object.keys(currentPatient)?.length) {
      const emrPayload = {
        patient_id: currentPatient?.patientId,
        doc_id: currentPatient?.doc_id,
        appointment_id: currentPatient?.id,
        hip_id: currentPatient?.hip_id,
        consultation_status: "InProgress"
      };
      dispatch(getEMRId(emrPayload)).then((res) => {
        setEMRId(res.payload?.pmr_details.id);
        sessionStorage.setItem("pmrID", res.payload?.pmr_details.id); 
        const pmrDetails = res.payload?.pmr_details.pmr_data;
        if(pmrDetails){
          if(pmrDetails.vital){
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
            })
          }
          if(pmrDetails.symptom.data.length > 0){
            const symptomList = pmrDetails?.symptom.data;
            symptomList.map((symptomsData) => {
              setSymptoms(symptoms => [...symptoms, {
                label: symptomsData.symptom, 
                value: symptomsData.symptom,
                snowmed_code: symptomsData.snowmed_code,
                snowmed_display: symptomsData.snowmed_display,
              }]);
              setSymptomsSpecs(prevState  => ({...prevState,
                [symptomsData.symptom]: { 
                  since: symptomsData.duration, 
                  severity: symptomsData.severity, 
                  notes: symptomsData.notes 
                },
              }));
            });
           
          }
          if(pmrDetails.medical_history.data.length > 0){
            const medicalHistoryList = pmrDetails?.medical_history.data;
            medicalHistoryList.map((medicalHistoryData) => {
              setMedicalHistory(medicalHistory => [...medicalHistory, {
                label: medicalHistoryData.medical_history, 
                value: medicalHistoryData.medical_history,
                snowmed_code: medicalHistoryData.snowmed_code,
                snowmed_display: medicalHistoryData.snowmed_display,
              }]);
              setOptionTextValues(prevState  => ({...prevState,
                [medicalHistoryData.medical_history]: { 
                  since: medicalHistoryData.since, 
                  relationship: medicalHistoryData.relationship,
                  severity: medicalHistoryData.severity, 
                  notes: medicalHistoryData.notes 
                },
              }));
            });
          }
          if(pmrDetails.examination_findings.data.length > 0){
            const examinationFindingsList = pmrDetails?.examination_findings.data;
            examinationFindingsList.map((findingsData) => {
              setExamFinding(examFindings => [...examFindings, {
                label: findingsData.disease, 
                value: findingsData.disease,
                snowmed_code: findingsData.snowmed_code,
                snowmed_display: findingsData.snowmed_display,
              }]);
              setExaminationSpecs(prevState  => ({...prevState,
                [findingsData.disease]: { 
                  notes: findingsData.notes 
                },
              }));
            });
          }
          if(pmrDetails.diagnosis.data.length > 0){
            const diagnosisList = pmrDetails?.diagnosis.data;
            diagnosisList.map((diagnosisData) => {
              setDiagnosis(diagnosis => [...diagnosis, {
                label: diagnosisData.disease, 
                value: diagnosisData.disease,
                snowmed_code: diagnosisData.snowmed_code,
                snowmed_display: diagnosisData.snowmed_display,
              }]);
              setDiagnosisSpecs(prevState  => ({...prevState,
                [diagnosisData.disease]: { 
                  since: diagnosisData.status,
                  severity: diagnosisData.diagnosis_type,
                  notes: diagnosisData.notes 
                },
              }));
            });
          }
          if(pmrDetails.lab_investigation.data.length > 0){
            const labInvestigationList = pmrDetails?.lab_investigation.data;
            labInvestigationList.map((labInvestigationData) => {
              setLabInvestigation(labInvestigation => [...labInvestigation, {
                label: labInvestigationData.name, 
                value: labInvestigationData.name,
                snowmed_code: labInvestigationData.snowmed_code,
                snowmed_display: labInvestigationData.snowmed_display,
              }]);
              setLabInvestigationSpecs(prevState  => ({...prevState,
                [labInvestigationData.name]: { 
                  notes: labInvestigationData.notes 
                },
              }));
            });
          }
          if(pmrDetails.medication.data.length > 0){
            const medicationList = pmrDetails?.medication.data;
            medicationList.map((medicationData) => {
              setMedications(medications => [...medications, {
                label: medicationData.medicine_name, 
                value: medicationData.medicine_name,
                snowmed_code: medicationData.snowmed_code,
                snowmed_display: medicationData.snowmed_display,
              }]);
              setMedicationsSpecs(prevState  => ({...prevState,
                [medicationData.medicine_name]: { 
                  severity: medicationData.frequency,
                  timing: medicationData.time_of_day,
                  dose: medicationData.dosage,
                  since: medicationData.duration,
                },
              }));
            })
          }
        }
      });
    }
  }, []);

  const handleMeidcalHistoryChange = async (event) => {
    const inputValue = event.target.value;

    if (inputValue.length >= 3) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: inputValue,
        state: "active",
        semantictag: "situation",
        acceptability: "all",
        returnlimit: 5,
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
        setMedicalHistoryOpts(customData);
      });
    } else {
      setMedicalHistoryOpts([]);
    }
  };

  const handleExistingConditionsChange = async (event) => {
    const inputValue = event.target.value;

    if (inputValue.length >= 3) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: inputValue,
        state: "active",
        semantictag: "finding",
        acceptability: "preferred",
        returnlimit: 5,
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
    const inputValue = event.target.value;

    if (inputValue.length >= 3) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: inputValue,
        state: "active",
        semantictag: "finding",
        acceptability: "all",
        groupbyconcept: "true",
        returnlimit: 5,
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
        setSymptomsOpts(customData);
      });
    } else {
      setSymptomsOpts([]);
    }
  };
  const handleExamFindingsChange = async (event) => {
    const inputValue = event.target.value;

    if (inputValue.length >= 3) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: inputValue,
        state: "active",
        semantictag: "finding++observable entity++morphologic abnormality",
        acceptability: "all",
        returnlimit: 5,
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
        setExamFindingsOpts(customData);
      });
    } else {
      setExamFindingsOpts([]);
    }
  };
  const handleDiagnosisChange = async (event) => {
    const inputValue = event.target.value;

    if (inputValue.length >= 3) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: inputValue,
        state: "active",
        semantictag: "disorder",
        acceptability: "all",
        returnlimit: 5,
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
        setDiagnosisOpts(customData);
      });
    } else {
      setDiagnosisOpts([]);
    }
  };
  const handleMedicationsChange = async (event) => {
    const inputValue = event.target.value;

    if (inputValue.length >= 3) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: inputValue,
        state: "active",
        semantictag: "real clinical drug++substance",
        acceptability: "all",
        returnlimit: 5,
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
        setMedicationsOpts(customData);
      });
    } else {
      setMedicationsOpts([]);
    }
  };

  const handleLabInvestigationsChange = async (event) => {
    const inputValue = event.target.value;

    if (inputValue.length >= 3) {
      // Call your API here and fetch data based on the inputValue
      const queryParams = {
        term: inputValue,
        state: "active",
        semantictag: "procedure",
        acceptability: "all",
        returnlimit: 5,
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
        setLabInvestigationsOpts(customData);
      });
    } else {
      setLabInvestigationsOpts([]);
    }
  };

  const handleMedicalHistoryValue = (event, value) => {
    if (value) {
      // setShowMedicalHistory(true);
      const fieldValue = value;
      setOptionTextValues({
        ...optionTextValues,
        [value]: { since: "", relationship: "", severity: "", notes: "" },
      });
      setMedicalHistory([...medicalHistory, fieldValue]);
    }
  };
  const handleExistingConditions = (event, value) => {
    if (value) {
      const fieldValue = value;
      setExistingConditionsSpecs({
        ...existingConditionSpecs,
        [value]: { since: "", severity: "", notes: "" },
      });
      setExistingCondition([...existingConditions, fieldValue]);
    }
  };
  
  const handleSymptoms = (event, value) => {
    console.log(event, value);
    if (value) {
      const fieldValue = value;
      setSymptomsSpecs({
        ...symptomsSpecs,
        [value]: { since: "", severity: "", notes: "" },
      });
      setSymptoms([...symptoms, fieldValue]);
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
  
  const handleExaminationFindings = (event, value) => {
    if (value) {
      const fieldValue = value;
      setExaminationSpecs({
        ...symptomsSpecs,
        [value]: { notes: "" },
      });

      setExamFinding([...examFindings, fieldValue]);
      handleExaminationTextChange(value, "notes", "");
    }
  };
  const handleDiagnosis = (event, value) => {
    if (value) {
      const fieldValue = value;
      setDiagnosisSpecs({
        ...diagnosisSpecs,
        [value]: { since: "", severity: "", notes: "" },
      });
      setDiagnosis([...diagnosis, fieldValue]);
    }
  };
  const handleMedications = (event, value) => {
    if (value) {
      const fieldValue = value;
      setMedicationsSpecs({
        ...medicationsSpecs,
        [value]: { since: "", severity: "", notes: "" },
      });
      setMedications([...medications, fieldValue]);
    }
  };
  const handleLabInvestigations = (event, value) => {
    if (value) {
      const fieldValue = value;
      setLabInvestigationSpecs({
        ...labInvestigationSpecs,
        [value]: { since: "", severity: "", notes: "" },
      });
      setLabInvestigation([...labInvestigation, fieldValue]);
      handleLabTextChange(value, "notes", "");
    }
  };

  const prescriptionCommentChange = (event) => {
    setPrescriptionComment(event.target.value);
  };

  const adviceChange = (event) => {
    setAdvices(event.target.value);
  };

  const handleTextFieldChange = (option, textField, newValue) => {
    console.log(option, textField, newValue, "valuecheck");
    setOptionTextValues({
      ...optionTextValues,
      [option?.label]: {
        ...optionTextValues[option?.label],
        [textField]: newValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
    console.log({
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
    console.log({
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
    console.log(
      {
        ...examinationSpecs,
        [option?.label]: {
          ...examinationSpecs[option?.label],
          [textField]: newValue,
          snowmed_code: option?.snowmed_code,
          snowmed_display: option?.snowmed_display,
        },
      },
      "EXAM"
    );
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
    setMedicationsSpecs({
      ...medicationsSpecs,
      [option?.label]: {
        ...medicationsSpecs[option?.label],
        [textField]: newValue,
        snowmed_code: option?.snowmed_code,
        snowmed_display: option?.snowmed_display,
      },
    });
    console.log("MEDICATIONS", {
      ...medicationsSpecs,
      [option?.label]: {
        ...medicationsSpecs[option?.label],
        [textField]: newValue,
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
      console.log(inputObject, "inputobj");
      const objectDetails = inputObject[key];
      console.log(objectDetails, "objectdet");
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
    if (valueArr?.length && key !== "vital") {
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

  const createPdfBlob = async () => {
    const pdfBlob = await pdf(<PMRPdf patientData={patientData} />).toBlob();

    const pdfFile = new File([pdfBlob], "patient_record.pdf", {
      type: "application/pdf",
    });

    return pdfFile;
  };

  const handleModalClose = () => {
    setShowSync(false);
  };

  const postPMR = async () => {
    const pmr_request = pdfData;
    pmr_request["pmr_id"] = emrId;
    // pmr_request["advice"] = {
    //   advices: advices,
    // };
    pmr_request["advice"] = advices
    pmr_request["notes"] = prescriptionComment

    const pdfPayload = {
      document_type: "Prescription",
      pmr_id: emrId,
    };
    const current_patientt = JSON.parse(patient);
    const appointment_request = {
      appointment_id: current_patientt?.id,
      followup_date: followUp ? convertDateFormat(followUp, "yyyy-MM-dd") : "",
      consultation_status: "Completed"
    }
    const allData ={
      pmr_request, appointment_request
    }
    const blob = await createPdfBlob();
    dispatch(submitPdf({ blob, pdfPayload })).then(
      dispatch(postEMR(allData)).then((res) => {
        if (
          !(
            currentPatient?.patient_details?.abha_number &&
            currentPatient?.patient_details?.abha_number !== ""
          )
        ) {
          navigate("/appointment-list");
          sessionStorage.removeItem("pmrID");
          // ("/appointment-list");
        }
      })
    );
    const currentPatient = JSON.parse(
      sessionStorage.getItem("selectedPatient")
    );
    if (userRole === "ADMIN" && 
      currentPatient?.patient_details?.abha_number &&
      currentPatient?.patient_details?.abha_number !== ""
    ) {
      setShowSync(true);
    }
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
  const submitEMR = () => {
    console.log(
      medicalHistory,
      existingConditions,
      symptoms,
      examFindings,
      diagnosis,
      medications,
      labInvestigation,
      "---------Selected Data------------"
    );

    const symptomsEMR = symptomObj(symptomsSpecs);
    const diagnosisEMR = diagnosisObj(diagnosisSpecs);
    const conditionEMR = conditonObject(existingConditionSpecs);
    const examinEMR = diseaseObject(examinationSpecs);
    const medicationEMR = medicationObj(medicationsSpecs);
    const currentMedicationEMR = currentMedicationObj();
    const labInvestigationEMR = labInvestigationObj(labInvestigationSpecs);
    const medicalHistoryEMR = medicalHistoryObj(optionTextValues);

    console.log(formValues, "formValues");

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
        patientName: currentPatient?.patient_details?.name || currentPatient?.name || "-",
        doctorName: currentPatient?.docName || "-",
        patientEmail: currentPatient?.patient_details?.email || currentPatient?.email || "-",
        patientGender: currentPatient?.patient_details?.gender || currentPatient?.gender || "-",
        patientNumber: currentPatient?.mobileNumber || currentPatient?.mobile_number || "-",
        patientId: currentPatient?.patientId || "-",
        patientAge: "-",
      };
    }
    setPatientData(patientDetails);
    setPdfData(submitEMRPayload);

    console.log(submitEMRPayload, "payload");

    sessionStorage.setItem("patientDetailsPdf", JSON.stringify(patientDetails));
    sessionStorage.setItem(
      "patientEMRDetails",
      JSON.stringify(submitEMRPayload)
    );
    setPmrFinished(true);
    setStep("preview");
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
    pmr_request["advice"] = advices
    pmr_request["notes"] = prescriptionComment

    const appointment_request = {
      appointment_id: currentPatient?.id,
      followup_date: followUp ? convertDateFormat(followUp, "yyyy-MM-dd") : "",
      consultation_status: "Completed"
    }
    const allData ={
      pmr_request, appointment_request
    }
   
    dispatch(postEMR(allData)).then((res) => {
      if (
        !(
          currentPatient?.patient_details?.abha_number &&
          currentPatient?.patient_details?.abha_number !== ""
        )
      ) {
        navigate("/appointment-list");
        sessionStorage.removeItem("pmrID");
      }
    })
  }

  const editPMR = () => {
    setStep("create");
  };
  const relationshipOptions = ["self", "father", "mother", "sister", "daughter"];
  const diagnosisStatusOpts = ["Suspected", "Confirmed", "Ruled out"];
  const diagnosisTypeOpts = ["Primary Diagnosis", "Differential Diagnosis"];
  const timeOptions = ["Days", "Weeks", "Months", "Years"];
  const doseOptions = ["Tablet"];
  const timingOptions = [
    "After Meal",
    "Before Meal",
    "With Meal",
    "Empty Stomach",
    "before breakfast",
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
    if (isNaN(parsedNumber) || !item?.label) {
      return [];
    }
    const sinceValue = medicationsSpecs[item?.label]?.since;
    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return timeOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }
    return [];
  };

  const generateSymptomsOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);

    if (isNaN(parsedNumber) || !item?.label) {
      return [];
    }

    const sinceValue = symptomsSpecs[item.label]?.since;

    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return timeOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }

    return [];
  };

  const generateHistoryOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);
    if (isNaN(parsedNumber) || !item?.label) {
      return [];
    }
    const sinceValue = optionTextValues[item?.label]?.since;
    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return timeOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }
    return [];
  };

  const generateSymptomsOptionChange = (option, newValue, key) => {
    console.log("options", option, newValue, key);
    handleSymtomsTextChange(option, key, newValue);
  };

  const generateMedicalHistoryOptionChange = (option, newValue) => {
    console.log("options", option, newValue, 'since');
    handleTextFieldChange(option, 'since', newValue);
  };

  const generateDoseOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);

    if (isNaN(parsedNumber) || !item?.label) {
      return [];
    }

    const sinceValue = medicationsSpecs[item?.label]?.dose || "";

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

  return (
    <PatientEMRWrapper>
      {step === "create" && <PatientDetailsHeader
        documents={documents} />}
      {step === "create" && (
        <EMRFormWrapper>
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
                        <DiastolicTextField
                          fullWidth
                          variant="outlined"
                          name="diastolicaBP"
                          value={formValues.diastolicaBP}
                          onChange={handleInputChange}
                          className="emr-input-field"
                        />
                        <Divider>/</Divider>
                        <SystolicTextField
                          fullWidth
                          variant="outlined"
                          name="systolicBP"
                          value={formValues.systolicBP}
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
                  <Typography variant="subtitle1">Respiratory rate</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={8}>
                      <TextField
                        fullWidth
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
                  <Typography variant="subtitle1">Body Temperature</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={8}>
                      <TextField
                        fullWidth
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
                />
                {symptoms?.length > 0 && (
                  <div>
                    {symptoms?.map((item) => (
                      <FieldSpecsContainer>
                        <RecordLayout>
                          <SelectedRecord>{item?.label}</SelectedRecord>
                        </RecordLayout>
                        <TextBoxLayout className="addMaxWidth">
                          <Autocomplete                          
                            className="sinceAutocomplete"
                            options={generateSymptomsOptions(symptomNumber, item)}
                            value={symptomsSpecs[item?.label]?.since || ""}
                            onChange={(e, newValue) =>
                              generateSymptomsOptionChange(item, newValue, "since")
                            }
                            // inputValue={symptomNumber}
                            onInputChange={(e, newValue) =>
                              handleSymptomNumberOptions(item, newValue)
                            }
                            renderInput={(params) => (
                              <TextField
                                {...params}
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
                              value={symptomsSpecs[item?.label]?.notes || ""}
                              onChange={(e) =>
                                handleSymtomsTextChange(item, "notes", e.target.value)
                              }
                              label="Notes"
                              variant="outlined"
                            />
                          </TextBoxLayout>
                          
                       
                          </NotesWrapper>
                          <DeleteWrapper>
                          <p onClick={handleOpenComplaintNotes} className="mobile"><NotesField /></p>
                          <Modal
                            open={openComplaintNotes}
                            onClose={handleCloseComplaintNotes}
                            aria-labelledby="modal-modal-title"
                            aria-describedby="modal-modal-description"
                          >
                            <Box sx={style}>
                              <Typography id="modal-modal-title" variant="h3">
                                Complaints Note
                              </Typography>
                              <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                <TextBoxLayout>
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={symptomsSpecs[item?.label]?.notes || ""}
                                    onChange={(e) =>
                                      handleSymtomsTextChange(item, "notes", e.target.value)
                                    }
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </Typography>
                              <PrimaryButton onClick={handleCloseComplaintNotes} sx={{marginTop: "10px", float: "right"}}>Submit</PrimaryButton>
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
                  autocompleteRef={medicalHistoryRef}
                />
                {medicalHistory?.length > 0 && (
                  <div>
                    {medicalHistory?.map((item) => (
                      <FieldSpecsContainer>
                        <RecordLayout className="addMaxWidth">
                          <SelectedRecord>{item?.label}</SelectedRecord>
                        </RecordLayout>
                        <TextBoxLayout className="addMaxWidth">
                          {/* <RecordTextField
                            placeholder="Since"
                            value={optionTextValues[item?.label]?.since || ""}
                            onChange={(e) =>
                              handleTextFieldChange(item, "since", e.target.value)
                            }
    variant="outlined"
                          /> */}
                         <Autocomplete
                            options={generateHistoryOptions(medicalHistoryNumber, item)}
                            value={optionTextValues[item?.label]?.since || ""}
                            onChange={(e, newValue) =>
                              generateMedicalHistoryOptionChange(item, newValue)
                            }
                            // inputValue={symptomNumber}
                            onInputChange={(e, newValue) =>
                              handleHistoryNumberOptions(item, newValue)
                            }
                            renderInput={(params) => (
                              <TextField
                                {...params}
                                label="Since"
                                variant="outlined"
                              />
                            )}
                          />
                        </TextBoxLayout>
                        <TextBoxLayout className="addMaxWidth">
                          <Autocomplete
                            options={relationshipOptions}
                            value={
                              optionTextValues[item?.label]?.relationship || ""
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
                              value={optionTextValues[item?.label]?.notes || ""}
                              onChange={(e) =>
                                handleTextFieldChange(item, "notes", e.target.value)
                              }
                              label="Notes"
                              variant="outlined"
                            />
                          </TextBoxLayout>
                          
                     
                        </NotesWrapper>
                        <DeleteWrapper>
                        <p onClick={handleOpenMedicalHistory} className="mobile"><NotesField /></p>
                          <Modal
                            open={openMedicalHistory}
                            onClose={handleCloseMedicalHistory}
                            aria-labelledby="modal-modal-title"
                            aria-describedby="modal-modal-description"
                          >
                            <Box sx={style}>
                              <Typography id="modal-modal-title" variant="h3">
                                Patient Medical History Notes
                              </Typography>
                              <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                <TextBoxLayout>
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={optionTextValues[item?.label]?.notes || ""}
                                    onChange={(e) =>
                                      handleTextFieldChange(item, "notes", e.target.value)
                                    }
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </Typography>
                              <PrimaryButton onClick={handleCloseMedicalHistory} sx={{marginTop: "10px", float: "right"}}>Submit</PrimaryButton>
                            </Box>
                          </Modal>
                          <DeleteField onClick={handleOptionRemove(item?.label)}>
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
                />
                {examFindings?.length > 0 && (
                  <div>
                    {examFindings?.map((item) => (
                      <FieldSpecsContainer>
                        <RecordLayout>
                          <SelectedRecord>{item?.label}</SelectedRecord>
                        </RecordLayout>
                        <NotesWrapper>
                          <TextBoxLayout className="desktop">
                            <RecordTextField
                              placeholder="Notes"
                              value={examinationSpecs[item?.label]?.notes || ""}
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
                          <p onClick={handleOpenFindingNotes} className="mobile"><NotesField /></p>
                          <Modal
                            open={openFindingNotes}
                            onClose={handleCloseFindingNotes}
                            aria-labelledby="modal-modal-title"
                            aria-describedby="modal-modal-description"
                          >
                            <Box sx={style}>
                              <Typography id="modal-modal-title" variant="h3">
                                Examination Finding Notes
                              </Typography>
                              <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                <TextBoxLayout>
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={examinationSpecs[item?.label]?.notes || ""}
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
                              <PrimaryButton onClick={handleCloseFindingNotes} sx={{marginTop: "10px", float: "right"}}>Submit</PrimaryButton>
                            </Box>
                          </Modal>
                          <DeleteField
                            onClick={handleExaminationSpecsDelete(item?.label)}
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
                />
                {diagnosis?.length > 0 && (
                  <div>
                    {diagnosis?.map((item) => (
                      <FieldSpecsContainer>
                        <RecordLayout className="addMaxWidth">
                          <SelectedRecord>{item?.label}</SelectedRecord>
                        </RecordLayout>
                        <TextBoxLayout className="addMaxWidth">
                          <Autocomplete
                            options={diagnosisStatusOpts}
                            value={diagnosisSpecs[item?.label]?.since || ""}
                            onChange={(e, newValue) =>
                              handleDiganosisOptionChange(item, newValue, "since")
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
                        <TextBoxLayout className="addMaxWidth">
                          <Autocomplete
                            options={diagnosisTypeOpts}
                            value={diagnosisSpecs[item?.label]?.severity || ""}
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
                              value={diagnosisSpecs[item?.label]?.notes || ""}
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
                        <p onClick={handleOpenDiagnosisNotes} className="mobile"><NotesField /></p>
                          <Modal
                            open={openDiagnosisNotes}
                            onClose={handleCloseDiagnosisNotes}
                            aria-labelledby="modal-modal-title"
                            aria-describedby="modal-modal-description"
                          >
                            <Box sx={style}>
                              <Typography id="modal-modal-title" variant="h3">
                                Diagnosis Notes
                              </Typography>
                              <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                <TextBoxLayout>
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={diagnosisSpecs[item?.label]?.notes || ""}
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
                              <PrimaryButton onClick={handleCloseDiagnosisNotes} sx={{marginTop: "10px", float: "right"}}>Submit</PrimaryButton>
                            </Box>
                          </Modal>
                          <DeleteField
                            onClick={handleDiagnosisSpecsDelete(item?.label)}
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
                />
                {labInvestigation?.length > 0 && (
                  <div>
                    {labInvestigation?.map((item) => (
                      <FieldSpecsContainer>
                        <RecordLayout>
                          <SelectedRecord>{item?.label}</SelectedRecord>
                        </RecordLayout>
                        <NotesWrapper>
                          <TextBoxLayout className="desktop">
                            <RecordTextField
                              placeholder="Notes"
                              value={labInvestigationSpecs[item?.label]?.notes || ""}
                              onChange={(e) =>
                                handleLabTextChange(item, "notes", e.target.value)
                              }
                              label="Notes"
                              variant="outlined"
                            />
                          </TextBoxLayout>
                          
                        
                        </NotesWrapper>
                        <DeleteWrapper>  
                          <p onClick={handleOpenLabNotes} className="mobile"><NotesField /></p>
                          <Modal
                            open={openLabNotes}
                            onClose={handleCloseLabNotes}
                            aria-labelledby="modal-modal-title"
                            aria-describedby="modal-modal-description"
                          >
                            <Box sx={style}>
                              <Typography id="modal-modal-title" variant="h3">
                                Lab Investigation Notes
                              </Typography>
                              <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                                <TextBoxLayout>
                                  <RecordTextField
                                    placeholder="Notes"
                                    value={labInvestigationSpecs[item?.label]?.notes || ""}
                                    onChange={(e) =>
                                      handleLabTextChange(item, "notes", e.target.value)
                                    }
                                    variant="outlined"
                                  />
                                </TextBoxLayout>
                              </Typography>
                              <PrimaryButton onClick={handleCloseLabNotes} sx={{marginTop: "10px", float: "right"}}>Submit</PrimaryButton>
                            </Box>
                          </Modal>
                          <DeleteField onClick={handleLabSpecsDelete(item?.label)}>
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
                />
                {medications?.length > 0 && (
                  <div>
                    {medications?.map((item) => (
                      <FieldSpecsContainer>
                        <RecordLayout>
                          <SelectedRecord>{item?.label}</SelectedRecord>
                        </RecordLayout>
                        <TextBoxLayout className="desktopTextBoxLayout">
                          <RecordTextField
                            placeholder="Frequency"
                            value={medicationsSpecs[item?.label]?.severity || ""}
                            onChange={(e) =>
                              handleMedicationsTextChange(
                                item,
                                "severity",
                                e.target.value
                              )
                            }
                            label="Frequency"
                            variant="outlined"
                          />
                        </TextBoxLayout>
                        <TextBoxLayout className="desktopTextBoxLayout">
                          <Autocomplete
                            options={timingOptions} // Replace with your actual timing options
                            value={medicationsSpecs[item?.label]?.timing || null}
                            onChange={(event, newValue) =>
                              handleMedicationsTextChange(item, "timing", newValue)
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
                        <TextBoxLayout className="addMaxWidth">
                          <Autocomplete
                            options={generateDoseOptions(dose, item)}
                            value={medicationsSpecs[item?.label]?.dose || ""}
                            onChange={(e, newValue) =>
                              handleMedicationOptionsChange(item, newValue, "dose")
                            }
                            // inputValue={dose}
                            onInputChange={(e, newVal) =>
                              handleDoseOptions(e, newVal)
                            }
                            renderInput={(params) => (
                              <TextField
                                {...params}
                                label="Dose"
                                variant="outlined"
                              />
                            )}
                          />

                        </TextBoxLayout>
                        <TextBoxLayout className="addMaxWidth">
                          <Autocomplete
                            options={generateOptions(number, item)}
                            value={medicationsSpecs[item?.label]?.since || ""}
                            onChange={(e, newValue) =>
                              handleMedicationOptionsChange(item, newValue, "since")
                            }
                            // inputValue={number}
                            onInputChange={(e, newValue) =>
                              handleNumberOptions(item, newValue)
                            }
                            renderInput={(params) => (
                              <TextField
                                {...params}
                                label="Duration"
                                variant="outlined"
                              />
                            )}
                          />
                        </TextBoxLayout>
                        <TextBoxLayout className="mobileTextBoxLayout">
                          <RecordTextField
                            placeholder="Frequency"
                            value={medicationsSpecs[item?.label]?.severity || ""}
                            onChange={(e) =>
                              handleMedicationsTextChange(
                                item,
                                "severity",
                                e.target.value
                              )
                            }
                            label="Frequency"
                            variant="outlined"
                          />
                        </TextBoxLayout>
                        <TextBoxLayout className="mobileTextBoxLayout">
                          <Autocomplete
                            options={timingOptions} // Replace with your actual timing options
                            value={medicationsSpecs[item?.label]?.timing || null}
                            onChange={(event, newValue) =>
                              handleMedicationsTextChange(item, "timing", newValue)
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
                        <DeleteWrapper>
                          <DeleteField
                            onClick={handleMedicationsSpecsDelete(item?.label)}
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
              <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DemoContainer components={['DatePicker']}>
                  <DatePicker sx={{ width: '100%' }} 
                    disablePast
                    value={followUp}
                    onChange={(newValue) => setFollowUp(newValue)}
                  />
                </DemoContainer>
              </LocalizationProvider>
              </VitalsContainer>


              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <VitalsContainer>
                    <SectionHeader>Notes</SectionHeader>
                    <div>
                      <RecordTextField
                        placeholder="Add your notes here"
                        className="notes-field"
                        onChange={prescriptionCommentChange}
                      />
                    </div>
                  </VitalsContainer>
                </Grid>
                <Grid item xs={12} md={6}>
                  <VitalsContainer>
                    <SectionHeader>Advices</SectionHeader>
                    <div>
                      <RecordTextField
                        placeholder="Add your advices here"
                        className="notes-field"
                        onChange={adviceChange}
                      />
                    </div>
                  </VitalsContainer>
                </Grid>
              </Grid>
            </>
          )}
          <EMRFooter>
            <SecondaryButton onClick={resetEMRForm}>Clear</SecondaryButton>
            <PrimaryButton onClick={saveEMR}>
              Save
            </PrimaryButton>
            <PrimaryButton onClick={submitEMR}>
              Review Prescription
            </PrimaryButton>
          </EMRFooter>
        </EMRFormWrapper>
      )}
      {pmrFinished && step === "preview" && (
        <PdfDisplayWrapper>
          {/* <PageTitle>Preview</PageTitle>
          <PageSubText>
            Closely Review the Details Before Confirming
          </PageSubText> */}
          <SyncAabha
            showSync={showSync}
            handleModalClose={handleModalClose}
            setSelectedAuthOption={setSelectedAuthOption}
            selectedAuthOption={selectedAuthOption}
          />
          <PDFViewerWrapper>
            <PDFViewer style={{ width: "100%", height: "100%" }} zoom={1}>
              <PMRPdf pdfData={submitEMRPayload} patientData={patientData} />
            </PDFViewer>
          </PDFViewerWrapper>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <SecondaryButton onClick={editPMR}>Edit</SecondaryButton>
            <PrimaryButton onClick={postPMR}>Finish Prescription</PrimaryButton>
          </div>
        </PdfDisplayWrapper>
      )}
    </PatientEMRWrapper>
  );
};

export default PatientEMRDetails;
