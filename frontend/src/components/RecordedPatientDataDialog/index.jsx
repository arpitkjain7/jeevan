import * as React from "react";
import Button from "@mui/material/Button";
import { alpha, styled } from "@mui/material/styles";
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
import {
  Chip,
  FormControl,
  InputBase,
  InputLabel,
  List,
  ListItem,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
} from "@mui/material";
import { useState } from "react";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import contentData from "../../components/RecorderComponent/content.json";
import Translate from "../Translate";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiPaper-root": {
    borderRadius: "15px",
    border: "5px solid ",
    minWidth: "50%",
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

const BootstrapInput = styled(InputBase)(({ theme }) => ({
  "label + &": {
    marginTop: theme.spacing(6),
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

export default function CustomizedSummaryDialog({
  open,
  setOpen,
  summaryContent,
  setSummaryContent,
  translatedContent,
  setTranslatedContent,
}) {
  const [edit, setEdit] = useState(false);
  const handleClickOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const [newMedication, setNewMedication] = useState({
    med_name: "",
    instructions: "",
    dosages: "",
    duration_refill: "",
  });

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

  const handleMedicationInputChange = (e, field) => {
    setNewMedication({ ...newMedication, [field]: e.target.value });
  };

  const handleDeleteMedication = (medNameToDelete) => {
    setSummaryContent((prevContent) => {
      const updatedContent = [...prevContent];
      const medicationsIndex = 7; // Assuming the medications are at index 7
      const medicationList =
        updatedContent[medicationsIndex][1]?.medications || [];

      // Filter out the medication to delete
      const filteredMedications = medicationList.filter(
        (medication) => medication.med_name !== medNameToDelete
      );

      // Update the medications array
      updatedContent[medicationsIndex][1].medications = filteredMedications;

      return updatedContent;
    });
  };

  const handleAddMedication = () => {
    if (
      newMedication.med_name &&
      newMedication.instructions &&
      newMedication.dosages &&
      newMedication.duration_refill
    ) {
      // Create a new medication object from the input fields
      const medicationToAdd = { ...newMedication };

      // Update the summaryContent state with the new medication
      setSummaryContent((prevContent) => {
        // Clone the previous state to avoid direct mutation
        const updatedContent = [...prevContent];

        // Assuming summaryContent[7][1]?.medications is the array you're updating
        // Check if the medications array exists, if not, initialize it
        if (!updatedContent[7][1]?.medications) {
          updatedContent[7][1] = { medications: [] };
        }

        // Add the new medication to the medications array
        updatedContent[7][1].medications.push(medicationToAdd);

        // Return the updated state
        return updatedContent;
      });

      // Reset the newMedication input fields
      setNewMedication({
        med_name: "",
        instructions: "",
        dosages: "",
        duration_refill: "",
      });
    } else {
      // Optionally handle the case where some fields are empty
      console.log("Please fill in all fields.");
    }
  };

  const [isEditing, setIsEditing] = useState(false);
  const [editingMedName, setEditingMedName] = useState("");

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
      instructions: "",
      dosages: "",
      duration_refill: "",
    });
  };

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
          <FormControl variant="standard" fullWidth>
            <InputLabel shrink htmlFor="bootstrap-input">
              <Typography variant="h6">
                <strong>Consultation Summary</strong>
              </Typography>
            </InputLabel>
            <BootstrapInput
              disabled={!edit}
              defaultValue={summaryContent[0][1]?.summary}
              id="bootstrap-input"
              name="summary"
              multiline
              onChange={(e) => handleSummaryChange(e, 0)}
            />
          </FormControl>

          <Typography gutterBottom></Typography>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <AllergyIcon /> <strong>Subjective</strong>
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
                    summaryContent[1][1]?.chief_complaint || "Not Available"
                  }
                  id="bootstrap-input"
                  multiline
                  name="chief_complaint"
                  onChange={(e) => handleSummaryChange(e, 1)}
                />
              </FormControl>

              {summaryContent[1][1]?.allergy_information.length > 0 && (
                <div>
                  <Typography gutterBottom>Allergies:</Typography>
                  <Stack direction="row" spacing={1}>
                    {summaryContent[1][1]?.allergy_information.map(
                      (item, index) => (
                        <Chip key={index} label={item} />
                      )
                    )}
                  </Stack>
                </div>
              )}
              {summaryContent[1][1]?.family_history.length > 0 && (
                <div>
                  <Typography gutterBottom>Family History:</Typography>
                  <List sx={{ listStyleType: "circle", pl: 4 }}>
                    {summaryContent[1][1]?.family_history.map((item, index) => (
                      <ListItem key={index} sx={{ display: "list-item" }}>
                        {item}
                      </ListItem>
                    ))}
                  </List>
                </div>
              )}
              {summaryContent[1][1]?.history_of_present_illness.length > 0 && (
                <div>
                  <Typography gutterBottom>
                    History of Present Illness:
                  </Typography>
                  <List sx={{ listStyleType: "circle", pl: 4 }}>
                    {summaryContent[1][1]?.history_of_present_illness.map(
                      (item, index) => (
                        <ListItem key={index} sx={{ display: "list-item" }}>
                          {item}
                        </ListItem>
                      )
                    )}
                  </List>
                </div>
              )}
              {summaryContent[1][1]?.medication_history.length > 0 && (
                <div>
                  <Typography gutterBottom>Medication History:</Typography>
                  <List sx={{ listStyleType: "circle", pl: 4 }}>
                    {summaryContent[1][1]?.medication_history.map(
                      (item, index) => (
                        <ListItem key={index} sx={{ display: "list-item" }}>
                          {item}
                        </ListItem>
                      )
                    )}
                  </List>
                </div>
              )}
              {summaryContent[1][1]?.past_medical_history.length > 0 && (
                <div>
                  <Typography gutterBottom>Past Medical History:</Typography>
                  <List sx={{ listStyleType: "circle", pl: 4 }}>
                    {summaryContent[1][1]?.past_medical_history.map(
                      (item, index) => (
                        <ListItem key={index} sx={{ display: "list-item" }}>
                          {item}
                        </ListItem>
                      )
                    )}
                  </List>
                </div>
              )}
              {summaryContent[1][1]?.review_of_systems.length > 0 && (
                <div>
                  <Typography gutterBottom>Review of Systems:</Typography>
                  <List sx={{ listStyleType: "circle", pl: 4 }}>
                    {summaryContent[1][1]?.review_of_systems.map(
                      (item, index) => (
                        <ListItem key={index} sx={{ display: "list-item" }}>
                          {item}
                        </ListItem>
                      )
                    )}
                  </List>
                </div>
              )}
              {summaryContent[1][1]?.social_history.length > 0 && (
                <div>
                  <Typography gutterBottom>Social History:</Typography>
                  <List sx={{ listStyleType: "circle", pl: 4 }}>
                    {summaryContent[1][1]?.social_history.map((item, index) => (
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
              <FormControl variant="standard" fullWidth>
                <InputLabel shrink htmlFor="bootstrap-input">
                  <Typography variant="h6">
                    <strong> comment: </strong>
                  </Typography>
                </InputLabel>
                <BootstrapInput
                  disabled={!edit}
                  defaultValue={
                    summaryContent[3][1]?.comment || "Not Available"
                  }
                  id="bootstrap-input"
                  multiline
                  name="comment"
                  onChange={(e) => handleSummaryChange(e, 3)}
                />
              </FormControl>
              <FormControl variant="standard" fullWidth>
                <InputLabel shrink htmlFor="bootstrap-input">
                  <Typography variant="h6">
                    <strong>Differential Diagnosis:</strong>{" "}
                  </Typography>
                </InputLabel>
                <BootstrapInput
                  disabled={!edit}
                  defaultValue={
                    summaryContent[3][1]?.differential_diagnosis ||
                    "Not Available"
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
                    summaryContent[3][1]?.preliminary_diagnosis ||
                    "Not Available"
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
                    summaryContent[3][1]?.risk_factors || "Not Available"
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
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <PlanIcon /> <strong>Plans</strong>
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
                    summaryContent[4][1]?.diagnostic_plan || "Not Available"
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
                    summaryContent[4][1]?.treatment_plan || "Not Available"
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
                    <strong>Follow Up:</strong>{" "}
                  </Typography>
                </InputLabel>
                <BootstrapInput
                  disabled={!edit}
                  defaultValue={
                    summaryContent[4][1]?.follow_up || "Not Available"
                  }
                  id="bootstrap-input"
                  multiline
                  name="follow_up"
                  onChange={(e) => handleSummaryChange(e, 4)}
                />
              </FormControl>
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <PrescriptionIcon /> <strong>Prescription</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <FormControl variant="standard" fullWidth>
                <InputLabel shrink htmlFor="bootstrap-input">
                  <Typography variant="h6">
                    <strong>Comment:</strong>{" "}
                  </Typography>
                </InputLabel>
                <BootstrapInput
                  disabled={!edit}
                  defaultValue={
                    summaryContent[7][1]?.comment || "Not Available"
                  }
                  id="bootstrap-input"
                  multiline
                  name="comment"
                  onChange={(e) => handleSummaryChange(e, 7)}
                />
              </FormControl>
              <Typography variant="h7">
                <strong>Medications:</strong>{" "}
              </Typography>
              <TableContainer>
                <Table sx={{ minWidth: 650 }} aria-label="medications table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Medication Name</TableCell>
                      <TableCell align="right">Instructions</TableCell>
                      <TableCell align="right">Dosages</TableCell>
                      <TableCell align="right">Duration/Refill</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {summaryContent[7][1]?.medications?.map((medication) => (
                      <TableRow
                        key={medication.med_name}
                        sx={{
                          "&:last-child td, &:last-child th": { border: 0 },
                        }}
                      >
                        <TableCell component="th" scope="row">
                          {medication.med_name}
                        </TableCell>
                        <TableCell align="right">
                          {medication.instructions}
                        </TableCell>
                        <TableCell align="right">
                          {medication.dosages}
                        </TableCell>
                        <TableCell align="right">
                          {medication.duration_refill}
                        </TableCell>
                        {edit && (
                          <TableCell>
                            <button
                              onClick={() =>
                                handleDeleteMedication(medication.med_name)
                              }
                            >
                              Delete
                            </button>
                            <button
                              onClick={() => startEditMedication(medication)}
                            >
                              Edit
                            </button>
                          </TableCell>
                        )}
                      </TableRow>
                    ))}
                    {edit && (
                      <TableRow>
                        <TableCell component="th" scope="row">
                          <TextField
                            value={newMedication.med_name}
                            onChange={(e) =>
                              handleMedicationInputChange(e, "med_name")
                            }
                          />
                        </TableCell>
                        <TableCell align="right">
                          <TextField
                            value={newMedication.instructions}
                            onChange={(e) =>
                              handleMedicationInputChange(e, "instructions")
                            }
                          />
                        </TableCell>
                        <TableCell align="right">
                          <TextField
                            value={newMedication.dosages}
                            onChange={(e) =>
                              handleMedicationInputChange(e, "dosages")
                            }
                          />
                        </TableCell>
                        <TableCell align="right">
                          <TextField
                            value={newMedication.duration_refill}
                            onChange={(e) =>
                              handleMedicationInputChange(e, "duration_refill")
                            }
                          />
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </Table>
                {edit &&
                  (!isEditing ? (
                    <Button onClick={handleAddMedication}>
                      Add Medication
                    </Button>
                  ) : (
                    <Button onClick={saveEditedMedication}>
                      Save Edited Medication
                    </Button>
                  ))}
              </TableContainer>
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
                  {summaryContent[5][1]?.imaging_tests?.length > 0 &&
                    summaryContent[5][1]?.imaging_tests?.map((item, index) => (
                      <ListItem key={index} sx={{ display: "list-item" }}>
                        {item}
                      </ListItem>
                    ))}
                </List>
                <Typography gutterBottom>Laboratory Tests:</Typography>
                <List sx={{ listStyleType: "circle", pl: 4 }}>
                  {summaryContent[5][1]?.laboratory_tests?.length > 0 &&
                    summaryContent[5][1]?.laboratory_tests?.map(
                      (item, index) => (
                        <ListItem key={index} sx={{ display: "list-item" }}>
                          {item}
                        </ListItem>
                      )
                    )}
                </List>
                <Typography gutterBottom>Special Exams:</Typography>
                <List sx={{ listStyleType: "circle", pl: 4 }}>
                  {summaryContent[5][1]?.special_exams?.length > 0 &&
                    summaryContent[5][1]?.special_exams?.map((item, index) => (
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
                  {summaryContent[6][1]?.consultations.length > 0 &&
                    summaryContent[6][1]?.consultations.map((item, index) => (
                      <ListItem key={index} sx={{ display: "list-item" }}>
                        {item}
                      </ListItem>
                    ))}
                </List>
                <Typography gutterBottom>Lifestyle Modifications:</Typography>
                <List sx={{ listStyleType: "circle", pl: 4 }}>
                  {summaryContent[6][1]?.lifestyle_modifications.length > 0 &&
                    summaryContent[6][1]?.lifestyle_modifications.map(
                      (item, index) => (
                        <ListItem key={index} sx={{ display: "list-item" }}>
                          {item}
                        </ListItem>
                      )
                    )}
                </List>
                <Typography gutterBottom>Precautions:</Typography>
                <List sx={{ listStyleType: "circle", pl: 4 }}>
                  {summaryContent[6][1]?.precautions.length > 0 &&
                    summaryContent[6][1]?.precautions.map((item, index) => (
                      <ListItem key={index} sx={{ display: "list-item" }}>
                        {item}
                      </ListItem>
                    ))}
                </List>
                <Typography gutterBottom>Referrals:</Typography>
                <List sx={{ listStyleType: "circle", pl: 4 }}>
                  {summaryContent[6][1]?.referrals.length > 0 &&
                    summaryContent[6][1]?.referrals.map((item, index) => (
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
              <FormControl variant="standard" fullWidth>
                <BootstrapInput
                  disabled={!edit}
                  defaultValue={
                    summaryContent[8][1]?.content || "Not Available"
                  }
                  id="bootstrap-input"
                  multiline
                  name="content"
                  onChange={(e) => handleSummaryChange(e, 8)}
                />
              </FormControl>
            </AccordionDetails>
          </Accordion>
        </DialogContent>
        <DialogActions>
          <Translate />
          <Button autoFocus onClick={() => setEdit(!edit)}>
            Edit
          </Button>
        </DialogActions>
      </BootstrapDialog>
    </React.Fragment>
  );
}
