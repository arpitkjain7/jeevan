import * as React from "react";
import { useState } from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import CloseIcon from "@mui/icons-material/Close";
import Slide from "@mui/material/Slide";
import AspectRatioIcon from "@mui/icons-material/AspectRatio";
import AllergyIcon from "@mui/icons-material/HealthAndSafety";
import AssessmentIcon from "@mui/icons-material/Assignment";
import PlanIcon from "@mui/icons-material/FactCheck";
import PrescriptionIcon from "@mui/icons-material/Description";
import TestIcon from "@mui/icons-material/Biotech";
import MonitorHeartIcon from "@mui/icons-material/MonitorHeart";
import NextStepsIcon from "@mui/icons-material/Forward";
import NotesIcon from "@mui/icons-material/Notes";
import { Document, Page } from "react-pdf";
import { pdfjs } from "react-pdf";
import AddCircleRoundedIcon from '@mui/icons-material/AddCircleRounded';
import {
  Autocomplete,
  Box,
  Chip,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  Grid,
  InputBase,
  InputLabel,
  ListItem,
  Modal,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  TextareaAutosize,
  Tooltip,
  createTheme,
  InputAdornment,
} from "@mui/material";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { alpha, styled } from "@mui/material/styles";
import contentData from "../../components/RecorderComponent/content.json";
import Translate from "../Translate";
import { ThemeProvider } from "@emotion/react";
import { useDispatch } from "react-redux";
import {
  postEMR,
  previewPMRSummary,
  searchVitalsDetails,
  updatePMRSummary,
} from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import PdfFromDocumentBytes from "../PdfFromDocumentBytes";
import SendPMR from "../../pages/DoctorPage/SendPMR";
import CustomLoader from "../CustomLoader";
import CustomizedDialogs from "../Dialog";
import { format } from "date-fns";
import Calendar from "../Calendar";
import { Delete, Assignment } from "@mui/icons-material";
import CustomAutoComplete from "../CustomAutoComplete";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const isMobile = window.innerWidth < 600;

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 320,
  bgcolor: "background.paper",
  border: "1px solid #000",
  boxShadow: 24,
  padding: "0 16px 16px",
};

const PDFViewerWrapper = styled("div")(({ theme }) => ({
  height: isMobile ? "auto" : "800px",
  marginBottom: isMobile ? "0" : "32px",
  flex: "1",
}));

const PDFButtonWrapper = styled(Box)(({ theme }) => ({
  display: "flex",
  justifyContent: "center",
  gap: "16px",
  position: "sticky",
  bottom: 0,
  border: "1px solid #0089E9",
  backgroundColor: "#b2d6f0",
  padding: theme.spacing(2, 2),
  zIndex: 1,
}));

const PrimaryButton = styled(Button)(({ theme }) => ({
  "&": theme.typography.primaryButton,
  float: "right",
  [theme.breakpoints.down("sm")]: {
    padding: "5px 7px",
  },
}));
const CustomStyle = {
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

const theme = createTheme({
  components: {
    MuiOutlinedInput: {
      styleOverrides: {
        input: {
          "&.Mui-disabled": {
            WebkitTextFillColor: "black",
          },
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        input: {
          "&.Mui-disabled": {
            WebkitTextFillColor: "black",
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          "&.Mui-disabled": {
            opacity: 1,
          },
        },
      },
    },
  },
});

const BootstrapInput = styled(InputBase)(({ theme }) => ({
  "label + &": {
    marginTop: theme.spacing(4),
    marginBottom: theme.spacing(2),
  },
  "& .MuiInputBase-input": {
    borderRadius: 4,
    position: "relative",
    backgroundColor: theme.palette.mode === "light" ? "#F3F6F9" : "#1A2027",
    border: "1px solid",
    borderColor: theme.palette.mode === "light" ? "#E0E3E7" : "#2D3843",
    fontSize: 16,
    padding: "10px 12px",
    transition: theme.transitions.create([
      "border-color",
      "background-color",
      "box-shadow",
    ]),
    fontFamily: [
      "-apple-system",
      "BlinkMacSystemFont",
      '"Segoe UI"',
      "Roboto",
      '"Helvetica Neue"',
      "Arial",
      "sans-serif",
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(","),
    "&:focus": {
      boxShadow: `${alpha(theme.palette.primary.main, 0.25)} 0 0 0 0.2rem`,
      borderColor: theme.palette.primary.main,
    },
  },
}));

const FieldSpecsContainer = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    // marginTop: theme.spacing(4),
    margin: "20px 0",
    justifyContent: "space-between",
    gap: "20px",
    [theme.breakpoints.down("sm")]: {
      gap: theme.spacing(2),
      padding: "10px 5px",
      alignItems: "center",
      border: "1px solid #ccccccb8",
      flexWrap: "wrap",
    },
  },
}));

const RecordLayout = styled("div")(({ theme }) => ({
  textAlign: "left",
  width: "120px",
  // padding: "20px 5px",
  // margin: "10px 0",
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

const SelectedRecord = styled(Typography)(({ theme }) => ({
  "&": theme.typography.body1,
  marginBottom: theme.spacing(1),
  // marginBottom: "0",
  width: "120px",
  [theme.breakpoints.down("sm")]: {
    marginBottom: "0",
  },
}));

const VitalsContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    // marginTop: theme.spacing(4),
    // padding: theme.spacing(6),
    borderRadius: theme.spacing(1),
    // [theme.breakpoints.down("sm")]: {
    //   padding: theme.spacing(4, 2),
    // },
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

const TextBoxLayout = styled("div")(({ theme }) => ({
  flex: 1,
  width: "120px",
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

const NotesField = styled(Assignment)(({ theme }) => ({
  height: "30px",
  width: "30px",
}));

const DeleteField = styled(Delete)(({ theme }) => ({
  height: "30px",
  width: "30px",
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

  React.useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  return windowDimensions;
}

export default function CustomizedSummaryDialog({
  open,
  setOpen,
  summaryContent,
  setSummaryContent,
  emrData,
}) {
  const [showLoader, setShowLoader] = useState(false);
  const [translatedContent, setTranslatedContent] = useState(summaryContent);
  const [changeLanguage, setChangeLanguage] = useState(false);
  const [edit, setEdit] = useState(false);
  const [data, setData] = useState("");
  const [openPdf, setOpenPdf] = useState(false);
  const [pmrDialogOpen, setPmrDialogOpen] = useState(false);
  const [numPages, setNumPages] = useState(null);
  const selectedPatient = JSON.parse(sessionStorage.getItem("selectedPatient"));
  const PageSelected = sessionStorage.getItem("PageSelected");
  const [openCalendar, setOpenCalendar] = useState(false);
  const [selectedDate, setSelectedDate] = useState("");
  const [openFollowUp, setOpenFollowUp] = useState(false);
  const handleFollowUpClose = () => setOpenFollowUp(false);
  const selectedHospital = JSON.parse(
    sessionStorage.getItem("selectedHospital")
  );
  const encounterDetail = JSON.parse(sessionStorage.getItem("encounterDetail"));
  const dispatch = useDispatch();

  //begins Vitals medication section
  const [medications, setMedications] = useState([]);
  const [medicationsSpecs, setMedicationsSpecs] = useState({});
  const [medicationsOpts, setMedicationsOpts] = useState([]);
  const [number, setNumber] = useState("");
  const [dosages, setDosages] = useState("");
  const [medicationOptions, setMedicationOptions] = useState("");
  const [openMedicationNotes, setOpenMedicationNotes] = React.useState(false);
  const handleCloseMedicationNotes = () => setOpenMedicationNotes(false);
  const handleOpenMedicationNotes = () => setOpenMedicationNotes(true);
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

  React.useEffect(() => {
    if (summaryContent[7]?.[1]?.medications.length > 0) {
      summaryContent[7][1]?.medications?.map((medication) => {
        setMedications((medications) => [
          ...medications,
          {
            label: medication.med_name,
            value: medication.med_name,
            // snowmed_code: "",
            // snowmed_display: "",
          },
        ]);
        setMedicationsSpecs((prevState) => ({
          ...prevState,
          [medication.med_name]: {
            frequency: medication?.frequency,
            dosages: medication?.dosages,
            duration: medication?.duration,
            instructions: medication?.instructions,
            time_of_day: medication?.time_of_day,
          },
        }));
      });
    }
  }, [summaryContent]);

  // const addMedicationsToSummary = () => {
  //   setSummaryContent((prevContent) => {
  //     // Create a shallow copy of the previous state
  //     const updatedContent = [...prevContent];

  //     // Ensure the nested structure is properly initialized
  //     if (!updatedContent[7]) {
  //       updatedContent[7] = [];
  //     }
  //     if (!updatedContent[7][1]) {
  //       updatedContent[7][1] = { medications: [] };
  //     } else if (!Array.isArray(updatedContent[7][1].medications)) {
  //       updatedContent[7][1].medications = [];
  //     }

  //     // Create a deep copy of the medications array
  //     const medicationsArray = Object.keys(medicationsSpecs).map((medName) => {
  //       const spec = medicationsSpecs[medName];
  //       return {
  //         med_name: medName,
  //         frequency: spec.severity,
  //         dosages: spec.dose,
  //         duration: spec.since,
  //         instructions: spec.notes,
  //         time_of_day: spec.timing,
  //       };
  //     });

  //     // Combine the existing medications with the new ones
  //     updatedContent[7][1] = {
  //       ...updatedContent[7][1],
  //       medications: [...updatedContent[7][1].medications, ...medicationsArray],
  //     };

  //     return updatedContent;
  //   });
  // };

  React.useEffect(() => {
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
        if (resData?.length > 0) {
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
  }, [medicationOptions]);

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
      console.log(objectDetails);
      const transformedItem = {
        med_name: key,
        frequency: objectDetails.frequency,
        dosages: objectDetails.dosages,
        time_of_day: objectDetails.time_of_day,
        duration: objectDetails.duration,
        instructions: objectDetails.instructions,
        // snowmed_code: objectDetails?.snowmed_code,
        // snowmed_display: objectDetails?.snowmed_display,
      };

      result.push(transformedItem);
    }

    const filteredResult = result.filter(
      (item) => item.medicine_name !== "[object Object]"
    );
    return filteredResult;
  };

  const handleMedicationsTextChange = (option, textField, newValue) => {
    let inputValue;
    if (textField === "frequency") {
      const durationValue = newValue.trim().replace(/[^0-9]/g, "");
      if (durationValue.length < 3) {
        inputValue = durationValue.replace(/(\d{1})(\d{1})/, "$1-$2");
      } else if (durationValue.length < 6) {
        inputValue = durationValue.replace(/(\d{1})(\d{1})(\d{1})/, "$1-$2-$3");
      } else inputValue = "";
    } else inputValue = newValue;
    setMedicationsSpecs({
      ...medicationsSpecs,
      [option?.label]: {
        ...medicationsSpecs[option?.label],
        [textField]: inputValue,
        // snowmed_code: option?.snowmed_code,
        // snowmed_display: option?.snowmed_display,
      },
    });
  };

  const generateDoseOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);

    if (isNaN(parsedNumber) || !item) {
      return [];
    }

    const sinceValue = medicationsSpecs[item]?.dosages || "";

    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return doseOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }

    return [];
  };

  const handleMedicationOptionsChange = (option, newValue, key) => {
    handleMedicationsTextChange(option, key, newValue);
  };

  const generateOptions = (number, item) => {
    const parsedNumber = parseInt(number, 10);
    if (isNaN(parsedNumber) || !item) {
      return [];
    }
    const sinceValue = medicationsSpecs[item]?.duration;
    if (sinceValue === "" || !isNaN(parsedNumber)) {
      return timeOptions?.map((option) => `${parsedNumber}${option}`) || [];
    }
    return [];
  };

  const handleDoseOptions = (event, value) => {
    const isValidInput = /^([1-9]\d{0,2}(Tablet)?)?$/.test(value);
    if (isValidInput) {
      setDosages(value);
    }
  };

  const handleNumberOptions = (event, value) => {
    const isValidInput = /^([1-9]\d{0,2}(Days|Weeks|Months)?)?$/.test(value);
    if (isValidInput) {
      setNumber(value);
    }
  };

  const handleAddNewMedication = () => {
    const updatedContent = summaryContent;
    console.log(medicationsSpecs);
    console.log(updatedContent);
    updatedContent[7][1] = {
      ...updatedContent[7][1],
      medications: medicationsSpecs,
    };
    console.log(updatedContent);
  }

  const handleMedicationsSpecsDelete = (optionToRemove) => () => {
    setMedications(
      medications.filter((option) => option?.label !== optionToRemove)
    );
    setMedicationsSpecs((prevState) => {
      const { [optionToRemove]: _, ...restOptionTextValues } = prevState;
      return restOptionTextValues;
    });
  };

  const handleMedicationsChange = async (event) => {
    setTimeout(() => {
      setMedicationOptions(event.target.value);
    }, 1000);
  };

  const handleMedications = (event, value) => {
    if (value) {
      const fieldValue = value;
      setMedicationsSpecs({
        ...medicationsSpecs,
        [value?.label || value]: { duration: "", frequency: "", instructions: "" },
      });

      if (value?.label) {
        setMedications([...medications, fieldValue]);
      } else {
        setMedications((medications) => [
          ...medications,
          {
            label: fieldValue,
            value: fieldValue,
            snowmed_code: "",
            snowmed_display: "",
          },
        ]);
      }
      setMedicationsOpts([]);
    }
  };

  const handleUpdateMedications = () => {
    const medicationEMR = medicationObj(medicationsSpecs);
    const updatedContent = summaryContent;
    console.log(updatedContent);
    updatedContent[7][1] = {
      ...updatedContent[7][1],
      medications: medicationEMR,
    };
    console.log(medicationEMR);
    console.log(updatedContent);
    setSummaryContent(updatedContent);
  }

  const clearMedicationOptions = (event) => {
    setMedicationsOpts([]);
  };

  //ENds Vitals medication section

  let content = !changeLanguage ? summaryContent : translatedContent;
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => setOpen(false);
  const [newMedication, setNewMedication] = useState({
    med_name: "",
    frequency: "",
    dosages: "",
    duration: "",
    instructions: "",
    time_of_day: "",
  });

  const postPMR = async () => {
    setShowLoader(true);
    let pmr_request;
    pmr_request = {
      pmr_id: sessionStorage.getItem("pmrID"),
    };
    let appointment_request;
    if (selectedDate) {
      appointment_request = {
        appointment_id:
          PageSelected === "1"
            ? encounterDetail?.id || selectedPatient?.id
            : selectedPatient?.id || encounterDetail?.id,
        followup_date: selectedDate, //convertDateFormat(followUp, "yyyy-MM-dd"),
        consultation_status: "Completed",
      };
    } else {
      appointment_request = {
        appointment_id:
          PageSelected === "1"
            ? encounterDetail?.id || selectedPatient?.id
            : selectedPatient?.id || encounterDetail?.id,
        consultation_status: "Completed",
      };
    }
    const allData = {
      pmr_request,
      appointment_request,
    };

    dispatch(postEMR(allData))
      .then((res) => {
        setShowLoader(false);
        if (res?.meta?.requestStatus === "rejected") {
          setPmrDialogOpen(true);
        } else {
          setNotifyModal(true);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
  };

  React.useEffect(() => {
    if (translatedContent && translatedContent.length > 0) {
    }
  }, [translatedContent]);

  const handleSummaryChange = (event, index) => {
    const { name, value } = event.target;
    setSummaryContent((prevContent) => {
      let newContent = [...prevContent];
      if (newContent[index] && newContent[index][1]) {
        newContent[index][1] = { ...newContent[index][1], [name]: value };
      }
      console.log(newContent);
      return newContent;
    });
  };

  const handleVitalsChange = (event, index) => {
    const { name, value } = event.target;
    console.log(name, value);
    setSummaryContent((prevContent) => {
      let newContent = [...prevContent];
      if (
        newContent[index] &&
        newContent[index][1] &&
        newContent[index][1].vital_signs
      ) {
        newContent[index][1] = {
          ...newContent[index][1],
          vital_signs: {
            ...newContent[index][1].vital_signs,
            [name]: value,
          },
        };
      }
      console.log(newContent);
      return newContent;
    });
  };
  const handleChipChange = (e, index, newValue, sectionName) => {
    console.log(sectionName);
    setSummaryContent((prevContent) => {
      // Create a deep copy of the previous content
      const newContent = prevContent.map((item, idx) => {
        if (idx === index && item[1]) {
          return [
            ...item.slice(0, 1),
            {
              ...item[1],
              [sectionName]: newValue,
            },
          ];
        }
        return item;
      });
      console.log(newContent);
      return newContent;
    });
  };

  const handleMedicationInputChange = (e, field) => {
    setNewMedication({ ...newMedication, [field]: e.target.value });
  };

  const handleDeleteMedication = (medNameToDelete) => {
    setSummaryContent((prevContent) => {
      const updatedContent = [...prevContent];
      console.log(updatedContent);
      const medicationsIndex = 7;
      const medicationList =
        updatedContent[medicationsIndex][1]?.medications || [];
      const filteredMedications = medicationList.filter(
        (medication) => medication.med_name !== medNameToDelete
      );
      console.log(updatedContent);
      updatedContent[medicationsIndex][1].medications = filteredMedications;
      return updatedContent;
    });
  };

  // const handleAddMedication = () => {
  //   if (
  //     newMedication.med_name &&
  //     newMedication.frequency 
  //     // &&
  //     // newMedication.time_of_day &&
  //     // newMedication.instructions &&
  //     // newMedication.dosages &&
  //     // newMedication.duration
  //   ) {
  //     // Create a new medication object from the input fields
  //     const medicationToAdd = { ...newMedication };
  //     console.log(medicationToAdd);

  //     setMedications((medications) => [
  //       ...medications,
  //       {
  //         label: medicationToAdd.med_name,
  //         value: medicationToAdd.med_name,
  //         snowmed_code: "",
  //         snowmed_display: "",
  //       },
  //     ]);
  //     setMedicationsSpecs((prevState) => ({
  //       ...prevState,
  //       [medicationToAdd.med_name]: {
  //         severity: medicationToAdd?.frequency,
  //         timing: medicationToAdd?.time_of_day,
  //         dose: medicationToAdd?.dosages,
  //         since: medicationToAdd?.duration,
  //         notes: medicationToAdd?.instructions,
  //       },
  //     }));

  //     // Update the summaryContent state with the new medication
  //     console.log(medicationsSpecs);
  //       const updatedContent = summaryContent;
  //       console.log(updatedContent);
  //       updatedContent[7][1] = {
  //         ...updatedContent[7][1],
  //         medications: [medicationsSpecs],
  //       };
  //       // updatedContent[7][1]?.medications = medicationsSpecs;
       
  //       // if (!finalMedications) {
  //       //   updatedContent[7][1].medications(medicationToAdd);
  //       // }
  //       // else {
  //       //   // Add the new medication to the medications array
  //       //   updatedContent[7][1].medications.push(medicationToAdd);
  //       // }
        
  //       console.log(updatedContent);
  //       // Return the updated state
  //       // return updatedContent;
  //       setSummaryContent(updatedContent);

  //     // Reset the newMedication input fields
  //     // setNewMedication({
  //     //   med_name: "",
  //     //   frequency: "",
  //     //   dosages: "",
  //     //   duration: "",
  //     //   instructions: "",
  //     //   time_of_day: "",
  //     // });
  //   } else {
  //     // Optionally handle the case where some fields are empty
  //     console.log("Please fill in all fields.");
  //   }
  // };

  const { width } = useWindowDimensions();
  const [notifyModal, setNotifyModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editingMedName, setEditingMedName] = useState("");
  const [documentID, setDocumentID] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);

  const startEditMedication = (medication) => {
    setIsEditing(true);
    setEditingMedName(medication.med_name);
    setNewMedication(medication);

  };

  const saveEditedMedication = () => {
    setSummaryContent((prevContent) => {
      const updatedContent = [...prevContent];
      const medicationsIndex = 7; // Assuming the medications are at index 7
      const medicationList =
        updatedContent[medicationsIndex][1]?.medications || [];

      // Find and update the medication
      const medicationIndex = medicationList.findIndex(
        (medication) => medication.med_name === editingMedName
      );
      if (medicationIndex !== -1) {
        updatedContent[medicationsIndex][1].medications[medicationIndex] = {
          ...newMedication,
        };
      }

      return updatedContent;
    });

    // Reset states
    setIsEditing(false);
    setEditingMedName("");
    setNewMedication({
      med_name: "",
      frequency: "",
      dosages: "",
      duration: "",
      instructions: "",
      time_of_day: "",
    });
  };

  //Changing the Summary
  const handleSavechanges = () => {
    const payload = {
      pmr_id: sessionStorage.getItem("pmrID"),
      ...Object.fromEntries(summaryContent),
    };
    dispatch(updatePMRSummary(payload)).then((res) => {
      if (res?.payload) {
        console.log(res?.payload);
        setEdit(!edit);
      }
    });
  };

  //Handling Preview Summary
  const handleReviewPrescription = () => {
    const payload = {
      pmr_metadata: {
        doctor_name: selectedPatient?.doc_name || encounterDetail?.doc_name,
        patient_name:
          selectedPatient?.name ||
          selectedPatient?.p_name ||
          encounterDetail?.p_name,
        hospital_name: selectedHospital?.name,
        patient_uid:
          selectedPatient?.patient_uid ||
          selectedPatient?.patientUid ||
          encounterDetail?.patient_uid,
        patient_gender:
          encounterDetail?.gender ||
          selectedPatient?.patient_details?.gender ||
          "NA",
        // document_id: selectedPatient?.doc_id || null,
        patient_age_years:
          selectedPatient?.age_in_years || encounterDetail?.age_in_years,
        patient_age_months: selectedPatient?.age_in_months,
        patient_contact_number:
          selectedPatient?.mobile_number ||
          selectedPatient?.mobileNumber ||
          encounterDetail?.mobile_number,
        patient_email: encounterDetail?.email || selectedPatient?.email || "NA",
      },
      pmr_request: {
        pmr_id: sessionStorage.getItem("pmrID"),
      },
      appointment_request: {
        appointment_id:
          emrData?.id || encounterDetail?.id || selectedPatient?.id,
        followup_date: selectedDate || selectedPatient?.followup_date,
        consultation_status: selectedPatient?.consultation_status,
      },
    };
    console.log(payload);
    console.log("selectedPatient", selectedPatient);
    dispatch(previewPMRSummary(payload)).then((response) => {
      if (response?.payload) {
        setDocumentID(response?.payload?.document_id);
        setData(response?.payload?.data);
        setOpenPdf(true);
        // setDocumentBytes(response?.payload?.data);
        pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;
        if (response?.payload?.data) {
          const decodedByteCode = atob(response?.payload?.data);
          const byteNumbers = new Array(decodedByteCode.length);
          for (let i = 0; i < decodedByteCode.length; i++) {
            byteNumbers[i] = decodedByteCode.charCodeAt(i);
          }
          const blobData = new Blob([new Uint8Array(byteNumbers)], {
            type: "application/pdf",
          });
          // const pdfUrls = URL.createObjectURL(blobData);
          setPdfUrl(URL.createObjectURL(blobData));
          return () => {
            URL.revokeObjectURL(pdfUrl);
          };
        } else return;
      }
    });
  };

  const handleFollowUpDateChange = (event) => {
    console.log(event.target.value);
    setSelectedDate(event.target.value);
  };

  const handleFollowUp = () => {
    setOpenFollowUp(true);
  };

  return (
    <React.Fragment>
      <CustomLoader open={showLoader} />
      <CustomizedDialogs
        open={pmrDialogOpen}
        handleClose={() => setPmrDialogOpen(false)}
      />
      <ThemeProvider theme={theme}>
        <Tooltip title="See More">
          <IconButton
            variant="text"
            onClick={handleClickOpen}
            sx={{ backgroundColor: "#89f2ff61" }}
          >
            <AspectRatioIcon sx={{ color: "#1976d2" }} />
          </IconButton>
        </Tooltip>
        <Dialog
          fullScreen
          open={open}
          onClose={handleClose}
          TransitionComponent={Transition}
        >
          <AppBar sx={{ position: "relative", backgroundColor: "#f8f8f8" }}>
            <Toolbar>
              <DialogTitle
                sx={{ m: 0, p: 2, display: "flex", flex: 1 }}
                id="customized-dialog-title"
              >
                <Stack
                  justifyContent={"center"}
                  alignItems={"center"}
                  sx={{
                    backgroundColor: "#0089E9",
                    width: "130px",
                    padding: "5px",
                  }}
                >
                  <Typography
                    sx={{ fontSize: "1rem", fontWeight: 500, color: "white" }}
                    variant="h2"
                  >
                    CLINICAL NOTE
                  </Typography>
                </Stack>
                <Stack ml={5} justifyContent={"center"} alignItems={"center"}>
                  <Typography color={"#0089E9"}>
                    PATIENT VISIT SUMMARY
                  </Typography>
                </Stack>
              </DialogTitle>
              {/* <Stack direction={"row"} gap={2}>
                <Translate
                  translatedContent={translatedContent}
                  setTranslatedContent={setTranslatedContent}
                  setOpen={setOpen}
                />
               
              </Stack> */}
              <IconButton
                edge="start"
                color="inherit"
                onClick={handleClose}
                aria-label="close"
              >
                <CloseIcon sx={{ color: "#0089E9" }} />
              </IconButton>
            </Toolbar>
          </AppBar>
          <DialogContent dividers>
            <FormControl variant="standard" fullWidth>
              <TextField
                disabled={!edit}
                label="Consultaion Summary"
                variant="outlined"
                defaultValue={content?.[0]?.[1]?.summary}
                id="bootstrap-input"
                name="summary"
                multiline
                onChange={(e) => handleSummaryChange(e, 0)}
              />
            </FormControl>

            <Typography gutterBottom></Typography>
            <Accordion>
              <AccordionSummary
                alignItems={"center"}
                expandIcon={<ExpandMoreIcon />}
              >
                <AllergyIcon sx={{ marginRight: "5px" }} />
                <Typography variant="h6" textAlign={"center"}>
                  <strong>Subjective</strong>
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong> Chief Complaint: </strong>
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[1][1]?.chief_complaint || "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="chief_complaint"
                    onChange={(e) => handleSummaryChange(e, 1)}
                  />
                </FormControl>
                <>
                  <div>
                    <Typography gutterBottom>Allergy Information:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="allergy_information"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 1, newValue, "allergy_information")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[1][1]?.allergy_information || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Allergies"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                1,
                                [
                                  ...(content[1][1]?.allergy_information || []),
                                  value.trim(),
                                ],
                                "allergy_information"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  1,
                                  [
                                    ...(content[1][1]?.allergy_information ||
                                      []),
                                    value.trim(),
                                  ],
                                  "allergy_information"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>

                  <div>
                    <Typography gutterBottom>Family History:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="family_history"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 1, newValue, "family_history")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[1][1]?.family_history || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Family History"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                1,
                                [
                                  ...(content[1][1]?.family_history || []),
                                  value.trim(),
                                ],
                                "family_history"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  1,
                                  [
                                    ...(content[1][1]?.family_history || []),
                                    value.trim(),
                                  ],
                                  "family_history"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>

                  <div>
                    <Typography gutterBottom>
                      History of Present Illness:
                    </Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="history_of_present_illness"
                      onChange={(e, newValue) =>
                        handleChipChange(
                          e,
                          1,
                          newValue,
                          "history_of_present_illness"
                        )
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[1][1]?.history_of_present_illness || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="History of Illness"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                1,
                                [
                                  ...(content[1][1]
                                    ?.history_of_present_illness || []),
                                  value.trim(),
                                ],
                                "history_of_present_illness"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  1,
                                  [
                                    ...(content[1][1]
                                      ?.history_of_present_illness || []),
                                    value.trim(),
                                  ],
                                  "history_of_present_illness"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>

                  <div>
                    <Typography gutterBottom>Medication History:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="medication_history"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 1, newValue, "medication_history")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[1][1]?.medication_history || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Medication History"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                1,
                                [
                                  ...(content[1][1]?.medication_history || []),
                                  value.trim(),
                                ],
                                "medication_history"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  1,
                                  [
                                    ...(content[1][1]?.medication_history ||
                                      []),
                                    value.trim(),
                                  ],
                                  "medication_history"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>

                  <div>
                    <Typography gutterBottom>Past Medical History:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="past_medical_history"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 1, newValue, "past_medical_history")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[1][1]?.past_medical_history || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Past Medical History"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                1,
                                [
                                  ...(content[1][1]?.past_medical_history ||
                                    []),
                                  value.trim(),
                                ],
                                "past_medical_history"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  1,
                                  [
                                    ...(content[1][1]?.past_medical_history ||
                                      []),
                                    value.trim(),
                                  ],
                                  "past_medical_history"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>

                  <div>
                    <Typography gutterBottom>Social History:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="social_history"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 1, newValue, "social_history")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[1][1]?.social_history || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Social History"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                1,
                                [
                                  ...(content[1][1]?.social_history || []),
                                  value.trim(),
                                ],
                                "social_history"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  1,
                                  [
                                    ...(content[1][1]?.social_history || []),
                                    value.trim(),
                                  ],
                                  "social_history"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>
                </>
              </AccordionDetails>
            </Accordion>
            <Accordion>
              <AccordionSummary
                alignItems={"center"}
                expandIcon={<ExpandMoreIcon />}
              >
                <MonitorHeartIcon sx={{ marginRight: "5px" }} />
                <Typography variant="h6">
                  <strong>Objective</strong>
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong> Laboratory and Diagnostic Test Result: </strong>
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[2][1]?.laboratory_and_diagnostic_test_results ||
                      "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="laboratory_and_diagnostic_test_results"
                    onChange={(e) => handleSummaryChange(e, 2)}
                  />
                </FormControl>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong>Examination Findings </strong>
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[2][1]?.physical_examination_findings ||
                      "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="physical_examination_findings"
                    onChange={(e) => handleSummaryChange(e, 2)}
                  />
                </FormControl>
                <Grid container gap={1} spacing={1}>
                  <Grid item md={2.5} sm={10} xs={12}>
                    <FormControl variant="standard" fullWidth>
                      <InputLabel shrink htmlFor="bootstrap-input">
                        <Typography variant="h6">
                          <strong> Blood Pressure </strong>
                        </Typography>
                      </InputLabel>

                      <BootstrapInput
                        disabled={!edit}
                        defaultValue={
                          content[2][1]?.vital_signs?.blood_pressure || 0
                        }
                        id="bootstrap-input"
                        multiline
                        name="blood_pressure"
                        onChange={(e) => handleVitalsChange(e, 2)}
                        endAdornment={
                          <InputAdornment position="end">mmHg</InputAdornment>
                        }
                      />
                    </FormControl>
                  </Grid>
                  <Grid item md={2.5} sm={5} xs={12}>
                    <FormControl variant="standard" fullWidth>
                      <InputLabel shrink htmlFor="bootstrap-input">
                        <Typography variant="h6">
                          <strong> Heart Rate: </strong>
                        </Typography>
                      </InputLabel>
                      <BootstrapInput
                        disabled={!edit}
                        defaultValue={
                          content[2][1]?.vital_signs?.heart_rate || 0
                        }
                        id="bootstrap-input"
                        multiline
                        name="heart_rate"
                        onChange={(e) => handleVitalsChange(e, 2)}
                        endAdornment={
                          <InputAdornment position="end">/min</InputAdornment>
                        }
                      />
                    </FormControl>
                  </Grid>
                  <Grid item md={2.5} sm={5} xs={12}>
                    <FormControl variant="standard" fullWidth>
                      <InputLabel shrink htmlFor="bootstrap-input">
                        <Typography variant="h6">
                          <strong> Oxygen Saturation : </strong>
                        </Typography>
                      </InputLabel>
                      <BootstrapInput
                        disabled={!edit}
                        defaultValue={
                          content[2][1]?.vital_signs?.oxygen_saturation || 0
                        }
                        id="bootstrap-input"
                        multiline
                        name="oxygen_saturation"
                        onChange={(e) => handleVitalsChange(e, 2)}
                        endAdornment={
                          <InputAdornment position="end">%</InputAdornment>
                        }
                      />
                    </FormControl>
                  </Grid>
                  <Grid item md={2.5} sm={5} xs={12}>
                    <FormControl variant="standard" fullWidth>
                      <InputLabel shrink htmlFor="bootstrap-input">
                        <Typography variant="h6">
                          <strong>Respiratory Rate : </strong>
                        </Typography>
                      </InputLabel>
                      <BootstrapInput
                        disabled={!edit}
                        defaultValue={
                          content[2][1]?.vital_signs?.respiratory_rate || 0
                        }
                        id="bootstrap-input"
                        multiline
                        name="respiratory_rate"
                        onChange={(e) => handleVitalsChange(e, 2)}
                        endAdornment={
                          <InputAdornment position="end">/min</InputAdornment>
                        }
                      />
                    </FormControl>
                  </Grid>
                  <Grid item md={2.5} sm={5} xs={12}>
                    <FormControl variant="standard" fullWidth>
                      <InputLabel shrink htmlFor="bootstrap-input">
                        <Typography variant="h6">
                          <strong>Temperature : </strong>
                        </Typography>
                      </InputLabel>
                      <BootstrapInput
                        disabled={!edit}
                        defaultValue={
                          content[2][1]?.vital_signs?.temperature || 0
                        }
                        id="bootstrap-input"
                        multiline
                        name="temperature"
                        onChange={(e) => handleVitalsChange(e, 2)}
                        endAdornment={
                          <InputAdornment position="end">°C</InputAdornment>
                        }
                      />
                    </FormControl>
                  </Grid>
                </Grid>
              </AccordionDetails>
            </Accordion>
            <Accordion>
              <AccordionSummary
                alignItems={"center"}
                expandIcon={<ExpandMoreIcon />}
              >
                <PlanIcon sx={{ marginRight: "5px" }} />
                <Typography variant="h6">
                  <strong>Assessment</strong>
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong> Differential Diagnosis : </strong>
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[3][1]?.differential_diagnosis || "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="differential_diagnosis"
                    onChange={(e) => handleSummaryChange(e, 3)}
                  />
                </FormControl>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong>Preliminary Diagnosis:</strong>{" "}
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[3][1]?.preliminary_diagnosis || "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="preliminary_diagnosis"
                    onChange={(e) => handleSummaryChange(e, 3)}
                  />
                </FormControl>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong>Risk Factors:</strong>{" "}
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[3][1]?.risk_factors || "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="risk_factors"
                    onChange={(e) => handleSummaryChange(e, 3)}
                  />
                </FormControl>
              </AccordionDetails>
            </Accordion>
            <Accordion>
              <AccordionSummary
                alignItems={"center"}
                expandIcon={<ExpandMoreIcon />}
              >
                <PlanIcon sx={{ marginRight: "5px" }} />
                <Typography variant="h6">
                  <strong>Plans</strong>
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong> Diagnostic Plan: </strong>
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[4][1]?.diagnostic_plan || "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="diagnostic_plan"
                    onChange={(e) => handleSummaryChange(e, 4)}
                  />
                </FormControl>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong>Treatment Plan:</strong>{" "}
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[4][1]?.treatment_plan || "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="treatment_plan"
                    onChange={(e) => handleSummaryChange(e, 4)}
                  />
                </FormControl>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong>Patient Education:</strong>{" "}
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={
                      content[4][1]?.patient_education || "Not Available"
                    }
                    id="bootstrap-input"
                    multiline
                    name="patient_education"
                    onChange={(e) => handleSummaryChange(e, 4)}
                  />
                </FormControl>
                <FormControl variant="standard" fullWidth>
                  <InputLabel shrink htmlFor="bootstrap-input">
                    <Typography variant="h6">
                      <strong>Follow Up:</strong>{" "}
                    </Typography>
                  </InputLabel>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={content[4][1]?.follow_up || "Not Available"}
                    id="bootstrap-input"
                    multiline
                    name="follow_up"
                    onChange={(e) => handleSummaryChange(e, 4)}
                  />
                </FormControl>
              </AccordionDetails>
            </Accordion>
            <Accordion>
              <AccordionSummary
                alignItems={"center"}
                expandIcon={<ExpandMoreIcon />}
              >
                <PrescriptionIcon sx={{ marginRight: "5px" }} />{" "}
                <Typography variant="h6">
                  <strong>Prescription</strong>
                </Typography>
              </AccordionSummary>
              <VitalsContainer>
                {edit && 
                  <div style={{ padding: "0 20px"}}>
                    <CustomAutoComplete
                      placeholder="Enter Medicine"
                      options={medicationsOpts}
                      handleInputChange={handleMedicationsChange}
                      setOptions={setMedicationsOpts}
                      handleOptionChange={handleMedications}
                      handleClearOptions={clearMedicationOptions}
                    />
                  </div>
                }
                {medications?.length > 0 && (
                  <div style={{ margin: "25px 5px 0" }}>
                    {medications
                      ?.slice(0)
                      .reverse()
                      .map((item, index) => (
                        <FieldSpecsContainer key={index}>
                          <RecordLayout>
                            <>
                            <TextField
                              label="Medicine"
                              value = {item?.label || item}
                            />
                            </>
                          </RecordLayout>
                          <TextBoxLayout
                            className="desktopTextBoxLayout"
                            style={{ minWidth: "90px" }}
                          >
                            <TextField
                              placeholder="Frequency"
                              value={
                                medicationsSpecs[item?.label]?.frequency ||
                                ""
                              }
                              onChange={(e) =>
                                handleMedicationsTextChange(
                                  item,
                                  "frequency",
                                  e.target.value
                                )
                              }
                              type="tel"
                              inputProps={{ maxLength: 5 }}
                              label="Frequency"
                              variant="outlined"
                              disabled={!edit}
                            />
                          </TextBoxLayout>
                          <TextBoxLayout className="desktopTextBoxLayout">
                            <Autocomplete
                              options={timingOptions} // Replace with your actual timing options
                              value={medicationsSpecs[item?.label]?.time_of_day}
                              onChange={(event, newValue) =>
                                handleMedicationsTextChange(
                                  item,
                                  "time_of_day",
                                  newValue
                                )
                              }
                              disabled={!edit}
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
                              options={generateDoseOptions(dosages, item)}
                              value={
                                medicationsSpecs[item?.label]?.dosages || ""
                              }
                              onChange={(e, newValue) =>
                                handleMedicationOptionsChange(
                                  item,
                                  newValue,
                                  "dosages"
                                )
                              }
                              // inputValue={dose}
                              disabled={!edit}
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
                                medicationsSpecs[item?.label]?.duration || ""
                              }
                              onChange={(e, newValue) =>
                                handleMedicationOptionsChange(
                                  item,
                                  newValue,
                                  "duration"
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
                              disabled={!edit}
                            />
                          </TextBoxLayout>
                          <TextBoxLayout className="mobileTextBoxLayout frequencyInput">
                            <TextField
                              placeholder="Frequency"
                              type="tel"
                              value={
                                medicationsSpecs[item?.label]?.frequency ||
                                ""
                              }
                              onChange={(e) =>
                                handleMedicationsTextChange(
                                  item,
                                  "frequency",
                                  e.target.value
                                )
                              }
                              disabled={!edit}
                              inputProps={{ maxLength: 5 }}
                              label="Frequency"
                              variant="outlined"
                            />
                          </TextBoxLayout>
                          <TextBoxLayout className="mobileTextBoxLayout addMinWidth">
                            <Autocomplete
                              options={timingOptions} // Replace with your actual timing options
                              value={
                                medicationsSpecs[item?.label]?.time_of_day || ""
                              }
                              onChange={(event, newValue) =>
                                handleMedicationsTextChange(
                                  item,
                                  "time_of_day",
                                  newValue
                                )
                              }
                              disabled={!edit}
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
                              <TextField
                                placeholder="Instructions"
                                value={
                                  medicationsSpecs[item?.label]?.instructions || ""
                                }
                                onChange={(e) =>
                                  handleMedicationsTextChange(
                                    item,
                                    "instructions",
                                    e.target.value
                                  )
                                }
                                disabled={!edit}
                                label="Instructions"
                                variant="outlined"
                              />
                            </TextBoxLayout>
                          </NotesWrapper>
                          {/* <AddCircleRoundedIcon
                            onClick={handleAddNewMedication}
                          /> */}
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
                                      placeholder="Instructions"
                                      value={
                                        medicationsSpecs[item?.label]
                                          ?.instructions || ""
                                      }
                                      onChange={(e) =>
                                        handleMedicationsTextChange(
                                          item,
                                          "instructions",
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
                {edit && <Button onClick={handleUpdateMedications}>Save Changes</Button> }
              </VitalsContainer>
            </Accordion>
            <Accordion>
              <AccordionSummary
                alignItems={"center"}
                expandIcon={<ExpandMoreIcon />}
              >
                <TestIcon sx={{ marginRight: "5px" }} />{" "}
                <Typography variant="h6">
                  <strong>Tests To Be Taken</strong>
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <>
                  <div>
                    <Typography gutterBottom>Imaging Tests:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="imaging_tests"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 5, newValue, "imaging_tests")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[5][1]?.imaging_tests || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Imaging Tests"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                5,
                                [
                                  ...(content[5][1]?.imaging_tests || []),
                                  value.trim(),
                                ],
                                "imaging_tests"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  5,
                                  [
                                    ...(content[5][1]?.imaging_tests || []),
                                    value.trim(),
                                  ],
                                  "imaging_tests"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>
                  <div>
                    <Typography gutterBottom>Laboratory Tests:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="laboratory_tests"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 5, newValue, "laboratory_tests")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[5][1]?.laboratory_tests || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Laboratory Tests"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                5,
                                [
                                  ...(content[5][1]?.laboratory_tests || []),
                                  value.trim(),
                                ],
                                "laboratory_tests"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  5,
                                  [
                                    ...(content[5][1]?.laboratory_tests || []),
                                    value.trim(),
                                  ],
                                  "laboratory_tests"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>
                  <div>
                    <Typography gutterBottom>Special Exams:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="special_exams"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 5, newValue, "special_exams")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[5][1]?.special_exams || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Special Exam"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                5,
                                [
                                  ...(content[5][1]?.special_exams || []),
                                  value.trim(),
                                ],
                                "special_exams"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  5,
                                  [
                                    ...(content[5][1]?.special_exams || []),
                                    value.trim(),
                                  ],
                                  "special_exams"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>
                </>
              </AccordionDetails>
            </Accordion>
            <Accordion>
              <AccordionSummary
                alignItems={"center"}
                expandIcon={<ExpandMoreIcon />}
              >
                <NextStepsIcon sx={{ marginRight: "5px" }} />{" "}
                <Typography variant="h6">
                  <strong>Other Next Steps</strong>
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <>
                  <div>
                    <Typography gutterBottom>Consultations:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="consultations"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 6, newValue, "consultations")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[6][1]?.consultations || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Consultations"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                6,
                                [
                                  ...(content[6][1]?.consultations || []),
                                  value.trim(),
                                ],
                                "consultations"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  6,
                                  [
                                    ...(content[6][1]?.consultations || []),
                                    value.trim(),
                                  ],
                                  "consultations"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>

                  <div>
                    <Typography gutterBottom>
                      Lifestyle Modifications:
                    </Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="lifestyle_modifications"
                      onChange={(e, newValue) =>
                        handleChipChange(
                          e,
                          6,
                          newValue,
                          "lifestyle_modifications"
                        )
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[6][1]?.lifestyle_modifications || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Lifestyle Modifications"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                6,
                                [
                                  ...(content[6][1]?.lifestyle_modifications ||
                                    []),
                                  value.trim(),
                                ],
                                "lifestyle_modifications"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  6,
                                  [
                                    ...(content[6][1]
                                      ?.lifestyle_modifications || []),
                                    value.trim(),
                                  ],
                                  "lifestyle_modifications"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>

                  <div>
                    <Typography gutterBottom>Precautions:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="precautions"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 6, newValue, "precautions")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[6][1]?.precautions || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Precautions"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                6,
                                [
                                  ...(content[6][1]?.precautions || []),
                                  value.trim(),
                                ],
                                "precautions"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  6,
                                  [
                                    ...(content[6][1]?.precautions || []),
                                    value.trim(),
                                  ],
                                  "precautions"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>

                  <div>
                    <Typography gutterBottom>Referrals:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      disabled={!edit}
                      name="referrals"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 6, newValue, "referrals")
                      }
                      id="tags-filled"
                      options={[]}
                      value={content[6][1]?.referrals || []}
                      clearOnBlur={true}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={index} // Use index as key if items are unique
                            {...getTagProps({ index })}
                          />
                        ))
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Referrals"
                          onBlur={(e) => {
                            const { value } = e.target;
                            if (value.trim() !== "") {
                              handleChipChange(
                                e,
                                6,
                                [
                                  ...(content[6][1]?.referrals || []),
                                  value.trim(),
                                ],
                                "referrals"
                              );
                            }
                          }}
                          onKeyDown={(e) => {
                            if (e.key === "Enter" || e.key === ",") {
                              const { value } = e.target;
                              if (value.trim() !== "") {
                                handleChipChange(
                                  e,
                                  6,
                                  [
                                    ...(content[6][1]?.referrals || []),
                                    value.trim(),
                                  ],
                                  "referrals"
                                );
                                e.target.value = ""; // Clear input after adding chip
                              }
                            }
                          }}
                        />
                      )}
                    />
                  </div>
                </>
              </AccordionDetails>
            </Accordion>
            <Accordion>
              <AccordionSummary
                alignItems={"center"}
                expandIcon={<ExpandMoreIcon />}
              >
                <NotesIcon sx={{ marginRight: "5px" }} />{" "}
                <Typography variant="h6">
                  <strong>Additional Notes</strong>
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <FormControl variant="standard" fullWidth>
                  <BootstrapInput
                    disabled={!edit}
                    defaultValue={content[8][1]?.content || "Not Available"}
                    id="bootstrap-input"
                    multiline
                    name="content"
                    onChange={(e) => handleSummaryChange(e, 8)}
                  />
                </FormControl>
              </AccordionDetails>
            </Accordion>
          </DialogContent>
          <DialogActions gap={2}>
            <Button variant="outlined" onClick={handleFollowUp}>
              Follow Up
            </Button>
            {!edit ? (
              <Button
                sx={{
                  width: "50px",
                  "@media screen and (min-width: 0px) and (max-width: 600px)": {
                    paddingY: "17px",
                  },
                }}
                autoFocus
                variant="outlined"
                onClick={() => setEdit(!edit)}
              >
                Edit
              </Button>
            ) : (
              <Button
                sx={{ width: "150px" }}
                autoFocus
                variant="outlined"
                onClick={handleSavechanges}
              >
                Save Changes
              </Button>
            )}
            <Button
              onClick={handleReviewPrescription}
              autoFocus
              variant="contained"
              disabled={edit}
            >
              Review Prescription
            </Button>{" "}
          </DialogActions>
        </Dialog>
        <Dialog
          fullScreen
          open={openPdf}
          onClose={() => setOpenPdf(false)}
          aria-labelledby="responsive-dialog-title"
        >
          <AppBar position="relative">
            <Toolbar>
              <div style={{ flexGrow: 1 }}></div>{" "}
              {/* This div pushes the following items to the end */}
              <IconButton
                edge="end"
                color="inherit"
                onClick={() => setOpenPdf(false)}
                aria-label="close"
              >
                <CloseIcon />
              </IconButton>
            </Toolbar>
          </AppBar>
          <SendPMR
            notifyModal={notifyModal}
            handleNotifyModalClose={() => setNotifyModal(false)}
            documentId={documentID}
          />
          {!isMobile ? (
            <PDFViewerWrapper>
              <div style={{ width: "100%", height: "100%" }}>
                <embed
                  style={{ width: "100%", height: "100%" }}
                  src={`data:application/pdf;base64,${data}`}
                />
              </div>
              <PDFButtonWrapper>
                <PrimaryButton variant="contained" onClick={postPMR}>
                  Finish Prescription
                </PrimaryButton>
              </PDFButtonWrapper>
            </PDFViewerWrapper>
          ) : (
            <>
              <PDFButtonWrapper
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "16px",
                  marginBottom: "10px",
                }}
              >
                <PrimaryButton variant={"contained"} onClick={postPMR}>
                  Finish Prescription
                </PrimaryButton>
              </PDFButtonWrapper>
              <PDFViewerWrapper>
                <Document file={pdfUrl} onLoadSuccess={onDocumentLoadSuccess}>
                  {Array.apply(null, Array(numPages))
                    .map((x, i) => i + 1)
                    .map((page) => (
                      <Page
                        wrap
                        pageNumber={page}
                        renderTextLayer={false}
                        width={width}
                        height="auto"
                      />
                    ))}
                  {/* {Array.from({ length: numPages }, (v, i) => i + 1).map(
                    (page) => (
                      <Page
                        key={`page_${page}`}
                        pageNumber={page}
                        renderTextLayer={false}
                        width={getWindowDimensions().width}
                      />
                    )
                  )} */}
                </Document>
              </PDFViewerWrapper>
            </>
          )}
        </Dialog>
      </ThemeProvider>
      <Modal
        open={openFollowUp}
        onClose={handleFollowUpClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Toolbar stye={{ padding: 0 }}>
            <Typography sx={{ flex: 1, fontSize: "20px" }} component="div">
              Follow Up Date
            </Typography>
            <IconButton
              edge="end"
              color="inherit"
              onClick={handleFollowUpClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
          </Toolbar>
          <TextField
            sx={{ width: "100%", marginBottom: "20px" }}
            type="date"
            inputProps={{
              min: format(new Date(), "yyyy-MM-dd"), // Set max date to the current date
            }}
            value={selectedDate}
            onChange={handleFollowUpDateChange}
          />
          <PrimaryButton onClick={handleFollowUpClose}>Submit</PrimaryButton>
        </Box>
      </Modal>
      {/* <Calendar
        selectedDate={selectedDate}
        setSelectedDate={setSelectedDate}
        openCalendar={openCalendar}
        setOpenCalendar={setOpenCalendar}
      /> */}
    </React.Fragment>
  );
}
