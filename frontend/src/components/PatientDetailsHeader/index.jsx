import {
  Avatar,
  Box,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  AppBar,
  Slide,
  Toolbar,
  IconButton,
  Typography,
  styled,
  Button,
  TextField,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  FormLabel,
  Grid,
} from "@mui/material";
import React, { useRef, useState } from "react";
import { useEffect } from "react";
import PatientDocuments from "../../components/PatientDocuments";
import { pdf } from "@react-pdf/renderer";
import PMRPdf from "../../components/PMRPdf";
import { postEMR } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import { submitHealthDocument } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import { useNavigate } from "react-router-dom";
import Modal from "@mui/material/Modal";
import { forwardRef } from "react";
import CloseIcon from "@mui/icons-material/Close";
import { useDispatch } from "react-redux";
import { convertDateFormat } from "../../utils/utils";
import CustomLoader from "../CustomLoader";
import CustomizedDialogs from "../Dialog";
import SendPMR from "../../pages/DoctorPage/SendPMR";
import imageCompression from "browser-image-compression";
import EditIcon from "@mui/icons-material/Edit";
import PatientRegistartionForm from "../PatientRegistrationForm";
import { differenceInYears, format } from "date-fns";
import CustomSnackbar from "../CustomSnackbar";
import { registerPatient } from "../../pages/PatientRegistration/PatientRegistration.slice";
import patientDetailsReducer, {
  getPatientDetails,
} from "../../pages/PatientDetails/patientDetailsSlice";
import { apis } from "../../utils/apis";
import BackDropDash from "../BackDropDash";

const rotateImage = {
  // -webkit-transform: "rotate(90deg)",
  // -moz-transform: "rotate(90deg)",
  // -o-transform: "rotate(90deg)",
  // -ms-transform: rotate(90deg);
  transform: "rotate(90deg)",
};

const previewStyling = {
  margin: "1rem .5rem",
  position: "relative",
  boxShadow: "rgba(0,0,0,0.05) 0 1px 2px 0",
};

const deleteImage = {
  position: "absolute",
  top: 0,
  right: 0,
  cutser: "pointer",
  border: 0,
  backgroundColor: "#958c8c",
  color: "#fff",
};

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

const ImageTag = styled("img")(({ theme }) => ({
  "&": {
    width: "200px",
    height: "300px",
    objectFit: "cover",
    [theme.breakpoints.down("sm")]: {
      width: "150px",
      height: "230px",
    },
  },
}));

const DetailsHeaderContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    padding: theme.spacing(5, 6),
    marginBottom: "10px",
    display: "flex",
    [theme.breakpoints.down("md")]: {
      display: "block",
    },
  },
  ".details-header": {
    display: "flex",
    alignItems: "center",
    [theme.breakpoints.down("sm")]: {
      display: "block",
    },
  },
  ".details-avatar-container": {
    [theme.breakpoints.down("md")]: {
      display: "inline",
    },
  },
  ".details-Patientdetails": {
    padding: theme.spacing(0, 6),
    borderRight: `1px solid ${theme.palette.primaryGrey}`,
    [theme.breakpoints.down("md")]: {
      display: "inline",
      borderRight: "0",
    },
  },
  ".details-emailContainer": {
    padding: theme.spacing(0, 6),
    [theme.breakpoints.down("sm")]: {
      display: "inline",
      marginBottom: "10px",
    },
  },
  ".details-subContainer": {
    display: "flex",
    alignItems: "center",
    gap: theme.spacing(2),
  },
  ".details-patient-name": {
    "&.MuiTypography-root": theme.typography.h3,
  },
  ".details-patient-id": {
    "&.MuiTypography-root": theme.typography.body4,
  },
  "details-patient-email": {
    "&.MuiTypography-root": theme.typography.body3,
  },
  displayDocuments: {
    display: "block",
  },
  ".documents-subContainer": {
    display: "flex",
    alignItems: "center",
    [theme.breakpoints.only("md")]: {
      marginTop: "10px",
    },
    [theme.breakpoints.down("sm")]: {
      display: "block ",
    },
  },
}));

const HealthDocUpload = styled("div")(({ theme }) => ({
  "&": {
    [theme.breakpoints.up("sm")]: {
      marginLeft: "15px",
    },
    [theme.breakpoints.down("sm")]: {
      marginTop: "15px",
    },
  },
}));

const PreviewImageWrapper = styled("div")(({ theme }) => ({
  "&": {
    margin: "1rem",
    display: "flex",
    flexWrap: "wrap",
    [theme.breakpoints.down("sm")]: {
      justifyContent: "center",
    },
  },
  [theme.breakpoints.down("sm")]: {
    margin: "0",
  },
}));

const SectionHeader = styled(Typography)(({ theme }) => ({
  "&": theme.typography.sectionBody,
  marginBottom: theme.spacing(4),
}));

const PrimaryButton = styled("button")(({ theme }) => ({
  "&": theme.typography.primaryButton,
}));

const Transition = forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const PatientDetailsHeader = ({ documents }) => {
  const navigate = useNavigate();
  const patient = sessionStorage?.getItem("selectedPatient");
  const [patientData, setPatientData] = useState({});
  const [open, setOpen] = useState(false);
  const [openDocument, setOpenDocument] = useState(false);
  const handleCloseDocument = () => setOpenDocument(false);
  const [openFollowUp, setOpenFollowUp] = useState(false);
  const handleFollowUpClose = () => setOpenFollowUp(false);
  const [imageFiles, setImageFiles] = useState([]);
  const [selectedImages, setSelectedImages] = useState([]);
  const [followUp, setFollowUp] = useState("");
  const [showLoader, setShowLoader] = useState(false);
  const [pmrDialogOpen, setPmrDialogOpen] = useState(false);
  const [notifyModal, setNotifyModal] = useState(false);
  const [documentId, setDocumentId] = useState("");
  const scroll = "paper";
  const handleFileInput = useRef(null);
  const dispatch = useDispatch();
  const [cleared, setCleared] = useState(false);
  const [formOpen, setFormOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [isMobileError, setIsMobileError] = useState(false);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [patientDetails, setPatientdetails] = useState({});
  const [newPatientDetails, setNewPatientDetails] = useState({});

  useEffect(() => {
    if (cleared) {
      const timeout = setTimeout(() => {
        setCleared(false);
      }, 1500);

      return () => clearTimeout(timeout);
    }
    return () => {};
  }, [cleared]);

  useEffect(() => {
    const currentPatient = JSON.parse(patient);

    if (currentPatient) {
      if (Object.keys(currentPatient)?.length) {
        setPatientData(currentPatient);
        setPatientdetails(currentPatient);
      } else {
        setPatientData({});
      }
    }
  }, []);

  const onSnackbarClose = () => {
    setShowSnackbar(false);
  };

  const handleNotifyModalClose = () => {
    setNotifyModal(false);
  };

  const handlePmrDialogClose = () => {
    setPmrDialogOpen(false);
  };

  const handleClick = (e) => {
    handleFileInput.current.click();
  };

  const handleImageChange = async (event) => {
    const imageFile = event.target.files[0];

    const options = {
      maxSizeMB: 1,
      maxWidthOrHeight: 1920,
      useWebWorker: true,
    };
    const files = Array.from(event.target.files);
    try {
      const compressedFile = await imageCompression(imageFile, options);
      const image = new Image();
      image.src = compressedFile;

      const orientation = image.width > image.height ? "landscape" : "portrait";
      console.log(`Image orientation: ${orientation}`);
      // if(orientation === "landscape"){
      //   console.log('rotate(90deg)');
      //   compressedFile.style.transform = "rotate(90deg)";
      // }
      setImageFiles((prevFiles) => [...prevFiles, compressedFile]);

      if (event.target.files) {
        const fileArray = files.map((file) => URL.createObjectURL(file));

        setSelectedImages((prevImages) => prevImages.concat(fileArray));
        Array.from(event.target.files).map((file) => {
          URL.revokeObjectURL(file);
        });
      }
      setOpenDocument(true);
    } catch (error) {
      console.log(error);
    }
  };

  const handleDeleteImage = (photo, index) => {
    const files = imageFiles.filter((e, i) => {
      return i !== index;
    });
    setImageFiles(files);
    setSelectedImages(selectedImages.filter((e) => e !== photo));
  };

  const renderPhotos = (source) => {
    return source.map((photo, index) => {
      return (
        <div key={photo} style={previewStyling}>
          <ImageTag src={photo} />
          <IconButton
            onClick={() => handleDeleteImage(photo, index)}
            aria-label="close"
            style={deleteImage}
          >
            <CloseIcon />
          </IconButton>
        </div>
      );
    });
  };

  const handleDateChange = (event) => {
    setFollowUp(event.target.value);
  };

  const handleFollowUp = () => {
    setOpenFollowUp(true);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const onLoaderClose = () => {
    setShowLoader(false);
  };

  const SaveDocument = async () => {
    setShowLoader(true);

    const pmr_id = sessionStorage?.getItem("pmrID");
    const params = {
      pmr_id: pmr_id,
      mode: "handwritten",
    };

    const docPayload = {
      files: imageFiles,
    };

    dispatch(submitHealthDocument({ params, docPayload })).then((res) => {
      setDocumentId(res?.payload?.data?.document_id);
      setShowLoader(false);
      if (res?.meta.requestStatus === "rejected") {
        setPmrDialogOpen(true);
        return;
      } else {
        // setOpenFollowUp(true);
        postPMR();
      }
    });
  };

  const postPMR = async () => {
    const pmr_id = sessionStorage?.getItem("pmrID");

    const pmr_request = {};
    pmr_request["pmr_id"] = pmr_id;
    let appointment_request;
    if (followUp) {
      appointment_request = {
        appointment_id: patientData?.id,
        followup_date: followUp
          ? convertDateFormat(followUp, "yyyy-MM-dd")
          : "",
        consultation_status: "Completed",
      };
    } else {
      appointment_request = {
        appointment_id: patientData?.id,
        consultation_status: "Completed",
      };
    }
    const allData = {
      pmr_request,
      appointment_request,
    };
    dispatch(postEMR(allData))
      .then((res) => {
        setOpenFollowUp(false);
        if (res?.payload) {
          setNotifyModal(true);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };
  //Patient edit form
  const openPatientForm = () => {
    setFormOpen(true);
  };

  const handleFormClose = () => {
    setFormOpen(false);
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setPatientdetails((prevData) => ({
      ...prevData,
      [name]: value,
    }));
    if (name === "DOB") {
      // && value !== "01-01-1900"
      if (value) {
        const age = differenceInYears(new Date(), new Date(value));
        setPatientdetails((prevData) => ({
          ...prevData,
          age_in_years: age,
        }));
      } else {
        setPatientdetails((prevData) => ({
          ...prevData,
          age_in_years: "",
        }));
      }
    } else if (name === "age_in_years") {
      setPatientdetails((prevData) => ({
        ...prevData,
        age_in_years: value,
      }));
      console.log(patientDetails.DOB);
      if (patientDetails.DOB) {
        const birthDate = new Date(patientDetails.DOB);
        const dateToday = new Date();
        let year = dateToday.getFullYear();
        const calculated_birth_year = year - value;
        console.log(calculated_birth_year);
        const birthDay = birthDate.getDate();
        const birthMonth = birthDate.getMonth() + 1;
        // const birthYear = birthDate.getFullYear();
        console.log(birthMonth, birthDay);
        const dateOfBirth = `${calculated_birth_year}-${birthMonth}-${birthDay}`;
        console.log(convertDateFormat(dateOfBirth, "yyyy-MM-dd"));
        setPatientdetails((prevData) => ({
          ...prevData,
          DOB: convertDateFormat(dateOfBirth, "yyyy-MM-dd"),
        }));
      }
    }
  };

  const formatDob = (date) => {
    return format(new Date(date), "yyyy-MM-dd");
  };

  useEffect(() => {
    const patientObject = JSON.parse(patient);
    if (patientObject) {
      const payload = {
        patient_id: patientObject.id,
      };
      console.log(patientObject.id);
      dispatch(getPatientDetails({ payload })).then((res) => {
        const detail = res?.payload;
        console.log(detail);
        setNewPatientDetails(detail);
      });
    }
  }, [patient, dispatch]);
  const handleFormSubmit = () => {
    setShowLoader(true);
    const url = apis?.registerUser;

    const payload = {
      id: patientDetails.id,
      name: patientDetails.name,
      gender: patientDetails.gender,
      DOB: patientDetails.DOB
        ? convertDateFormat(patientDetails?.DOB, "dd-MM-yyyy")
        : "",
      age: patientDetails.age_in_years
        ? patientDetails.age_in_years.toString()
        : "",
      email: patientDetails.email,
      mobile_number: patientDetails.mobile_number,
    };
    dispatch(registerPatient({ payload, url: url })).then((res) => {
      if (res?.payload) {
        setPatientData(patientDetails);
        sessionStorage?.setItem(
          "selectedPatient",
          JSON.stringify(patientDetails)
        );
      } else {
        setErrorMessage("Error while updating details");
        setShowSnackbar(true);
      }
      setShowLoader(false);
      setFormOpen(false);
    });
  };
  const [backDrop, setBackDrop] = useState(false);
  const handleBackdrop = () => {
    setBackDrop(!backDrop);
  };
  return (
    <DetailsHeaderContainer>
      <div>{backDrop && <BackDropDash />}</div>
      <CustomLoader open={showLoader} />
      <div className="details-header">
        <div className="details-avatar-container" onClick={handleBackdrop}>
          <Avatar />
        </div>
        <div className="details-Patientdetails">
          <Typography className="details-patient-name">
            {newPatientDetails?.name || patientData?.name}
          </Typography>
          <div className="details-subContainer">
            <Typography className="details-patient-id">
              {newPatientDetails?.patient_uid || patientData?.patient_uid}
            </Typography>
            <Typography className="details-patient-id">
              {newPatientDetails?.age_in_years + "Y "}
            </Typography>
            <Typography className="details-patient-id">
              {newPatientDetails?.gender}
            </Typography>
          </div>
        </div>
        <div className="details-emailContainer">
          <Typography className="details-patient-email">
            {newPatientDetails?.email || "NOT AVAILABLE"}
          </Typography>
          <Typography className="details-patient-email">
            {patientData?.mobileNumber || patientData?.mobile_number}
          </Typography>
        </div>
        <div className="details-emailContainer">
          <Typography className="details-patient-email">
            {newPatientDetails?.abha_address}
          </Typography>
          <Typography className="details-patient-email">
            {patientData?.abha_number}
          </Typography>
        </div>
        <div className="details-emailContainer">
          <Button onClick={openPatientForm} variant="outlined">
            {" "}
            Edit
          </Button>
        </div>
      </div>
      {documents && (
        <>
          <div className="documents-subContainer">
            <PatientDocuments
              handleClickOpen={handleClickOpen}
              open={open}
              handleClose={handleClose}
              aria-labelledby="scroll-dialog-title"
              aria-describedby="scroll-dialog-description"
            ></PatientDocuments>

            <HealthDocUpload>
              <CustomizedDialogs
                open={pmrDialogOpen}
                handleClose={handlePmrDialogClose}
              />
              <PrimaryButton onClick={handleClick}>Upload Photo</PrimaryButton>
              <label>
                <input
                  style={{ display: "none" }}
                  type="file"
                  id="file"
                  accept="image/*"
                  capture="environment"
                  ref={handleFileInput}
                  onChange={handleImageChange}
                  aria-orientation="vertical"
                  multiple
                />
              </label>
              {/* {imageObject &&  */}
              <Dialog
                fullScreen
                open={openDocument}
                onClose={handleCloseDocument}
                TransitionComponent={Transition}
              >
                <CustomLoader open={showLoader} onClose={onLoaderClose} />
                <AppBar sx={{ position: "relative" }}>
                  <Toolbar>
                    <Typography
                      sx={{ ml: 2, flex: 1 }}
                      variant="h6"
                      component="div"
                    >
                      Patient History
                    </Typography>
                    <IconButton
                      edge="start"
                      color="inherit"
                      onClick={handleCloseDocument}
                      aria-label="close"
                    >
                      <CloseIcon />
                    </IconButton>
                  </Toolbar>
                </AppBar>
                <div>
                  <PreviewImageWrapper>
                    {renderPhotos(selectedImages)}
                  </PreviewImageWrapper>
                  <div style={{ display: "flex", margin: "10px" }}>
                    <PrimaryButton
                      style={{ margin: "0 10px" }}
                      onClick={handleClick}
                    >
                      Add Image
                    </PrimaryButton>
                    <PrimaryButton
                      style={{ marginRight: "10px" }}
                      onClick={handleFollowUp}
                    >
                      Follow Up Date
                    </PrimaryButton>
                    <PrimaryButton onClick={SaveDocument}>
                      Finish Prescription
                    </PrimaryButton>
                  </div>
                  <div>
                    <Modal
                      open={openFollowUp}
                      onClose={handleFollowUpClose}
                      aria-labelledby="modal-modal-title"
                      aria-describedby="modal-modal-description"
                    >
                      <Box sx={style}>
                        <Toolbar stye={{ padding: 0 }}>
                          <Typography
                            sx={{ flex: 1, fontSize: "20px" }}
                            component="div"
                          >
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
                        {/* <LocalizationProvider dateAdapter={AdapterDayjs}>
                          <DemoContainer components={["DatePicker"]}>
                            <DatePicker
                              slotProps={{
                                field: { clearable: true, onClear: () => setCleared(true) },
                                actionBar: {
                                  actions: ['clear'],
                                },
                              }}
                              sx={{ width: "100%" }}
                              disablePast
                              value={followUp}
                              onChange={(newValue) => setFollowUp(newValue)}
                            />
                          </DemoContainer>
                        </LocalizationProvider> */}
                        <TextField
                          sx={{ width: "100%", marginBottom: "20px" }}
                          type="date"
                          inputProps={{
                            min: format(new Date(), "yyyy-MM-dd"), // Set max date to the current date
                          }}
                          value={followUp}
                          onChange={handleDateChange}
                        />
                        <PrimaryButton onClick={handleFollowUpClose}>
                          Submit
                        </PrimaryButton>
                      </Box>
                    </Modal>
                  </div>
                </div>
              </Dialog>
            </HealthDocUpload>
          </div>
        </>
      )}
      <SendPMR
        notifyModal={notifyModal}
        handleNotifyModalClose={handleNotifyModalClose}
        documentId={documentId}
      />
      <Dialog
        open={formOpen}
        onClose={handleFormClose}
        // scroll="paper"
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
      >
        <CustomLoader open={showLoader} />
        <AppBar sx={{ position: "relative" }}>
          <Toolbar>
            <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
              Update Patient Details
            </Typography>
            <IconButton
              edge="start"
              color="inherit"
              onClick={handleFormClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
        <DialogContent>
          <CustomSnackbar
            message={errorMessage || "Something went wrong"}
            open={showSnackbar}
            status={"error"}
            onClose={onSnackbarClose}
          />
          <form>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <TextField
                  label="First Name"
                  name="name"
                  value={patientDetails?.name}
                  onChange={handleChange}
                  InputLabelProps={{ shrink: true }}
                  required
                  fullWidth
                />
              </Grid>
              {/* <Grid item xs={12} md={6}>
                <TextField
                  name="middlename"
                  label="Middle Name"
                  value={patientData?.middlename}
                  onChange={handleChange}
                  InputLabelProps={{ shrink: true }}
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  name="lastname"
                  label="Last Name"
                  value={patientData?.lastname}
                  onChange={handleChange}
                  InputLabelProps={{ shrink: true }}
                  fullWidth
                />
              </Grid> */}
              <Grid item xs={12} md={6}>
                <FormControl component="fieldset">
                  <FormLabel component="legend">Gender</FormLabel>
                  <RadioGroup
                    aria-label="gender"
                    name="gender"
                    value={patientDetails?.gender}
                    onChange={handleChange}
                  >
                    <Grid>
                      <FormControlLabel
                        value="M"
                        control={<Radio />}
                        label="Male"
                      />
                      <FormControlLabel
                        value="F"
                        control={<Radio />}
                        label="Female"
                      />
                      <FormControlLabel
                        value="other"
                        control={<Radio />}
                        label="Other"
                      />
                    </Grid>
                  </RadioGroup>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="DOB"
                  name="DOB"
                  value={patientDetails?.DOB}
                  onChange={handleChange}
                  type="date"
                  inputProps={{
                    max: formatDob(new Date()), // Set max date to the current date
                  }}
                  InputLabelProps={{ shrink: true }}
                  // style={{ width: "50%" }}
                  // required
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Age(in years)"
                  name="age_in_years"
                  value={patientDetails?.age_in_years}
                  onChange={handleChange}
                  InputLabelProps={{ shrink: true }}
                  // style={{ width: "50%" }}
                  // required
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Email Address"
                  name="email"
                  value={patientDetails?.email}
                  onChange={handleChange}
                  type="email"
                  InputLabelProps={{ shrink: true }}
                  // required
                  fullWidth
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  name="mobile_number"
                  label="Mobile Number"
                  type="number"
                  value={patientDetails?.mobile_number}
                  error={isMobileError}
                  onChange={handleChange}
                  InputLabelProps={{ shrink: true }}
                  required
                  fullWidth
                />
              </Grid>
            </Grid>
            <span style={{ color: "red" }}>
              {isMobileError ? "Please enter valid number" : ""}
            </span>
            <br />
          </form>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleFormClose} className="cancel_btn">
            Discard
          </Button>
          <Button onClick={handleFormSubmit} className="ok_btn">
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </DetailsHeaderContainer>
  );
};

export default PatientDetailsHeader;
