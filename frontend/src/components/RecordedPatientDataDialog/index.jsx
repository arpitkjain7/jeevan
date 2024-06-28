import * as React from "react";
import { useState } from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import CloseIcon from "@mui/icons-material/Close";
import Slide from "@mui/material/Slide";
import AspectRatioIcon from "@mui/icons-material/AspectRatio";
import AllergyIcon from "@mui/icons-material/HealthAndSafety";
import AssessmentIcon from "@mui/icons-material/Assignment";
import PlanIcon from "@mui/icons-material/FactCheck";
import PrescriptionIcon from "@mui/icons-material/Description";
import TestIcon from "@mui/icons-material/Biotech";
import NextStepsIcon from "@mui/icons-material/Forward";
import NotesIcon from "@mui/icons-material/Notes";
import {
  Autocomplete,
  Chip,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputBase,
  InputLabel,
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
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { alpha, styled } from "@mui/material/styles";
import contentData from "../../components/RecorderComponent/content.json";
import Translate from "../Translate";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});
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
  const handleClickOpen = () => {
    setOpen(true);
  };
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

  const handleChipChange = (e, index, newValue, sectionName) => {
    // e.prevent.default();
    console.log(sectionName);
    setSummaryContent((prevContent) => {
      const newContent = [...prevContent];
      if (newContent[index] && newContent[index][1]) {
        newContent[index][1][sectionName] = newValue;
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
      <Dialog
        fullScreen
        open={open}
        onClose={handleClose}
        TransitionComponent={Transition}
      >
        <AppBar sx={{ position: "relative", backgroundColor: "#f8f8f8" }}>
          <Toolbar>
            <DialogTitle
              sx={{ m: 0, p: 2, display: "flex", flex: 1 }}
              id="customized-dialog-title"
            >
              <Stack
                justifyContent={"center"}
                alignItems={"center"}
                sx={{
                  backgroundColor: "#0089E9",
                  width: "130px",
                  padding: "5px",
                }}
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
              edge="start"
              color="inherit"
              onClick={handleClose}
              aria-label="close"
            >
              <CloseIcon sx={{ color: "#0089E9" }} />
            </IconButton>
          </Toolbar>
        </AppBar>
        <DialogContent dividers>
          <FormControl variant="standard" fullWidth>
            <InputLabel shrink htmlFor="bootstrap-input">
              <Typography variant="h6">
                <strong>Consultation Summary</strong>
              </Typography>
            </InputLabel>
            <BootstrapInput
              disabled={!edit}
              defaultValue={summaryContent?.[0]?.[1]?.summary}
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
                <>
                  <Typography gutterBottom>Allergy Information:</Typography>
                  <Autocomplete
                    multiple
                    freeSolo
                    name="allergy_information"
                    onChange={(e, newValue) =>
                      handleChipChange(e, 1, newValue, "allergy_information")
                    }
                    id="tags-filled"
                    options={[]}
                    defaultValue={
                      summaryContent[1][1]?.allergy_information || []
                    }
                    renderTags={(value, getTagProps) =>
                      value.map((item, index) => {
                        const { key, ...tagProps } = getTagProps({ index });
                        return (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={key}
                            {...tagProps}
                          />
                        );
                      })
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        placeholder="allergies"
                      />
                    )}
                  />
                </>
              )}

              {summaryContent[1][1]?.family_history.length > 0 && (
                <div>
                  <Typography gutterBottom>Family History:</Typography>
                  <Autocomplete
                    multiple
                    freeSolo
                    name="family_history"
                    onChange={(e, newValue) =>
                      handleChipChange(e, 1, newValue, "family_history")
                    }
                    id="tags-filled"
                    options={[]}
                    defaultValue={summaryContent[1][1]?.family_history || []}
                    renderTags={(value, getTagProps) =>
                      value.map((item, index) => {
                        const { key, ...tagProps } = getTagProps({ index });
                        return (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={key}
                            {...tagProps}
                          />
                        );
                      })
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        placeholder="Family History"
                      />
                    )}
                  />
                </div>
              )}
              {summaryContent[1][1]?.history_of_present_illness.length > 0 && (
                <div>
                  <Typography gutterBottom>
                    History of Present Illness:
                  </Typography>
                  <Autocomplete
                    multiple
                    freeSolo
                    name="history_of_present_illness"
                    onChange={(e, newValue) =>
                      handleChipChange(
                        e,
                        1,
                        newValue,
                        "history_of_present_illness"
                      )
                    }
                    id="tags-filled"
                    options={[]}
                    defaultValue={
                      summaryContent[1][1]?.history_of_present_illness || []
                    }
                    renderTags={(value, getTagProps) =>
                      value.map((item, index) => {
                        const { key, ...tagProps } = getTagProps({ index });
                        return (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={key}
                            {...tagProps}
                          />
                        );
                      })
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        placeholder=" History of Illness"
                      />
                    )}
                  />
                </div>
              )}
              {summaryContent[1][1]?.medication_history.length > 0 && (
                <div>
                  <Typography gutterBottom>Medication History:</Typography>
                  <Autocomplete
                    multiple
                    freeSolo
                    name="medication_history"
                    onChange={(e, newValue) =>
                      handleChipChange(e, 1, newValue, "medication_history")
                    }
                    id="tags-filled"
                    options={[]}
                    defaultValue={
                      summaryContent[1][1]?.medication_history || []
                    }
                    renderTags={(value, getTagProps) =>
                      value.map((item, index) => {
                        const { key, ...tagProps } = getTagProps({ index });
                        return (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={key}
                            {...tagProps}
                          />
                        );
                      })
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        placeholder=" Medical History"
                      />
                    )}
                  />
                </div>
              )}
              {summaryContent[1][1]?.past_medical_history.length > 0 && (
                <div>
                  <Typography gutterBottom>Past Medical History:</Typography>
                  <Autocomplete
                    multiple
                    freeSolo
                    name="past_medical_history"
                    onChange={(e, newValue) =>
                      handleChipChange(e, 1, newValue, "past_medical_history")
                    }
                    id="tags-filled"
                    options={[]}
                    defaultValue={
                      summaryContent[1][1]?.past_medical_history || []
                    }
                    renderTags={(value, getTagProps) =>
                      value.map((item, index) => {
                        const { key, ...tagProps } = getTagProps({ index });
                        return (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={key}
                            {...tagProps}
                          />
                        );
                      })
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        placeholder=" Past Medical History"
                      />
                    )}
                  />
                </div>
              )}
              {summaryContent[1][1]?.review_of_systems.length > 0 && (
                <div>
                  <Typography gutterBottom>Review of Systems:</Typography>
                  <Autocomplete
                    multiple
                    freeSolo
                    name="review_of_systems"
                    onChange={(e, newValue) =>
                      handleChipChange(e, 1, newValue, "review_of_systems")
                    }
                    id="tags-filled"
                    options={[]}
                    defaultValue={summaryContent[1][1]?.review_of_systems || []}
                    renderTags={(value, getTagProps) =>
                      value.map((item, index) => {
                        const { key, ...tagProps } = getTagProps({ index });
                        return (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={key}
                            {...tagProps}
                          />
                        );
                      })
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        placeholder="Reviews of System"
                      />
                    )}
                  />
                </div>
              )}
              {summaryContent[1][1]?.social_history.length > 0 && (
                <div>
                  <Typography gutterBottom>Social History:</Typography>
                  <Autocomplete
                    multiple
                    freeSolo
                    name="social_history"
                    onChange={(e, newValue) =>
                      handleChipChange(e, 1, newValue, "social_history")
                    }
                    id="tags-filled"
                    options={[]}
                    defaultValue={summaryContent[1][1]?.social_history || []}
                    renderTags={(value, getTagProps) =>
                      value.map((item, index) => {
                        const { key, ...tagProps } = getTagProps({ index });
                        return (
                          <Chip
                            variant="outlined"
                            label={item}
                            key={key}
                            {...tagProps}
                          />
                        );
                      })
                    }
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        placeholder="Social History"
                      />
                    )}
                  />
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
              <>
                {summaryContent[5][1]?.imaging_tests?.length > 0 && (
                  <div>
                    <Typography gutterBottom>Imaging Tests:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      name="imaging_tests"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 5, newValue, "imaging_tests")
                      }
                      id="tags-filled"
                      options={[]}
                      defaultValue={summaryContent[5][1]?.imaging_tests || []}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => {
                          const { key, ...tagProps } = getTagProps({ index });
                          return (
                            <Chip
                              variant="outlined"
                              label={item}
                              key={key}
                              {...tagProps}
                            />
                          );
                        })
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Imaging Test"
                        />
                      )}
                    />
                  </div>
                )}
                {summaryContent[5][1]?.laboratory_tests?.length > 0 && (
                  <div>
                    <Typography gutterBottom>Laboratory Tests:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      name="laboratory_tests"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 5, newValue, "laboratory_tests")
                      }
                      id="tags-filled"
                      options={[]}
                      defaultValue={
                        summaryContent[5][1]?.laboratory_tests || []
                      }
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => {
                          const { key, ...tagProps } = getTagProps({ index });
                          return (
                            <Chip
                              variant="outlined"
                              label={item}
                              key={key}
                              {...tagProps}
                            />
                          );
                        })
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Laboratory Test"
                        />
                      )}
                    />
                  </div>
                )}
                {summaryContent[5][1]?.special_exams?.length > 0 && (
                  <div>
                    <Typography gutterBottom>Special Exams:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      name="special_exams"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 5, newValue, "special_exams")
                      }
                      id="tags-filled"
                      options={[]}
                      defaultValue={summaryContent[5][1]?.special_exams || []}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => {
                          const { key, ...tagProps } = getTagProps({ index });
                          return (
                            <Chip
                              variant="outlined"
                              label={item}
                              key={key}
                              {...tagProps}
                            />
                          );
                        })
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Special Exams"
                        />
                      )}
                    />
                  </div>
                )}
              </>
            </AccordionDetails>
          </Accordion>
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">
                <NextStepsIcon /> <strong>Other Next Steps</strong>
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <>
                {summaryContent[6][1]?.consultations.length > 0 && (
                  <div>
                    <Typography gutterBottom>Consultations:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      name="consultations"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 6, newValue, "consultations")
                      }
                      id="tags-filled"
                      options={[]}
                      defaultValue={summaryContent[6][1]?.consultations || []}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => {
                          const { key, ...tagProps } = getTagProps({ index });
                          return (
                            <Chip
                              variant="outlined"
                              label={item}
                              key={key}
                              {...tagProps}
                            />
                          );
                        })
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Consulation"
                        />
                      )}
                    />
                  </div>
                )}
                {summaryContent[6][1]?.lifestyle_modifications.length > 0 && (
                  <div>
                    <Typography gutterBottom>
                      Lifestyle Modifications:
                    </Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      name="lifestyle_modifications"
                      onChange={(e, newValue) =>
                        handleChipChange(
                          e,
                          6,
                          newValue,
                          "lifestyle_modifications"
                        )
                      }
                      id="tags-filled"
                      options={[]}
                      defaultValue={
                        summaryContent[6][1]?.lifestyle_modifications || []
                      }
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => {
                          const { key, ...tagProps } = getTagProps({ index });
                          return (
                            <Chip
                              variant="outlined"
                              label={item}
                              key={key}
                              {...tagProps}
                            />
                          );
                        })
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Lifestyle Modifications"
                        />
                      )}
                    />
                  </div>
                )}
                {summaryContent[6][1]?.precautions.length > 0 && (
                  <div>
                    <Typography gutterBottom>Precautions:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      name="precautions"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 6, newValue, "precautions")
                      }
                      id="tags-filled"
                      options={[]}
                      defaultValue={summaryContent[6][1]?.precautions || []}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => {
                          const { key, ...tagProps } = getTagProps({ index });
                          return (
                            <Chip
                              variant="outlined"
                              label={item}
                              key={key}
                              {...tagProps}
                            />
                          );
                        })
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Precautions"
                        />
                      )}
                    />
                  </div>
                )}
                {summaryContent[6][1]?.referrals.length > 0 && (
                  <div>
                    <Typography gutterBottom>Referrals:</Typography>
                    <Autocomplete
                      multiple
                      freeSolo
                      name="referrals"
                      onChange={(e, newValue) =>
                        handleChipChange(e, 6, newValue, "referrals")
                      }
                      id="tags-filled"
                      options={[]}
                      defaultValue={summaryContent[6][1]?.referrals || []}
                      renderTags={(value, getTagProps) =>
                        value.map((item, index) => {
                          const { key, ...tagProps } = getTagProps({ index });
                          return (
                            <Chip
                              variant="outlined"
                              label={item}
                              key={key}
                              {...tagProps}
                            />
                          );
                        })
                      }
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          variant="outlined"
                          placeholder="Precautions"
                        />
                      )}
                    />
                  </div>
                )}
              </>
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
          <Button autoFocus variant="contained">
            Review Priscription
          </Button>
          <Translate
            translatedContent={translatedContent}
            setTranslatedContent={setTranslatedContent}
            setOpen={setOpen}
          />
          <Button autoFocus onClick={() => setEdit(!edit)}>
            Edit
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}
