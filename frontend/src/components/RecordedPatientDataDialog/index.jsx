import * as React from "react";
import Button from "@mui/material/Button";
import { styled } from "@mui/material/styles";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";
import Typography from "@mui/material/Typography";
import { Box, List, ListItem, Stack } from "@mui/material";
import { useState } from "react";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
    overflowY: "scroll",
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));

export default function CustomizedSummaryDialog({
  open,
  setOpen,
  summaryContent,
}) {
  const handleClickOpen = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };
  console.log(summaryContent?.data);
  const content = Object.entries(summaryContent?.data);
  console.log(content);

  return (
    <React.Fragment>
      <Button variant="outlined" onClick={handleClickOpen}>
        See More...
      </Button>
      <BootstrapDialog
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
      >
        <DialogTitle
          sx={{ m: 0, p: 2, display: "flex" }}
          id="customized-dialog-title"
        >
          <Stack
            justifyContent={"center"}
            alignItems={"center"}
            sx={{ backgroundColor: "#0089E9", width: "130px", padding: "5px" }}
          >
            <Typography
              sx={{ fontSize: "1rem", fontWeight: 500, color: "white" }}
              variant="h2"
            >
              CLINICAL NOTE
            </Typography>
          </Stack>
          <Stack ml={5} justifyContent={"center"} alignItems={"center"}>
            <Typography color={"#0089E9"}>PATIENT VISIT SUMMARY</Typography>
          </Stack>
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={{
            position: "absolute",
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
        <DialogContent dividers>
          <Typography variant="h3" gutterBottom>
            Consultation Summary
          </Typography>
          <Typography gutterBottom>{content[0][1]?.summary}</Typography>
          <hr />
          <Typography variant="h3" gutterBottom>
            Subjective{" "}
          </Typography>
          {content[1][1]?.allergy_information.length > 0 && (
            <div>
              <Typography gutterBottom>Allergies:</Typography>
              <List>
                {content[1][1]?.allergy_information.map((item, index) => (
                  <ListItem key={index}>{item}</ListItem>
                ))}
              </List>
            </div>
          )}
          <Typography>
            <strong>Cheif Complaint : </strong>
            {content[1][1]?.chief_complaint}
          </Typography>
          {content[1][1]?.family_history.length > 0 && (
            <div>
              <Typography gutterBottom>Allergies:</Typography>
              <List>
                {content[1][1]?.family_history.map((item, index) => (
                  <ListItem key={index}>{item}</ListItem>
                ))}
              </List>
            </div>
          )}
          {content[1][1]?.history_of_present_illness.length > 0 && (
            <div>
              <Typography gutterBottom>History of present illness: </Typography>
              <List>
                {content[1][1]?.history_of_present_illness.map(
                  (item, index) => (
                    <ListItem key={index}>{item}</ListItem>
                  )
                )}
              </List>
            </div>
          )}
          {content[1][1]?.medication_history.length > 0 && (
            <div>
              <Typography gutterBottom>Medication History: </Typography>
              <List>
                {content[1][1]?.medication_history.map((item, index) => (
                  <ListItem key={index}>{item}</ListItem>
                ))}
              </List>
            </div>
          )}
          {content[1][1]?.past_medical_history.length > 0 && (
            <div>
              <Typography gutterBottom>Past Medical History: </Typography>
              <List>
                {content[1][1]?.past_medical_history.map((item, index) => (
                  <ListItem key={index}>{item}</ListItem>
                ))}
              </List>
            </div>
          )}
          {content[1][1]?.review_of_systems.length > 0 && (
            <div>
              <Typography gutterBottom>Review of System: </Typography>
              <List>
                {content[1][1]?.review_of_systems.map((item, index) => (
                  <ListItem key={index}>{item}</ListItem>
                ))}
              </List>
            </div>
          )}
          {content[1][1]?.social_history.length > 0 && (
            <div>
              <Typography gutterBottom>Social History: </Typography>
              <List>
                {content[1][1]?.social_history.map((item, index) => (
                  <ListItem key={index}>{item}</ListItem>
                ))}
              </List>
            </div>
          )}
          <hr />
          <Typography variant="h3">Doctor's Assessment</Typography>
          <List>
            <ListItem>
              Differential Diagnosis :{" "}
              {content[3][1]?.differential_diagnosis || "Not Available"}
            </ListItem>
            <ListItem>
              Preliminary Diagnosis :{" "}
              {content[4][1]?.preliminary_diagnosis || "Not Available"}
            </ListItem>
            <ListItem>
              Risk Factors : {content[3][1]?.risk_factors || "Not Available"}
            </ListItem>
            <ListItem>
              Treatment Plan: {content[3][1]?.treatment_plan || "Not Available"}
            </ListItem>
          </List>
          <hr />
          <Typography variant="h3">Plans</Typography>
          <List>
            <ListItem>
              Diagnostic Plan :{" "}
              {content[4][1]?.diagnostic_plan || "Not Available"}
            </ListItem>
            <ListItem>
              Follow up : {content[4][1]?.follow_up || "Not Available"}
            </ListItem>
            <ListItem>
              Patient Education:{" "}
              {content[4][1]?.patient_education || "Not Available"}
            </ListItem>
            <ListItem>
              Treatment Plan: {content[4][1]?.treatment_plan || "Not Available"}
            </ListItem>
          </List>
          <hr />
          <Typography variant="h3">Presciption</Typography>
          <List>
            Medications:
            {content[7][1]?.medications.length > 0 &&
              content[7][1]?.medications.map((item) => {
                <ListItem>{item}</ListItem>;
              })}
          </List>
          <hr />
          <Typography variant="h3">Test To be Taken: </Typography>
          <List>
            Imaging Test:
            {content[5][1]?.imaging_tests.length > 0 &&
              content[5][1]?.imaging_tests.map((item) => {
                <ListItem>{item}</ListItem>;
              })}
          </List>
          <List>
            Laboratory Test:
            {content[5][1]?.laboratory_tests.length > 0 &&
              content[5][1]?.laboratory_tests.map((item) => {
                <ListItem>{item}</ListItem>;
              })}
          </List>
          <List>
            Special Exams:
            {content[5][1]?.special_exams.length > 0 &&
              content[5][1]?.special_exams.map((item) => {
                <ListItem>{item}</ListItem>;
              })}
          </List>
          <hr />
          <Typography variant="h3">Other Next Steps: </Typography>
          <List>
            Consultations :
            {content[6][1]?.consultations.length > 0 &&
              content[6][1]?.consultations.map((item) => {
                <ListItem>{item}</ListItem>;
              })}
          </List>
          <List>
            Lifestyle Modifications :
            {content[6][1]?.lifestyle_modifications.length > 0 &&
              content[6][1]?.lifestyle_modifications.map((item) => {
                <ListItem>{item}</ListItem>;
              })}
          </List>
          <List>
            Precautions:
            {content[6][1]?.precautions.length > 0 &&
              content[6][1]?.precautions.map((item) => {
                <ListItem>{item}</ListItem>;
              })}
          </List>
          <List>
            Referrals:
            {content[6][1]?.referrals.length > 0 &&
              content[6][1]?.referrals.map((item) => {
                <ListItem>{item}</ListItem>;
              })}
          </List>
          <hr />
          <Typography variant="h3" gutterBottom>
            Additional Notes
          </Typography>
          <Typography gutterBottom>{content[8][1]?.content}</Typography>
          <hr />
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={handleClose}>
            Save changes
          </Button>
        </DialogActions>
      </BootstrapDialog>
    </React.Fragment>
  );
}
