import {Checkbox, FormControlLabel, Grid, IconButton, Radio, RadioGroup,  Typography } from "@mui/material";
import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import CloseIcon from '@mui/icons-material/Close';
import { useState } from "react";
import SyncAbha from "../SyncAbha";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { deepLink, googleReview, sendNotification } from "../EMRPage/EMRPage.slice";

const SendPMR= ({
  notifyModal,
  handleNotifyModalClose,
  documentId
}) => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const patient = sessionStorage?.getItem("selectedPatient");
  const currentPatient = JSON.parse(patient);
  const [showSync, setShowSync] = useState(false);
  const [channel, setChannel] = useState('whatsapp');
  const [mobile, setMobile] = useState(currentPatient?.mobile_number || currentPatient?.mobileNumber);
  const [showAbha, setShowAbha] = useState(false);
  const [checked, setChecked] = useState(true);
  const currentHospital = JSON.parse(sessionStorage.getItem("selectedHospital"));
  const handleMobileChange = (event) => {
    setMobile(event.target.value);
  };

  const handleChannelChange = (event) => {
    setChannel(event.target.value);
  };

  const handleModalClose = () => {
    setShowSync(false);
  };

  const handleReviewChange = (event) => {
    setChecked(event.target.checked);
  };

  const handleSkip = () => {
    setShowAbha(true);
  }

  const onSubmit = () => {
    const payload = {
      document_id: documentId,
      pmr_id: sessionStorage.getItem("pmrID"),
      channel: channel,
      mobile_number: mobile
    }
    dispatch(sendNotification(payload)).then((res) => {
      handleNotifyModalClose();
      if(res){
        if(currentHospital?.hip_id === "H3" && checked){
          dispatch(googleReview({channel: payload.channel, mobile_number: payload.mobile_number}));
        }
        if (
          !(
            (currentPatient?.patient_details?.abha_number || currentPatient?.abha_number) &&
            (currentPatient?.patient_details?.abha_number || currentPatient?.abha_number) !== ""
          )
        ) {
          if(currentHospital?.hip_id === "123123"){
            const deepLinkPayload = {
              mobile_no: mobile,
              hip_id: "123123",
              hip_name: currentHospital?.name
            }
            dispatch(deepLink(deepLinkPayload)).then((response) => {
              sessionStorage.removeItem("pmrID");
              navigate("/appointment-list");
            });
          } else {
            sessionStorage.removeItem("pmrID");
            navigate("/appointment-list");
          }
        } else {
          setShowAbha(true);
          setShowSync(true);
        }
      }
    }).catch((error) => {
      console.log(error);
    })
  }

  return (
    <>
      <Dialog
        open={notifyModal}
        onClose={handleNotifyModalClose}
        PaperProps={{
          component: 'form',
        }}
      >
        <DialogTitle>
          Confirm Patient's WhatsApp Number
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleNotifyModalClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
        <DialogContent dividers>
          <DialogContentText>
            Prescription will be sent to the below mentioned phone number. So verify the patient's mobile number and confirm if it is linked to WhatsApp for efficient communication and updates.
          </DialogContentText>
         
          <br/>
          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <Typography>Patient's mobile Number</Typography>
              <TextField
                autoFocus
                required
                id="mobile"
                name="mobile"
                type="tel"
                variant="outlined"
                value={mobile}
                onChange={handleMobileChange}
              /> 
              <br/>
              <RadioGroup
                row
                aria-labelledby="demo-row-radio-buttons-group-label"
                name="row-radio-buttons-group"
                value={channel}
                onChange={handleChannelChange}
                style={{ marginTop: "10px" }}
              >
                {/* <p style={{ verticalAlign: "center" }}>Select Channel</p> */}
                <FormControlLabel value="whatsapp" control={<Radio size="small"/>} label="WhatsApp" />
                <FormControlLabel value="sms" control={<Radio size="small"/>} label="SMS" />
              </RadioGroup>
            </Grid>
            {currentHospital?.hip_id === "H3" &&
              <Grid item xs={12} md={6}>
                <FormControlLabel control={
                  <Checkbox 
                  checked={checked}
                  onChange={handleReviewChange}
                  defaultChecked />
                  } 
                  label="Send Google Review" />
              </Grid>
            }
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSkip}>Skip</Button>
          <Button onClick={handleNotifyModalClose}>Cancel</Button>
          <Button onClick={onSubmit}>Continue</Button>
        </DialogActions>
      </Dialog>
      {showAbha && (
        <SyncAbha
          showSync={showSync}
          handleModalClose={handleModalClose}
        />
      )}
    </>
  );
}

export default SendPMR;
