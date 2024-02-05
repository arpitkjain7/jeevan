import {FormControlLabel, IconButton, Radio, RadioGroup,  Typography } from "@mui/material";
import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import CloseIcon from '@mui/icons-material/Close';
import styled from "@emotion/styled";
import { useState } from "react";
import SyncAbha from "../SyncAbha";
import { useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { sendNotification } from "../EMRPage/EMRPage.slice";

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
  const [mobile, setMobile] = useState(currentPatient?.mobileNumber);
  const [showAbha, setShowAbha] = useState(false);

  const handleMobileChange = (event) => {
    setMobile(event.target.value);
  };

  const handleChannelChange = (event) => {
    setChannel(event.target.value);
  };

  const handleModalClose = () => {
    setShowSync(false);
  };

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
        if (
          !(
            currentPatient?.patient_details?.abha_number &&
            currentPatient?.patient_details?.abha_number !== ""
          )
        ) {
          sessionStorage.removeItem("pmrID");
          navigate("/appointment-list");
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
    <React.Fragment>
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
        </DialogContent>
        <DialogActions>
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
    </React.Fragment>
  );
}

export default SendPMR;
