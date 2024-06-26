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
import AspectRatioIcon from "@mui/icons-material/AspectRatio";
import AllergyIcon from "@mui/icons-material/HealthAndSafety";
import ComplaintIcon from "@mui/icons-material/ReportProblem";
import HistoryIcon from "@mui/icons-material/History";
import MedicationIcon from "@mui/icons-material/Medication";
import AssessmentIcon from "@mui/icons-material/Assignment";
import PlanIcon from "@mui/icons-material/FactCheck";
import PrescriptionIcon from "@mui/icons-material/Description";
import TestIcon from "@mui/icons-material/Biotech";
import NextStepsIcon from "@mui/icons-material/Forward";
import NotesIcon from "@mui/icons-material/Notes";
import { Box, List, ListItem, Stack, Tooltip } from "@mui/material";
import { useState } from "react";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiPaper-root": {
    borderRadius: "15px",
    border: "5px solid ",
    animation: "borderAnimation 3s infinite",
    "@keyframes borderAnimation": {
      "0%": {
        borderColor: "#000000",
      },
      "25%": {
        borderColor: "#333333",
      },
      "50%": {
        borderColor: "#666666",
      },
      "75%": {
        borderColor: "#999999",
      },
      "100%": {
        borderColor: "#CCCCCC",
      },
    }, // Change this to your desired border radius
  },
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
      <Tooltip title="See More">
        <IconButton
          variant="text"
          onClick={handleClickOpen}
          sx={{ backgroundColor: "#89f2ff61" }}
        >
          <AspectRatioIcon sx={{ color: "#1976d2" }} />
        </IconButton>
      </Tooltip>
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
          <Typography variant="h6" gutterBottom>
            <strong>Consultation Summary</strong>
          </Typography>
          <Typography gutterBottom>{content[0][1]?.summary}</Typography>
          <hr />
          <Typography variant="h6" gutterBottom>
            <AllergyIcon /> <strong>Subjective</strong>
          </Typography>
          {content[1][1]?.allergy_information.length > 0 && (
            <div>
              <Typography gutterBottom>Allergies:</Typography>
              <List sx={{ listStyleType: "circle", pl: 4 }}>
                {content[1][1]?.allergy_information.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
              </List>
            </div>
          )}
          <Typography gutterBottom>
            <ComplaintIcon /> <strong>Chief Complaint:</strong>{" "}
            {content[1][1]?.chief_complaint}
          </Typography>
          {content[1][1]?.family_history.length > 0 && (
            <div>
              <Typography gutterBottom>Family History:</Typography>
              <List sx={{ listStyleType: "circle", pl: 4 }}>
                {content[1][1]?.family_history.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
              </List>
            </div>
          )}
          {content[1][1]?.history_of_present_illness.length > 0 && (
            <div>
              <Typography gutterBottom>History of Present Illness:</Typography>
              <List sx={{ listStyleType: "circle", pl: 4 }}>
                {content[1][1]?.history_of_present_illness.map(
                  (item, index) => (
                    <ListItem key={index} sx={{ display: "list-item" }}>
                      {item}
                    </ListItem>
                  )
                )}
              </List>
            </div>
          )}
          {content[1][1]?.medication_history.length > 0 && (
            <div>
              <Typography gutterBottom>Medication History:</Typography>
              <List sx={{ listStyleType: "circle", pl: 4 }}>
                {content[1][1]?.medication_history.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
              </List>
            </div>
          )}
          {content[1][1]?.past_medical_history.length > 0 && (
            <div>
              <Typography gutterBottom>Past Medical History:</Typography>
              <List sx={{ listStyleType: "circle", pl: 4 }}>
                {content[1][1]?.past_medical_history.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
              </List>
            </div>
          )}
          {content[1][1]?.review_of_systems.length > 0 && (
            <div>
              <Typography gutterBottom>Review of Systems:</Typography>
              <List sx={{ listStyleType: "circle", pl: 4 }}>
                {content[1][1]?.review_of_systems.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
              </List>
            </div>
          )}
          {content[1][1]?.social_history.length > 0 && (
            <div>
              <Typography gutterBottom>Social History:</Typography>
              <List sx={{ listStyleType: "circle", pl: 4 }}>
                {content[1][1]?.social_history.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
              </List>
            </div>
          )}
          <hr />
          <Typography variant="h6" gutterBottom>
            <AssessmentIcon /> <strong>Doctor's Assessment</strong>
          </Typography>
          <List>
            <ListItem>
              <strong>Differential Diagnosis:</strong>{" "}
              {content[3][1]?.differential_diagnosis || "Not Available"}
            </ListItem>
            <ListItem>
              <strong>Preliminary Diagnosis:</strong>{" "}
              {content[4][1]?.preliminary_diagnosis || "Not Available"}
            </ListItem>
            <ListItem>
              <strong>Risk Factors:</strong>{" "}
              {content[3][1]?.risk_factors || "Not Available"}
            </ListItem>
            <ListItem>
              <strong>Treatment Plan:</strong>{" "}
              {content[3][1]?.treatment_plan || "Not Available"}
            </ListItem>
          </List>
          <hr />
          <Typography variant="h6" gutterBottom>
            <PlanIcon /> <strong>Plans</strong>
          </Typography>
          <List>
            <ListItem>
              <strong>Diagnostic Plan:</strong>{" "}
              {content[4][1]?.diagnostic_plan || "Not Available"}
            </ListItem>
            <ListItem>
              <strong>Follow Up:</strong>{" "}
              {content[4][1]?.follow_up || "Not Available"}
            </ListItem>
            <ListItem>
              <strong>Treatment Plan:</strong>{" "}
              {content[4][1]?.treatment_plan || "Not Available"}
            </ListItem>
          </List>
          <hr />
          <Typography variant="h6" gutterBottom>
            <PrescriptionIcon /> <strong>Prescription</strong>
          </Typography>
          <List>
            <Typography gutterBottom>Medications:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[7][1]?.medications.length > 0 &&
                content[7][1]?.medications.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
            </List>
          </List>
          <hr />
          <Typography variant="h6" gutterBottom>
            <TestIcon /> <strong>Tests To Be Taken</strong>
          </Typography>
          <List>
            <Typography gutterBottom>Imaging Tests:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[5][1]?.imaging_tests.length > 0 &&
                content[5][1]?.imaging_tests.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Laboratory Tests:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[5][1]?.laboratory_tests.length > 0 &&
                content[5][1]?.laboratory_tests.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Special Exams:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[5][1]?.special_exams.length > 0 &&
                content[5][1]?.special_exams.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
            </List>
          </List>
          <hr />
          <Typography variant="h6" gutterBottom>
            <NextStepsIcon /> <strong>Other Next Steps</strong>
          </Typography>
          <List>
            <Typography gutterBottom>Consultations:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[6][1]?.consultations.length > 0 &&
                content[6][1]?.consultations.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Lifestyle Modifications:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[6][1]?.lifestyle_modifications.length > 0 &&
                content[6][1]?.lifestyle_modifications.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Precautions:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[6][1]?.precautions.length > 0 &&
                content[6][1]?.precautions.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Referrals:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[6][1]?.referrals.length > 0 &&
                content[6][1]?.referrals.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    {item}
                  </ListItem>
                ))}
            </List>
          </List>
          <hr />
          <Typography variant="h6" gutterBottom>
            <NotesIcon /> <strong>Additional Notes</strong>
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
