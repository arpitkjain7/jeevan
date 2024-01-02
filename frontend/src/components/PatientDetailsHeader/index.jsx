import { Avatar, Box, Typography, styled } from "@mui/material";
import React, { useRef, useState } from "react";
import { useEffect } from "react";
import PatientDocuments from "../../components/PatientDocuments";
import Modal from '@mui/material/Modal';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '1px solid #000',
  boxShadow: 24,
  p: 4,
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
  }
}));

const PrimaryButton = styled("Button")(({ theme }) => ({
  "&": theme.typography.primaryButton,
}));

const PatientDetailsHeader = ({ documents }) => {
  const patient = sessionStorage?.getItem("selectedPatient");
  const [patientData, setPatientData] = useState({});
  const [open, setOpen] = useState(false);
  const [openDocument, setOpenDocument] = useState(false);
  const handleCloseDocument = () => setOpenDocument(false);
  const [imageObject, setImageObject] = useState(null);

  const handleFileInput = useRef(null);

  const handleClick = () => {
    handleFileInput.current.click();
  };

  const handleImageChange = (event) => {
    setImageObject({
      imagePreview: URL.createObjectURL(event.target.files[0]),
      imageFile: event.target.files[0],
    });
    setOpenDocument(true);
  };

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

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
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
        )}
        <div>
          <PrimaryButton onClick={handleClick}>Upload Photo</PrimaryButton>
          <label>
            <input
              style={{ display: "none" }}
              type="file"
              accept="image/*"
              capture="environment"
              ref={handleFileInput}
              onChange={handleImageChange}
            />
          </label>
          {imageObject && 
           <Modal
              open={openDocument}
              onClose={handleCloseDocument}
              aria-labelledby="modal-modal-title"
              aria-describedby="modal-modal-description"
            >
              <Box sx={style}>
                <img src={imageObject.imagePreview} />
                <PrimaryButton>Save</PrimaryButton>
              </Box>
            </Modal>
          }
        </div>
      </div>
    </DetailsHeaderContainer>
  );
};

export default PatientDetailsHeader;
