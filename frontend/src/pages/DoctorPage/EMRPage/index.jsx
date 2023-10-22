import React, { useEffect, useRef } from "react";
import AutoSearch from "../../../components/AutoSearch";
import PatientDetailsHeader from "../../../components/PatientDetailsHeader";
import {
  Typography,
  styled,
  TextField,
  Grid,
  filledInputClasses,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getEMRId, postEMR, searchVitalsDetails } from "./EMRPage.slice";
import CustomAutoComplete from "../../../components/CustomAutoComplete";
import { Button } from "@mui/base";
import { PDFViewer, pdf } from "@react-pdf/renderer";
import PMRPdf from "../../../components/PMRPdf";
import { submitPdf } from "../../../components/PMRPdf/pmrPdf.slice";
import { useNavigate } from "react-router-dom";
const PatientEMRWrapper = styled("div")(({ theme }) => ({}));

const EMRFormWrapper = styled("div")(({ theme }) => ({}));

const VitalsContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    marginTop: theme.spacing(4),
    padding: theme.spacing(6),
    borderRadius: theme.spacing(1),
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
      height: "48px",
      borderRadius: "0",
    },
  },
}));

const VitalValue = styled("div")(({ theme }) => ({
  "&": {
    padding: theme.spacing(3),
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

const PrimaryButton = styled("Button")(({ theme }) => ({
  "&": theme.typography.primaryButton,
}));

const SecondaryButton = styled("Button")(({ theme }) => ({
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
  height: theme.spacing(8),
  borderRadius: theme.spacing(1.5),
}));

const TextBoxLayout = styled("div")(({ theme }) => ({
  flex: 1,
}));

const RecordTextField = styled(TextField)(({ theme }) => ({
  width: "100%",
}));
const DeleteWrapper = styled("div")(({ theme }) => ({
  flex: 1,
  display: "flex",
  alignItems: "center",
}));

const SelectedRecord = styled(Typography)(({ theme }) => ({
  "&": theme.typography.body1,
  marginBottom: theme.spacing(4),
}));

const DeleteField = styled(DeleteIcon)(({ theme }) => ({
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
}));

const PatientEMRDetails = () => {
  const [medicalHistoryoptions, setMedicalHistoryOptions] = useState([]);
  const [existingConditionsOpts, setExistingConditionOpts] = useState([]);
  const [symptomsOpts, setSymptomsOpts] = useState([]);
  const [examFindingsOpts, setExamFindingsOpts] = useState([]);
  const [diagnosisOpts, setDiagnosisOpts] = useState([]);
  const [medicationsOpts, setMedicationsOpts] = useState([]);
  const [labInvestigationsOpts, setLabInvestigationsOpts] = useState([]);
  const [medicalHistory, setMedicalHistory] = useState([]);
  const [existingConditions, setExistingCondition] = useState([]);
  const [symptoms, setSymptoms] = useState([]);
  const [examFindings, setExamFinding] = useState([]);
  const [diagnosis, setDiagnosis] = useState([]);
  const [medications, setMedications] = useState([]);
  const [labInvestigation, setLabInvestigation] = useState([]);
  const [prescriptionComment, setPrescriptionComment] = useState("");
  const [advices, setAdvices] = useState("");
  const [showSeveritySymptomps, setShowSeveritySymptomps] = useState(false);
  const [showMedicalHistory, setShowMedicalHostory] = useState(false);
  const [optionTextValues, setOptionTextValues] = useState({});
  const [existingConditionSpecs, setExistingConditionsSpecs] = useState({});
  const [symptomsSpecs, setSymptomsSpecs] = useState({});
  const [examinationSpecs, setExaminationSpecs] = useState({});
  const [diagnosisSpecs, setDiagnosisSpecs] = useState({});
  const [medicationsSpecs, setMedicationsSpecs] = useState({});
  const [labInvestigationSpecs, setLabInvestigationSpecs] = useState({});
  const medicalHistoryRef = useRef(null);
  const patient = sessionStorage?.getItem("selectedPatient");
  const [emrId, setEMRId] = useState("");
  const [pmrFinished, setPmrFinished] = useState(false);
  const [pdfData, setPdfData] = useState({});
  const [submitEMRPayload, setSubmitEMRPayload] = useState({});
  const dataState = useSelector((state) => state);
  const [patientData, setPatientData] = useState({});
  const [step, setStep] = useState("create");
  const navigate = useNavigate();

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
      };
      dispatch(getEMRId(emrPayload)).then((res) => {
        setEMRId(res.payload?.pmr_id);
        sessionStorage.setItem("pmrID", res.payload?.pmr_id);
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
        semantictag: "disorder",
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
        setMedicalHistoryOptions(customData);
      });
    } else {
      setMedicalHistoryOptions([]);
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
        semantictag: "observable entity",
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
        semantictag: "clinical drug",
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
        setLabInvestigationsOpts(customData);
      });
    } else {
      setLabInvestigationsOpts([]);
    }
  };

  const handleMedicalHistoryValue = (event, value) => {
    console.log(value);
    if (value) {
      setShowMedicalHostory(true);
      const fieldValue = value;
      console.log(fieldValue, "field");
      setOptionTextValues({
        ...optionTextValues,
        [value]: { since: "", severity: "", notes: "" },
      });
      setMedicalHistory([...medicalHistory, fieldValue]);
      console.log([...medicalHistory, fieldValue]);
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
    if (value) {
      const fieldValue = value;
      setSymptomsSpecs({
        ...symptomsSpecs,
        [value]: { since: "", severity: "", notes: "" },
      });
      setSymptoms([...symptoms, fieldValue]);
    }
  };
  const handleExaminationFindings = (event, value) => {
    if (value) {
      const fieldValue = value;
      setExaminationSpecs({
        ...symptomsSpecs,
        [value]: { since: "", severity: "", notes: "" },
      });
      setExamFinding([...examFindings, fieldValue]);
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
        snowmed_code: [option?.snowmed_code],
        snowmed_display: [option?.snowmed_display],
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
    setMedicationsSpecs({
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
        duration: objectDetails.since,
        status: objectDetails.severity,
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
        dosage: "3",
        time_of_day: "morning",
        duration: objectDetails.since,
        duration_period: "",
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
        severity: objectDetails.severity,
        since: objectDetails.since,
        notes: objectDetails.since,
        snowmed_code: objectDetails?.snowmed_code || "",
        snowmed_display: objectDetails?.snowmed_display || "",
      };
      result.push(transformedItem);
    }
    const filteredResult = result.filter(
      (item) => item.diabetes_melitus !== "[object Object]"
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

  const postPMR = async () => {
    const filteredPayload = pdfData;
    filteredPayload["pmr_id"] = emrId;
    filteredPayload["advice"] = {
      advices: advices,
    };
    filteredPayload["notes"] = {
      notes: prescriptionComment,
    };

    const pdfPayload = {
      document_type: "Prescription",
      pmr_id: emrId,
    };
    const blob = await createPdfBlob();
    dispatch(submitPdf({ blob, pdfPayload })).then(
      dispatch(postEMR(filteredPayload)).then((res) => {
        sessionStorage.removeItem("pmrID");
        navigate("/appointment-list");
      })
    );
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
    const diagnosisEMR = diseaseObject(diagnosisSpecs);
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
          body_mass_index: formValues?.bodyMass,
          systolic_blood_pressure: formValues?.systolicBP,
          diastolic_blood_pressure: formValues?.diastolicaBP,
        },
      },
      {
        key: "condition",
        dataArr: conditionEMR,
      },
      {
        key: "examinationFindings",
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
        key: "currentMedication",
        dataArr: [],
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
    const patient = sessionStorage?.getItem("selectedPatient");
    let patientDetails = {};
    if (hospital) {
      const currentHospital = JSON.parse(hospital);
      const currentPatient = JSON.parse(patient);
      patientDetails = {
        hospitalName: currentHospital?.name || "-",
        patientName: currentPatient?.patient_details?.name || "-",
        doctorName: currentPatient?.docName || "-",
        patientEmail: currentPatient?.patient_details?.email || "-",
        patientGender: currentPatient?.patient_details?.gender || "-",
        patientNumber: currentPatient?.mobileNumber || "-",
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
  const dummy = {
    pmr_id: "string",
    vital: {
      height: "string",
      weight: "string",
      pulse: "string",
      blood_pressure: "string",
      body_temperature: "string",
      oxygen_saturation: "string",
      respiratory_rate: "string",
      body_mass_index: "string",
      systolic_blood_pressure: "string",
      diastolic_blood_pressure: "string",
    },
    condition: {
      data: [
        {
          condition: "string",
          start_date: "string",
          status: "string",
          notes: "string",
          snowmed_code: "string",
          snowmed_display: "string",
        },
      ],
    },
    examinationFindings: {
      data: [
        {
          disease: "string",
          duration: "string",
          status: "string",
          snowmed_code: "string",
          snowmed_display: "string",
        },
      ],
    },
    diagnosis: {
      data: [
        {
          disease: "string",
          duration: "string",
          status: "string",
          notes: "string",
          snowmed_code: "string",
          snowmed_display: "string",
        },
      ],
    },
    symptom: {
      data: [
        {
          symptom: "string",
          duration: "string",
          severity: "string",
          notes: "string",
          start_date: "string",
          snowmed_code: "string",
          snowmed_display: "string",
        },
      ],
    },
    medication: {
      data: [
        {
          medicine_name: "string",
          frequency: "string",
          dosage: "string",
          time_of_day: "string",
          duration: "string",
          duration_period: "string",
          notes: "string",
          snowmed_code: "string",
          snowmed_display: "string",
        },
      ],
    },
    currentMedication: {
      data: [
        {
          medicine_name: "string",
          start_date: "string",
          status: "string",
          notes: "string",
          snowmed_code: "string",
          snowmed_display: "string",
        },
      ],
    },
    lab_investigation: {
      data: [
        {
          name: "string",
          snowmed_code: "string",
          snowmed_display: "string",
        },
      ],
    },
    medical_history: {
      data: [
        {
          medical_history: "string",
          since: "string",
          severity: "string",
          notes: "string",
          snowmed_code: "string",
          snowmed_display: "string",
        },
      ],
    },
    advice: {
      advices: "string",
    },
    notes: {
      notes: "string",
    },
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

  const editPMR = () => {
    setStep("create");
  };

  return (
    <PatientEMRWrapper>
      {step === "create" && <PatientDetailsHeader />}
      {step === "create" && (
        <EMRFormWrapper>
          <VitalsContainer>
            <SectionHeader>Vitals</SectionHeader>
            <form>
              <Grid container spacing={8}>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">Pulse Rate</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="pulseRate"
                        value={formValues.pulseRate}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>/min</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">
                    Peripheral oxygen saturation
                  </Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="oxygenSaturation"
                        value={formValues.oxygenSaturation}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>%</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">Blood Pressure</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="bloodPressure"
                        value={formValues.bloodPressure}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>mmHg</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">Respiratory rate</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="respiratoryRate"
                        value={formValues.respiratoryRate}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>/min</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">Body Temperature</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="bodyTemp"
                        value={formValues.bodyTemp}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>C</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">Body height</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="bodyHeight"
                        value={formValues.bodyHeight}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>Cms</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">Body weight</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="bodyWeight"
                        value={formValues.bodyWeight}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>Kgs</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">Body mass index</Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="bodyMass"
                        value={formValues.bodyMass}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>Kg/m2</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">
                    Systolic blood pressure
                  </Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="systolicBP"
                        value={formValues.systolicBP}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>mmHg</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="subtitle1">
                    Diastolic blood pressure
                  </Typography>
                  <TextFieldWrapper>
                    <Grid item xs={12} sm={10}>
                      <TextField
                        fullWidth
                        variant="outlined"
                        name="diastolicaBP"
                        value={formValues.diastolicaBP}
                        onChange={handleInputChange}
                        className="emr-input-field"
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <VitalValue>mmHg</VitalValue>
                    </Grid>
                  </TextFieldWrapper>
                </Grid>
              </Grid>
            </form>
          </VitalsContainer>
          <VitalsContainer>
            <SectionHeader>Patient Medical History</SectionHeader>
            <CustomAutoComplete
              options={medicalHistoryoptions}
              handleInputChange={handleMeidcalHistoryChange}
              setOptions={setMedicalHistoryOptions}
              handleOptionChange={handleMedicalHistoryValue}
              autocompleteRef={medicalHistoryRef}
            />
            {medicalHistory?.length > 0 && showMedicalHistory && (
              <div>
                {medicalHistory?.map((item) => (
                  <FieldSpecsContainer>
                    <RecordLayout>
                      <SelectedRecord>{item?.label}</SelectedRecord>
                    </RecordLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Since"
                        value={optionTextValues[item?.label]?.since || ""}
                        onChange={(e) =>
                          handleTextFieldChange(item, "since", e.target.value)
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Severity"
                        value={optionTextValues[item?.label]?.severity || ""}
                        onChange={(e) =>
                          handleTextFieldChange(
                            item,
                            "severity",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
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
                    <DeleteWrapper>
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
            <SectionHeader>Existing Conditions</SectionHeader>
            <CustomAutoComplete
              options={existingConditionsOpts}
              handleInputChange={handleExistingConditionsChange}
              setOptions={setExistingConditionOpts}
              handleOptionChange={handleExistingConditions}
            />
            {existingConditions?.length > 0 && (
              <div>
                {existingConditions?.map((item) => (
                  <FieldSpecsContainer>
                    <RecordLayout>
                      <SelectedRecord>{item?.label}</SelectedRecord>
                    </RecordLayout>
                    <TextBoxLayout>
                      {" "}
                      <RecordTextField
                        placeholder="Since"
                        value={existingConditionSpecs[item?.label]?.since || ""}
                        onChange={(e) =>
                          exisitingConditionsTextChange(
                            item,
                            "since",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Severity"
                        value={
                          existingConditionSpecs[item?.label]?.severity || ""
                        }
                        onChange={(e) =>
                          exisitingConditionsTextChange(
                            item,
                            "severity",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Notes"
                        value={existingConditionSpecs[item?.label]?.notes || ""}
                        onChange={(e) =>
                          exisitingConditionsTextChange(
                            item,
                            "notes",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <DeleteWrapper>
                      <DeleteField
                        onClick={handleExistingConditionsSpecDelete(
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
            <SectionHeader> Symptoms</SectionHeader>
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
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Since"
                        value={symptomsSpecs[item?.label]?.since || ""}
                        onChange={(e) =>
                          handleSymtomsTextChange(item, "since", e.target.value)
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Severity"
                        value={symptomsSpecs[item?.label]?.severity || ""}
                        onChange={(e) =>
                          handleSymtomsTextChange(
                            item,
                            "severity",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
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
                    <DeleteWrapper>
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
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Since"
                        value={examinationSpecs[item?.label]?.since || ""}
                        onChange={(e) =>
                          handleExaminationTextChange(
                            item,
                            "since",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Severity"
                        value={examinationSpecs[item?.label]?.severity || ""}
                        onChange={(e) =>
                          handleExaminationTextChange(
                            item,
                            "severity",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
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
                    <DeleteWrapper>
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
                    <RecordLayout>
                      <SelectedRecord>{item?.label}</SelectedRecord>
                    </RecordLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Since"
                        value={diagnosisSpecs[item?.label]?.since || ""}
                        onChange={(e) =>
                          handleDiagnosisTextChange(
                            item,
                            "since",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Severity"
                        value={diagnosisSpecs[item?.label]?.severity || ""}
                        onChange={(e) =>
                          handleDiagnosisTextChange(
                            item,
                            "severity",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
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
                    <DeleteWrapper>
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
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Since"
                        value={medicationsSpecs[item?.label]?.since || ""}
                        onChange={(e) =>
                          handleMedicationsTextChange(
                            item,
                            "since",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Severity"
                        value={medicationsSpecs[item?.label]?.severity || ""}
                        onChange={(e) =>
                          handleMedicationsTextChange(
                            item,
                            "severity",
                            e.target.value
                          )
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Notes"
                        value={medicationsSpecs[item?.label]?.notes || ""}
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
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Since"
                        value={labInvestigationSpecs[item?.label]?.since || ""}
                        onChange={(e) =>
                          handleLabTextChange(item, "since", e.target.value)
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
                    <TextBoxLayout>
                      <RecordTextField
                        placeholder="Severity"
                        value={
                          labInvestigationSpecs[item?.label]?.severity || ""
                        }
                        onChange={(e) =>
                          handleLabTextChange(item, "severity", e.target.value)
                        }
                        variant="outlined"
                      />
                    </TextBoxLayout>
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
                    <DeleteWrapper>
                      <DeleteField onClick={handleLabSpecsDelete(item?.label)}>
                        Delete
                      </DeleteField>
                    </DeleteWrapper>
                  </FieldSpecsContainer>
                ))}
              </div>
            )}
          </VitalsContainer>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
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
            <Grid item xs={12} sm={6}>
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
          <EMRFooter>
            <SecondaryButton onClick={resetEMRForm}>Clear</SecondaryButton>
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
          <div style={{ height: "800px", marginBottom: "32px", flex: "1" }}>
            <PDFViewer style={{ width: "100%", height: "100%" }} zoom={1}>
              <PMRPdf pdfData={submitEMRPayload} patientData={patientData} />
            </PDFViewer>
          </div>
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
