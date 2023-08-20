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
import { useState } from "react";
import { useDispatch } from "react-redux";
import { getEMRId, postEMR, searchVitalsDetails } from "./EMRPage.slice";
import CustomAutoComplete from "../../../components/CustomAutoComplete";
import { Button } from "@mui/base";
import { PDFViewer } from "@react-pdf/renderer";
import PMRPdf from "../../../components/PMRPdf";

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
    marginTop: theme.spacing(8),
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

const VitalsCardTitle = styled("Typography")(({ theme }) => ({
  "&": {},
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
    alignItems: "center",
    gap: theme.spacing(6),
    marginTop: theme.spacing(6),
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
  const [emrId, setEMRId] = useState();
  const [pmrFinished, setPmrFinished] = useState(false);
  const [pdfData, setPdfData] = useState({});
  const [submitEMRPayload, setSubmitEMRPayload] = useState({});

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
    if (currentPatient && Object.keys(currentPatient)?.length) {
      console.log(currentPatient, "patientData");
      const emrPayload = {
        patient_id: currentPatient?.patientId,
        doc_id: currentPatient?.doc_id,
        appointment_id: currentPatient?.id,
        hip_id: currentPatient?.hip_id,
      };
      dispatch(getEMRId(emrPayload)).then((res) => {
        setEMRId(res.payload.pmr_id);
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
      setExamFinding([...symptoms, fieldValue]);
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
        duration: objectDetails.since,
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
        frequency: "3",
        dosage: "3",
        time_of_day: "morning",
        duration: objectDetails.since,
        duration_period: "",
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
        frequency: "",
        dosage: "",
        time_of_day: "",
        duration_period: "2 days",
        duration: objectDetails.since,
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
        diabetes_melitus: "",
        hypertension: "",
        hypothyroidism: "",
        alcohol: "",
        tobacco: "",
        smoke: "",
        snowmed_code: objectDetails?.snowmed_code,
        snowmed_display: objectDetails?.snowmed_display,
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
    if (valueArr?.length) {
      const payloadData = {
        pmr_id: emrId,
        data: valueArr,
      };
      payload[key] = payloadData;
    }
    setSubmitEMRPayload(payload);
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

    // console.log(formValues, "formValues");
    const payloadArr = [
      {
        key: "vital",
        dataArr: [
          {
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
        ],
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
    setPdfData(submitEMRPayload);
    // setPmrFinished(true);
    console.log(symptomsEMR);
    if (Object.keys(submitEMRPayload)?.length) {
      const filteredPayload = submitEMRPayload;
      filteredPayload["pmr_id"] = emrId;
      dispatch(postEMR(submitEMRPayload)).then((res) => {
        console.log(res.payload, "submitted");
      });
    }
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
  };

  // console.log(pdfData, "pdfData")

  return (
    <PatientEMRWrapper>
      <PatientDetailsHeader />
      <EMRFormWrapper>
        <VitalsContainer>
          <Typography>Vitals</Typography>
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
          <VitalsCardTitle>Patient Medical History</VitalsCardTitle>
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
                  <Typography>{item?.label}</Typography>
                  <TextField
                    placeholder="Since"
                    value={optionTextValues[item?.label]?.since || ""}
                    onChange={(e) =>
                      handleTextFieldChange(item, "since", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
                    placeholder="Severity"
                    value={optionTextValues[item?.label]?.severity || ""}
                    onChange={(e) =>
                      handleTextFieldChange(item, "severity", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
                    placeholder="Notes"
                    value={optionTextValues[item?.label]?.notes || ""}
                    onChange={(e) =>
                      handleTextFieldChange(item, "notes", e.target.value)
                    }
                    variant="outlined"
                  />
                  <Button onClick={handleOptionRemove(item?.label)}>
                    Delete
                  </Button>
                </FieldSpecsContainer>
              ))}
            </div>
          )}
        </VitalsContainer>
        <VitalsContainer>
          <VitalsCardTitle>Existing Conditions</VitalsCardTitle>
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
                  <Typography>{item?.label}</Typography>
                  <TextField
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
                  <TextField
                    placeholder="Severity"
                    value={existingConditionSpecs[item?.label]?.severity || ""}
                    onChange={(e) =>
                      exisitingConditionsTextChange(
                        item,
                        "severity",
                        e.target.value
                      )
                    }
                    variant="outlined"
                  />
                  <TextField
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
                  <Button
                    onClick={handleExistingConditionsSpecDelete(item?.label)}
                  >
                    Delete
                  </Button>
                </FieldSpecsContainer>
              ))}
            </div>
          )}
        </VitalsContainer>
        <VitalsContainer>
          <VitalsCardTitle> Symptoms</VitalsCardTitle>
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
                  <Typography>{item?.label}</Typography>
                  <TextField
                    placeholder="Since"
                    value={symptomsSpecs[item?.label]?.since || ""}
                    onChange={(e) =>
                      handleSymtomsTextChange(item, "since", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
                    placeholder="Severity"
                    value={symptomsSpecs[item?.label]?.severity || ""}
                    onChange={(e) =>
                      handleSymtomsTextChange(item, "severity", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
                    placeholder="Notes"
                    value={symptomsSpecs[item?.label]?.notes || ""}
                    onChange={(e) =>
                      handleSymtomsTextChange(item, "notes", e.target.value)
                    }
                    variant="outlined"
                  />
                  <Button onClick={handleSymptomsSpecsDelete(item?.label)}>
                    Delete
                  </Button>
                </FieldSpecsContainer>
              ))}
            </div>
          )}
        </VitalsContainer>
        <VitalsContainer>
          <VitalsCardTitle>Examination Findings</VitalsCardTitle>
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
                  <Typography>{item?.label}</Typography>
                  <TextField
                    placeholder="Since"
                    value={examinationSpecs[item?.label]?.since || ""}
                    onChange={(e) =>
                      handleExaminationTextChange(item, "since", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
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
                  <TextField
                    placeholder="Notes"
                    value={examinationSpecs[item?.label]?.notes || ""}
                    onChange={(e) =>
                      handleExaminationTextChange(item, "notes", e.target.value)
                    }
                    variant="outlined"
                  />
                  <Button onClick={handleExaminationSpecsDelete(item?.label)}>
                    Delete
                  </Button>
                </FieldSpecsContainer>
              ))}
            </div>
          )}
        </VitalsContainer>
        <VitalsContainer>
          <VitalsCardTitle>Diagnosis</VitalsCardTitle>
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
                  <Typography>{item?.label}</Typography>
                  <TextField
                    placeholder="Since"
                    value={diagnosisSpecs[item?.label]?.since || ""}
                    onChange={(e) =>
                      handleDiagnosisTextChange(item, "since", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
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
                  <TextField
                    placeholder="Notes"
                    value={diagnosisSpecs[item?.label]?.notes || ""}
                    onChange={(e) =>
                      handleDiagnosisTextChange(item, "notes", e.target.value)
                    }
                    variant="outlined"
                  />
                  <Button onClick={handleDiagnosisSpecsDelete(item?.label)}>
                    Delete
                  </Button>
                </FieldSpecsContainer>
              ))}
            </div>
          )}
        </VitalsContainer>
        <VitalsContainer>
          <VitalsCardTitle>Medications</VitalsCardTitle>
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
                  <Typography>{item?.label}</Typography>
                  <TextField
                    placeholder="Since"
                    value={medicationsSpecs[item?.label]?.since || ""}
                    onChange={(e) =>
                      handleMedicationsTextChange(item, "since", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
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
                  <TextField
                    placeholder="Notes"
                    value={medicationsSpecs[item?.label]?.notes || ""}
                    onChange={(e) =>
                      handleMedicationsTextChange(item, "notes", e.target.value)
                    }
                    variant="outlined"
                  />
                  <Button onClick={handleMedicationsSpecsDelete(item?.label)}>
                    Delete
                  </Button>
                </FieldSpecsContainer>
              ))}
            </div>
          )}
        </VitalsContainer>
        <VitalsContainer>
          <VitalsCardTitle>Lab Investigations</VitalsCardTitle>
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
                  <Typography>{item?.label}</Typography>
                  <TextField
                    placeholder="Since"
                    value={labInvestigationSpecs[item?.label]?.since || ""}
                    onChange={(e) =>
                      handleLabTextChange(item, "since", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
                    placeholder="Severity"
                    value={labInvestigationSpecs[item?.label]?.severity || ""}
                    onChange={(e) =>
                      handleLabTextChange(item, "severity", e.target.value)
                    }
                    variant="outlined"
                  />
                  <TextField
                    placeholder="Notes"
                    value={labInvestigationSpecs[item?.label]?.notes || ""}
                    onChange={(e) =>
                      handleLabTextChange(item, "notes", e.target.value)
                    }
                    variant="outlined"
                  />
                  <Button onClick={handleLabSpecsDelete(item?.label)}>
                    Delete
                  </Button>
                </FieldSpecsContainer>
              ))}
            </div>
          )}
        </VitalsContainer>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <VitalsContainer>
              <VitalsCardTitle>Notes</VitalsCardTitle>
              <div>
                <TextField
                  placeholder="Add your notes here"
                  className="notes-field"
                  onChange={prescriptionCommentChange}
                />
              </div>
            </VitalsContainer>
          </Grid>
          <Grid item xs={12} sm={6}>
            <VitalsContainer>
              <VitalsCardTitle>Advices</VitalsCardTitle>
              <div>
                <TextField
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
          <PrimaryButton onClick={submitEMR}>Finish Prescription</PrimaryButton>
        </EMRFooter>
      </EMRFormWrapper>

      {pmrFinished && (
        <div style={{ height: "800px" }}>
          <PDFViewer style={{ width: "100%", height: "100%" }} zoom={1}>
            <PMRPdf pdfData={pdfData} />
          </PDFViewer>
        </div>
      )}
    </PatientEMRWrapper>
  );
};

export default PatientEMRDetails;
