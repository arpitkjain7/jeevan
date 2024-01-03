import { Avatar, Box, Dialog, AppBar, Slide, Toolbar, IconButton, Typography, styled, Button } from "@mui/material";
import React, { useRef, useState } from "react";
import { useEffect } from "react";
import PatientDocuments from "../../components/PatientDocuments";
import { pdf } from "@react-pdf/renderer";
import PMRPdf from "../../components/PMRPdf";
import { postEMR } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import { submitPdf } from "../../components/PMRPdf/pmrPdf.slice";
import { useNavigate } from "react-router-dom";
import Modal from '@mui/material/Modal';
import { forwardRef } from 'react';
import CloseIcon from '@mui/icons-material/Close';
import { useDispatch } from "react-redux";
import { convertDateFormat } from "../../utils/utils";
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import {
  uploadHealthDocument
} from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import CustomLoader from "../CustomLoader";

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '1px solid #000',
  boxShadow: 24,
  padding: "0 16px 16px",
};

const DetailsHeaderContainer = styled("div")(({ theme }) => ({
  "&": {
    backgroundColor: theme.palette.primaryWhite,
    padding: theme.spacing(5, 6),
  },
  ".details-header": {
    display: "flex",
    alignItems: "center",
    [theme.breakpoints.down('sm')]: {
      display: "block"
    },
  },
  ".details-avatar-container": {
    [theme.breakpoints.down('sm')]: {
      display: "inline",
    },
  },
  ".details-Patientdetails": {
    padding: theme.spacing(0, 6),
    borderRight: `1px solid ${theme.palette.primaryGrey}`,
    [theme.breakpoints.down('sm')]: {
      display: "inline",
      borderRight: "0"
    },
  },
  ".details-emailContainer": {
    padding: theme.spacing(0, 6),
    [theme.breakpoints.down('sm')]: {
      display: "inline",
      marginBottom: "10px"
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
  "displayDocuments": {
    display: "block"
  },
  ".documents-subContainer": {
    display: "flex",
    alignItems: "center",
    [theme.breakpoints.down('sm')]: {
      display: "block "
    },
  },
  ".result": {
    minHeight: "100%",
    maxHeight: "auto",
    width: "100%",
    marginTop: "1rem",
    display: "flex",
    flexWrap: "wrap",
    alignItems: "center",
    justifyContent: "left",
  },
}));

const HealthDocUpload = styled("div")(({ theme }) => ({
  "&": {
    [theme.breakpoints.up('sm')]:{
      marginLeft: "15px",
    },
    [theme.breakpoints.down('sm')]:{
      marginTop: "15px",
    }
  }
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
  const [selectedImages, setSelectedImages] = useState([]);
  const [imagesBytes, setImagesBytes] = useState([]);
  const [followUp, setFollowUp] = useState(null);
  const [showLoader, setShowLoader] = useState(false);

  const handleFileInput = useRef(null);
  const dispatch = useDispatch();

  useEffect(() => {
    const currentPatient = JSON.parse(patient);
    if(currentPatient){
      if (Object.keys(currentPatient)?.length) {
        setPatientData(currentPatient);
      } else {
        setPatientData({});
      }
    }
  }, []);

  const handleClick = (e) => {
    handleFileInput.current.click();
  };

  const handleImageChange = async (event) => {
    console.log(event.target.files);
    if(event.target.files){
      const fileArray = Array.from(event.target.files).map((file) => URL.createObjectURL(file));
      console.log(fileArray);
      setSelectedImages((prevImages) => prevImages.concat(fileArray));
      Array.from(event.target.files).map((file) => 
        convertBase64(file).then((result) => {
          setImagesBytes(bytes => [...bytes, result]);
        }).catch((error) => {
          console.log(error);
        })
      );

      Array.from(event.target.files).map(
        (file) => URL.revokeObjectURL(file)
      )
    }
    setOpenDocument(true);
  };

  const convertBase64 = async (file) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file);

      fileReader.onload = () => {
        const data = fileReader.result;
        const bytesData = data.split(',')[1];
        resolve(bytesData);
      };

      fileReader.onerror= (error) => {
        reject(error);
      };
    })
  }
  const renderPhotos = (source) => {
    return source.map((photo) => {
      return <img src={photo} key={photo} style={{ width: "200px",
      height: "300px",
      objectFit: "cover",
      padding: "0.7rem" }}/>
    })
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
    const params = {
      patient_id: patientData?.patient_id,
      appointment_id: patientData?.id,
      hip_id: patientData?.doc_details?.hip_id
    }
    
    const dateToday = new Date();
    const dateTodayFormat = convertDateFormat(dateToday, "yyyy-MM-dd");
    const docPayload = {
      doc_ids: [patientData?.doc_details.id],
      document_types: ["prescription"],
      dates: [dateTodayFormat],
      files: imagesBytes
    }
    console.log(docPayload);
    dispatch(uploadHealthDocument({params, docPayload}))
    .then((res) => {
      setShowLoader(false);
      console.log(res);
      // setShowFollowUp(true);
      setOpenFollowUp(true);
    })
  }

  const createPdfBlob = async () => {
    const hospital = sessionStorage?.getItem("selectedHospital");
    let patientDetails = {};
    if (hospital) {
      const currentHospital = JSON.parse(hospital);
      patientDetails = {
        hospitalName: currentHospital?.name || "-",
        patientName: patientData?.patient_details?.name || patientData?.name || "-",
        doctorName: patientData?.docName || "-",
        patientEmail: patientData?.patient_details?.email || patientData?.email || "-",
        patientGender: patientData?.patient_details?.gender || patientData?.gender || "-",
        patientNumber:  patientData?.mobile_number || patientData?.mobileNumber || "-",
        patientId: patientData?.patientId || "-",
        patientAge: "-",
      };
    }
    // setPatientData(patientDetails);
    const pdfBlob = await pdf(<PMRPdf patientData={patientDetails} />).toBlob();

    const pdfFile = new File([pdfBlob], "patient_record.pdf", {
      type: "application/pdf",
    });

    return pdfFile;
  };

  const postPMR = async () => {
    const pmr_id = sessionStorage?.getItem("pmrID");
    const pdfPayload = {
      document_type: "Prescription",
      pmr_id: pmr_id,
    };

    const pmr_request = {};
    pmr_request["pmr_id"] = pmr_id;
    const appointment_request = {
      appointment_id: patientData?.id,
      followup_date: followUp ? convertDateFormat(followUp, "yyyy-MM-dd") : "",
      consultation_status: "Completed"
    }
    const allData ={
      pmr_request, appointment_request
    }
    const blob = await createPdfBlob();
    dispatch(submitPdf({ blob, pdfPayload })).then(
      dispatch(postEMR(allData)).then((res) => {
          navigate("/appointment-list");
      })
    );
  };

  return (
    <DetailsHeaderContainer>
      <div container className="details-header">
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
              {patientData?.age || patientData?.DOB}
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
        {documents && (
          <>
            <div className="documents-subContainer">
              <PatientDocuments
                handleClickOpen={handleClickOpen}
                open={open}
                handleClose={handleClose}
                aria-labelledby="scroll-dialog-title"
                aria-describedby="scroll-dialog-description"
              >
              </PatientDocuments>
            </div>
        
            <HealthDocUpload>
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
                   <CustomLoader
                    open={showLoader}
                    onClose={onLoaderClose}
                  />
                  <AppBar sx={{ position: 'relative' }}>
                    <Toolbar>
                      <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
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
                    {/* <img src={imageObject.imagePreview} width="350px" height="500px"/> */}
                    <div className="result">
                      {renderPhotos(selectedImages)}
                      <div style = {{ display: "flex"}}>
                        <PrimaryButton style = {{ margin: "0 10px" }} onClick={handleClick}>Upload Image</PrimaryButton>
                        <PrimaryButton onClick={SaveDocument}>Save Document</PrimaryButton>
                      </div>
                      {/* {showFollowUp && ( */}
                        <div>
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
                              <LocalizationProvider dateAdapter={AdapterDayjs}>
                                <DemoContainer components={['DatePicker']}>
                                  <DatePicker sx={{ width: '100%' }} 
                                    disablePast
                                    value={followUp}
                                    onChange={(newValue) => setFollowUp(newValue)}
                                  />
                                </DemoContainer>
                              </LocalizationProvider>
                              <br/>
                              <PrimaryButton onClick={postPMR}>Finish Prescription</PrimaryButton>
                            </Box>
                          </Modal>
                        </div>
                    {/* )} */}
                    </div>
                </Dialog>
              {/* } */}
            </HealthDocUpload>
          
          </>
         )}
      </div>
    </DetailsHeaderContainer>
  );
};

export default PatientDetailsHeader;
