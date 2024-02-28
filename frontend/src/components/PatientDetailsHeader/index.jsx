import {
  Avatar,
  Box,
  Dialog,
  AppBar,
  Slide,
  Toolbar,
  IconButton,
  Typography,
  styled,
  Button,
  TextField,
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
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { uploadHealthDocument } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import CustomLoader from "../CustomLoader";
import CustomizedDialogs from "../Dialog";
import SendPMR from "../../pages/DoctorPage/SendPMR";
import { format } from "date-fns";

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

  const handleFileInput = useRef(null);
  const dispatch = useDispatch();
  const [cleared, setCleared] = useState(false);

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
      } else {
        setPatientData({});
      }
    }
  }, []);

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
    const files = Array.from(event.target.files);
    setImageFiles((prevFiles) => [...prevFiles, ...files]);

    if (event.target.files) {
      const fileArray = files.map((file) => URL.createObjectURL(file));

      setSelectedImages((prevImages) => prevImages.concat(fileArray));
      Array.from(event.target.files).map((file) => {
        URL.revokeObjectURL(file);
      });
    }
    setOpenDocument(true);
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
    setOpenFollowUp(true)
  }

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
    dispatch(postEMR(allData)).then((res) => {
      setOpenFollowUp(false);
      if (res?.payload) {
        setNotifyModal(true);
      }
    })
    .catch((error) => {
      console.log(error);
    })
  };

  return (
    <DetailsHeaderContainer>
      <div className="details-header">
        <div className="details-avatar-container">
          <Avatar />
        </div>
        <div className="details-Patientdetails">
          <Typography className="details-patient-name">
            {patientData?.patient_details?.name || patientData?.name}
          </Typography>
          <div className="details-subContainer">
            <Typography className="details-patient-id">
              {patientData?.patientId || patientData?.id}
            </Typography>
            <Typography className="details-patient-id">
              {(patientData?.patient_details?.age_in_years || patientData?.age_in_years) ? (patientData?.patient_details?.age_in_years || patientData?.age_in_years) + 'Y ' : ""}
              {(patientData?.patient_details?.age_in_months || patientData?.age_in_months) ? (patientData?.patient_details?.age_in_months || patientData?.age_in_months) + 'M' : "" }
              {!((patientData?.patient_details?.age_in_years || patientData?.age_in_years) || (patientData?.patient_details?.age_in_months || patientData?.age_in_months)) ? patientData?.DOB : ""}
            </Typography>
            <Typography className="details-patient-id">
              {patientData?.patient_details?.gender || patientData?.gender}
            </Typography>
          </div>
        </div>
        <div className="details-emailContainer">
          <Typography className="details-patient-email">
            {patientData?.patient_details?.email || patientData?.email}
          </Typography>
          <Typography className="details-patient-email">
            {patientData?.mobileNumber || patientData?.mobile_number}
          </Typography>
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
                    <PrimaryButton  style={{ marginRight: "10px" }} onClick={handleFollowUp}>
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
                          sx={{ width: "100%", marginBottom: "20px"  }}
                          type="date"
                          inputProps={{
                            min: format(new Date(), "yyyy-MM-dd"), // Set max date to the current date
                          }}
                          value={followUp}
                          onChange={handleDateChange}
                        />
                        <PrimaryButton onClick={handleFollowUpClose} >
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
    </DetailsHeaderContainer>
  );
};

export default PatientDetailsHeader;
