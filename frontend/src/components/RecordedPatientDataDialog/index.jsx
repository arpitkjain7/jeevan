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
import AssessmentIcon from "@mui/icons-material/Assignment";
import PlanIcon from "@mui/icons-material/FactCheck";
import PrescriptionIcon from "@mui/icons-material/Description";
import TestIcon from "@mui/icons-material/Biotech";
import NextStepsIcon from "@mui/icons-material/Forward";
import NotesIcon from "@mui/icons-material/Notes";
import ComplaintIcon from "@mui/icons-material/ContactSupport";
import {
  Box,
  List,
  ListItem,
  Stack,
  TextField,
  TextareaAutosize,
  Tooltip,
} from "@mui/material";
import { useState } from "react";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiPaper-root": {
    borderRadius: "15px",
    border: "5px solid ",
    minWidth: "40%",
    animation: "borderAnimation 3s infinite",
    "@keyframes borderAnimation": {
      "0%": { borderColor: "#000000" },
      "25%": { borderColor: "#333333" },
      "50%": { borderColor: "#666666" },
      "75%": { borderColor: "#999999" },
      "100%": { borderColor: "#CCCCCC" },
    },
  },
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
    overflowY: "scroll",
  },
  "& .MuiDialogActions-root": { padding: theme.spacing(1) },
  "& .MuiAccordion-root": {
    animation: "none",
    border: "1px solid #f1f1f1",
    borderRadius: "5px",
    marginBottom: "10px",
  },
}));

export default function CustomizedSummaryDialog({
  open,
  setOpen,
  summaryContent,
  setSummaryContent,
}) {
  const [edit, setEdit] = useState(false);
  const handleClickOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const content = Object.entries(summaryContent?.data);

  const handleContentChange = (sectionIndex, itemIndex, newValue) => {
    const updatedContent = [...content];
    updatedContent[sectionIndex][1][itemIndex] = newValue;
    setSummaryContent(updatedContent);
    setEdit(false);
    // setOpen(false);
  };

  return !edit ? (
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
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <AllergyIcon /> <strong>Subjective</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
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
                Chief Complaint: {content[1][1]?.chief_complaint}
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
                  <Typography gutterBottom>
                    History of Present Illness:
                  </Typography>
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
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <AssessmentIcon /> <strong>Doctor's Assessment</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
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
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <PlanIcon /> <strong>Plans</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
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
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <PrescriptionIcon /> <strong>Prescription</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
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
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <TestIcon /> <strong>Tests To Be Taken</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
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
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <NextStepsIcon /> <strong>Other Next Steps</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
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
                    content[6][1]?.lifestyle_modifications.map(
                      (item, index) => (
                        <ListItem key={index} sx={{ display: "list-item" }}>
                          {item}
                        </ListItem>
                      )
                    )}
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
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <NotesIcon /> <strong>Additional Notes</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography gutterBottom>{content[8][1]?.content}</Typography>
            </AccordionDetails>
          </Accordion>
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={() => setEdit(true)}>
            Edit
          </Button>
        </DialogActions>
      </BootstrapDialog>
    </React.Fragment>
  ) : (
    <React.Fragment>
      <Tooltip title="See More">
        <IconButton
          variant="text"
          onClick={handleClose}
          sx={{ backgroundColor: "#89f2ff61" }}
        >
          <AspectRatioIcon sx={{ color: "#1976d2" }} />
        </IconButton>
      </Tooltip>
      <Dialog
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
          <TextareaAutosize
            minRows={3}
            style={{ width: "100%" }}
            value={content[0][1]?.summary}
            onChange={(e) => handleContentChange(0, "summary", e.target.value)}
          />
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
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedAllergies = [
                          ...content[1][1].allergy_information,
                        ];
                        updatedAllergies[index] = e.target.value;
                        handleContentChange(
                          1,
                          "allergy_information",
                          updatedAllergies
                        );
                      }}
                    />
                  </ListItem>
                ))}
              </List>
            </div>
          )}
          <Typography gutterBottom>
            <ComplaintIcon /> <strong>Chief Complaint:</strong>
            <TextField
              fullWidth
              value={content[1][1]?.chief_complaint}
              onChange={(e) =>
                handleContentChange(1, "chief_complaint", e.target.value)
              }
            />
          </Typography>
          {/* Similarly add TextField/TextareaAutosize for other fields */}
          <hr />
          <Typography variant="h6" gutterBottom>
            <AssessmentIcon /> <strong>Doctor's Assessment</strong>
          </Typography>
          <List>
            <ListItem>
              <strong>Differential Diagnosis:</strong>
              <TextField
                fullWidth
                value={content[3][1]?.differential_diagnosis}
                onChange={(e) =>
                  handleContentChange(
                    3,
                    "differential_diagnosis",
                    e.target.value
                  )
                }
              />
            </ListItem>
            <ListItem>
              <strong>Preliminary Diagnosis:</strong>
              <TextField
                fullWidth
                value={content[4][1]?.preliminary_diagnosis}
                onChange={(e) =>
                  handleContentChange(
                    4,
                    "preliminary_diagnosis",
                    e.target.value
                  )
                }
              />
            </ListItem>
            <ListItem>
              <strong>Risk Factors:</strong>
              <TextField
                fullWidth
                value={content[3][1]?.risk_factors}
                onChange={(e) =>
                  handleContentChange(3, "risk_factors", e.target.value)
                }
              />
            </ListItem>
            <ListItem>
              <strong>Treatment Plan:</strong>
              <TextField
                fullWidth
                value={content[3][1]?.treatment_plan}
                onChange={(e) =>
                  handleContentChange(3, "treatment_plan", e.target.value)
                }
              />
            </ListItem>
          </List>
          <hr />
          <Typography variant="h6" gutterBottom>
            <PlanIcon /> <strong>Plans</strong>
          </Typography>
          <List>
            <ListItem>
              <strong>Diagnostic Plan:</strong>
              <TextField
                fullWidth
                value={content[4][1]?.diagnostic_plan}
                onChange={(e) =>
                  handleContentChange(4, "diagnostic_plan", e.target.value)
                }
              />
            </ListItem>
            <ListItem>
              <strong>Follow Up:</strong>
              <TextField
                fullWidth
                value={content[4][1]?.follow_up}
                onChange={(e) =>
                  handleContentChange(4, "follow_up", e.target.value)
                }
              />
            </ListItem>
            <ListItem>
              <strong>Treatment Plan:</strong>
              <TextField
                fullWidth
                value={content[4][1]?.treatment_plan}
                onChange={(e) =>
                  handleContentChange(4, "treatment_plan", e.target.value)
                }
              />
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
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedMedications = [
                          ...content[7][1].medications,
                        ];
                        updatedMedications[index] = e.target.value;
                        handleContentChange(
                          7,
                          "medications",
                          updatedMedications
                        );
                      }}
                    />
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
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedImagingTests = [
                          ...content[5][1].imaging_tests,
                        ];
                        updatedImagingTests[index] = e.target.value;
                        handleContentChange(
                          5,
                          "imaging_tests",
                          updatedImagingTests
                        );
                      }}
                    />
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Laboratory Tests:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[5][1]?.laboratory_tests.length > 0 &&
                content[5][1]?.laboratory_tests.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedLabTests = [
                          ...content[5][1].laboratory_tests,
                        ];
                        updatedLabTests[index] = e.target.value;
                        handleContentChange(
                          5,
                          "laboratory_tests",
                          updatedLabTests
                        );
                      }}
                    />
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Special Exams:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[5][1]?.special_exams.length > 0 &&
                content[5][1]?.special_exams.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedSpecialExams = [
                          ...content[5][1].special_exams,
                        ];
                        updatedSpecialExams[index] = e.target.value;
                        handleContentChange(
                          5,
                          "special_exams",
                          updatedSpecialExams
                        );
                      }}
                    />
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
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedConsultations = [
                          ...content[6][1].consultations,
                        ];
                        updatedConsultations[index] = e.target.value;
                        handleContentChange(
                          6,
                          "consultations",
                          updatedConsultations
                        );
                      }}
                    />
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Lifestyle Modifications:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[6][1]?.lifestyle_modifications.length > 0 &&
                content[6][1]?.lifestyle_modifications.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedLifestyleMods = [
                          ...content[6][1].lifestyle_modifications,
                        ];
                        updatedLifestyleMods[index] = e.target.value;
                        handleContentChange(
                          6,
                          "lifestyle_modifications",
                          updatedLifestyleMods
                        );
                      }}
                    />
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Precautions:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[6][1]?.precautions.length > 0 &&
                content[6][1]?.precautions.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedPrecautions = [
                          ...content[6][1].precautions,
                        ];
                        updatedPrecautions[index] = e.target.value;
                        handleContentChange(
                          6,
                          "precautions",
                          updatedPrecautions
                        );
                      }}
                    />
                  </ListItem>
                ))}
            </List>
            <Typography gutterBottom>Referrals:</Typography>
            <List sx={{ listStyleType: "circle", pl: 4 }}>
              {content[6][1]?.referrals.length > 0 &&
                content[6][1]?.referrals.map((item, index) => (
                  <ListItem key={index} sx={{ display: "list-item" }}>
                    <TextField
                      fullWidth
                      value={item}
                      onChange={(e) => {
                        const updatedReferrals = [...content[6][1].referrals];
                        updatedReferrals[index] = e.target.value;
                        handleContentChange(6, "referrals", updatedReferrals);
                      }}
                    />
                  </ListItem>
                ))}
            </List>
          </List>
          <hr />
          <Typography variant="h6" gutterBottom>
            <NotesIcon /> <strong>Additional Notes</strong>
          </Typography>
          <TextareaAutosize
            minRows={3}
            style={{ width: "100%" }}
            value={content[8][1]?.content}
            onChange={(e) => handleContentChange(8, "content", e.target.value)}
          />
          <hr />
        </DialogContent>
        <DialogActions>
          <Button autoFocus onClick={handleClose}>
            Save changes
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}
