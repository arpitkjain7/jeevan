import React, { useState } from "react";
import Modal from "@mui/material/Modal";
import {
  TextField,
  Select,
  MenuItem,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Typography,
  IconButton,
  Dialog,
  AppBar,
  Toolbar,
  Slide,
  Checkbox,
  ListItemText,
  OutlinedInput,
} from "@mui/material";
import { styled } from "@mui/material/styles";
import CloseIcon from "@mui/icons-material/Close";
import { Close } from "@mui/icons-material";
import { useDispatch } from "react-redux";
import {
  gatewayInteraction,
  postConsentRequest,
  searchAbha,
} from "../ConsentList/consentList.slice";
import { convertDateFormat } from "../../utils/utils";
import CustomSnackbar from "../CustomSnackbar";
import { render } from "@react-pdf/renderer";
import CustomLoader from "../CustomLoader";
import zIndex from "@mui/material/styles/zIndex";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const ModalContainer = styled("div")({
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  backgroundColor: "white",
  padding: "20px",
  borderRadius: "8px",
  outline: "none",
  width: "50%",
});

const Form = styled("form")({
  margin: "0 auto",
});

const FormRow = styled("div")({
  marginBottom: "20px",
});
const ModalTitle = styled(Typography)(({ theme }) => ({
  "&": theme.typography.h4,
  borderBottom: "1px solid #9e9e9e",
  padding: theme.spacing(2, 6),
  marginBottom: theme.spacing(4),
}));
const ModalFooter = styled("div")(({ theme }) => ({
  padding: theme.spacing(2, 6),
  display: "flex",
  justifyContent: "flex-end",
  alignItems: "center",
}));
const CustomButton = styled("button")(({ theme }) => ({
  "&": theme.typography.primaryButton,
}));

const FormLabel = styled(Typography)(({ theme }) => ({
  "&": theme.typography.body1,
}));

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const ConsentModal = ({
  open,
  handleClose,
  purposeOptions,
  infoTypeOptions,
  render,
  setRender,
}) => {
  const currentPatient = JSON.parse(sessionStorage?.getItem("selectedPatient"));
  const [hiTypes, setHiTypes] = useState([]);
  const [showLoader, setShowLoader] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [selectAllChecked, setSelectAllChecked] = useState(false);
  const [abhaUserName, setAbhaUserName] = useState("");
  const [isAbhaUserName, setIsAbhaUserName] = useState(false);
  const [requestId, setRequestId] = useState("");
  const [formData, setFormData] = useState({
    patientIdentifier: "",
    purposeOfRequest: "",
    healthInfoFromDate: "",
    healthInfoToDate: "",
    // healthInfoType: {},
    consentExpiryDate: "",
  });
  const hospital = sessionStorage?.getItem("selectedHospital");
  const dispatch = useDispatch();
  const isMobile = window.innerWidth < 600;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleAbhaName = (e) => {
    dispatch(searchAbha({ healthNumber: e.target.value })).then((response) => {
      if (response?.payload) {
        setIsAbhaUserName(true);
        setAbhaUserName(response?.payload?.name);
      } else {
        setIsAbhaUserName(false);
        setAbhaUserName("");
      }
    });
  };
  const handleSelectAll = () => {
    if (!selectAllChecked) {
      setHiTypes(infoTypeOptions); // Add all options
    } else {
      setHiTypes([]); // Deselect all options
    }
    setSelectAllChecked(!selectAllChecked);
  };

  const handleHealthInfoChange = (event) => {
    const {
      target: { value },
    } = event;
    if (value.includes("selectAll")) {
      handleSelectAll();
    } else {
      setHiTypes(
        // On autofill we get a stringified value.
        typeof value === "string" ? value.split(",") : value
      );
      setSelectAllChecked(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setShowLoader(true);
    if (hospital) {
      const currentHospital = JSON.parse(hospital);
      const payload = {
        patient_id: currentPatient?.patient_id || currentPatient?.id,
        abha_address: formData?.patientIdentifier,
        purpose: formData?.purposeOfRequest,
        hi_type: hiTypes, //[formData?.healthInfoType],
        date_from: formData?.healthInfoFromDate,
        date_to: formData?.healthInfoToDate,
        expiry: convertDateFormat(
          formData?.consentExpiryDate,
          "yyyy-MM-dd HH:mm:SS"
        ),
        hip_id: currentHospital?.hip_id,
        doc_id: "1",
      };
      dispatch(postConsentRequest(payload)).then((res) => {
        setShowLoader(true);
        if (res?.error && Object.keys(res?.error)?.length > 0) {
          setErrorMessage(res?.detail?.error_message);
          setShowSnackbar(true);
          return;
        }
        setRequestId(res?.payload?.request_id);
        setHiTypes([]);
     
      const checkConsentStatus = () => {
        dispatch(gatewayInteraction(res?.payload?.request_id)).then((res) => {
          const consentStatus = res?.payload?.callback_response?.status;
          console.log("consentStatus", consentStatus);
          handleClose();
          if (consentStatus !== "PROCESSING") {
            setShowLoader(false);
            setRender(!render);
            setFormData({
              patientIdentifier: "",
              purposeOfRequest: "",
              healthInfoFromDate: "",
              healthInfoToDate: "",
              consentExpiryDate: "",
            });
          } else if (consentStatus === "PROCESSING") {
            setTimeout(checkConsentStatus, 3000);
          }
        });
      };
      setTimeout(checkConsentStatus, 3000);
    });
     
    }
  };

  const onSnackbarClose = () => {
    setShowSnackbar(false);
  };

  return (
    <>
      <CustomSnackbar
        message={errorMessage || "Something went wrong"}
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
      {!isMobile && (
        <Modal open={open} onClose={handleClose}>
          <ModalContainer sx={{ padding: "0" }}>
            <CustomLoader open={showLoader} />
            <ModalTitle
              component="div"
              id="modal-title"
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              Request Consent
              <IconButton onClick={handleClose}>
                <Close sx={{ width: "32px", height: "32px" }} />
              </IconButton>
            </ModalTitle>
            <Form onSubmit={handleSubmit} sx={{ padding: "24px" }}>
              <Grid container spacing={4} sx={{ marginBottom: "32px" }}>
                <Grid item xs={6}>
                  <FormLabel>Patient Identifier</FormLabel>
                  <TextField
                    placeholder="Patient Identifier"
                    fullWidth
                    name="patientIdentifier"
                    value={formData.patientIdentifier}
                    onChange={handleChange}
                    onBlur={handleAbhaName}
                  />
                  {formData.patientIdentifier && isAbhaUserName && (
                    <span>{abhaUserName}</span>
                  )}
                </Grid>
                <Grid item xs={6}>
                  <FormLabel>Purpose of request</FormLabel>
                  <FormControl fullWidth>
                    <Select
                      name="purposeOfRequest"
                      value={formData.purposeOfRequest}
                      onChange={handleChange}
                      placeholder="Select purpose"
                    >
                      {purposeOptions.map((option) => (
                        <MenuItem key={option.value} value={option.value}>
                          {option.label}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
              <Grid container spacing={4} sx={{ marginBottom: "32px" }}>
                <Grid item xs={6}>
                  <FormLabel>Health Info From</FormLabel>
                  <TextField
                    placeholder="Select from date"
                    fullWidth
                    type="date"
                    name="healthInfoFromDate"
                    value={formData.healthInfoFromDate}
                    onChange={handleChange}
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <FormLabel>Health Info To</FormLabel>
                  <TextField
                    fullWidth
                    type="date"
                    name="healthInfoToDate"
                    value={formData.healthInfoToDate}
                    onChange={handleChange}
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                </Grid>
              </Grid>
              <Grid container spacing={4} sx={{ marginBottom: "32px" }}>
                <Grid item xs={6}>
                  <FormLabel>Health Info Type</FormLabel>
                  <FormControl fullWidth>
                    <Select
                      name="healthInfoType"
                      multiple
                      value={hiTypes}
                      onChange={handleHealthInfoChange}
                      input={<OutlinedInput label="Tag" />}
                      renderValue={(selected) => selected.join(", ")}
                      MenuProps={MenuProps}
                    >
                      <MenuItem value="selectAll">
                        <Checkbox checked={selectAllChecked} />
                        <ListItemText primary={"Select All"} />
                      </MenuItem>
                      {infoTypeOptions.map((option) => (
                        <MenuItem key={option} value={option}>
                          <Checkbox checked={hiTypes.indexOf(option) > -1} />
                          <ListItemText primary={option} />
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={6}>
                  <FormLabel>Consent Expiry</FormLabel>
                  <TextField
                    fullWidth
                    type="datetime-local"
                    name="consentExpiryDate"
                    value={formData.consentExpiryDate}
                    onChange={handleChange}
                    InputLabelProps={{
                      shrink: true,
                    }}
                  />
                </Grid>
              </Grid>
              <ModalFooter>
                {" "}
                <CustomButton
                  disabled={
                    !(
                      formData?.patientIdentifier?.length &&
                      formData?.purposeOfRequest?.length &&
                      formData?.healthInfoFromDate?.length &&
                      formData?.healthInfoToDate?.length &&
                      // formData?.healthInfoType?.length &&
                      hiTypes &&
                      formData?.consentExpiryDate?.length
                    )
                  }
                  type="submit"
                >
                  Request Consent
                </CustomButton>
              </ModalFooter>
            </Form>
          </ModalContainer>
        </Modal>
      )}
      {isMobile && (
        <Dialog
          fullScreen
          open={open}
          onClose={handleClose}
          TransitionComponent={Transition}
        >
          <AppBar sx={{ position: "relative" }}>
            <Toolbar>
              <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
                Request Consent
              </Typography>
              <IconButton
                edge="start"
                color="inherit"
                onClick={handleClose}
                aria-label="close"
              >
                <CloseIcon />
              </IconButton>
            </Toolbar>
          </AppBar>

          <CustomLoader open={showLoader} />
          <Form onSubmit={handleSubmit} sx={{ padding: "24px" }}>
            <Grid container spacing={4} sx={{ marginBottom: "32px" }}>
              <Grid item xs={12} sm={6}>
                <FormLabel>Patient Identifier</FormLabel>
                <TextField
                  placeholder="Patient Identifier"
                  fullWidth
                  name="patientIdentifier"
                  value={formData.patientIdentifier}
                  onChange={handleChange}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormLabel>Purpose of request</FormLabel>
                <FormControl fullWidth>
                  <Select
                    name="purposeOfRequest"
                    value={formData.purposeOfRequest}
                    onChange={handleChange}
                    placeholder="Select purpose"
                  >
                    {purposeOptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            <Grid container spacing={4} sx={{ marginBottom: "32px" }}>
              <Grid item xs={12} sm={6}>
                <FormLabel>Health Info From</FormLabel>
                <TextField
                  placeholder="Select from date"
                  fullWidth
                  type="date"
                  name="healthInfoFromDate"
                  value={formData.healthInfoFromDate}
                  onChange={handleChange}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormLabel>Health Info To</FormLabel>
                <TextField
                  fullWidth
                  type="date"
                  name="healthInfoToDate"
                  value={formData.healthInfoToDate}
                  onChange={handleChange}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
            </Grid>
            <Grid container spacing={4} sx={{ marginBottom: "32px" }}>
              <Grid item xs={12} sm={6}>
                <FormLabel>Health Info Type</FormLabel>
                <FormControl sx={{ width: { xs: 480 } }}>
                  <Select
                    name="healthInfoType"
                    multiple
                    value={hiTypes}
                    onChange={handleHealthInfoChange}
                    input={<OutlinedInput label="Tag" />}
                    renderValue={(selected) => selected.join(", ")}
                    MenuProps={MenuProps}
                  >
                    <MenuItem value="selectAll">
                      <Checkbox checked={selectAllChecked} />
                      <ListItemText primary={"Select All"} />
                    </MenuItem>
                    {infoTypeOptions.map((option) => (
                      <MenuItem key={option} value={option}>
                        <Checkbox checked={hiTypes.indexOf(option) > -1} />
                        <ListItemText primary={option} />
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormLabel>Consent Expiry</FormLabel>
                <TextField
                  fullWidth
                  type="datetime-local"
                  name="consentExpiryDate"
                  value={formData.consentExpiryDate}
                  onChange={handleChange}
                  InputLabelProps={{
                    shrink: true,
                  }}
                />
              </Grid>
            </Grid>
            <ModalFooter>
              {" "}
              <CustomButton
                disabled={
                  !(
                    formData?.patientIdentifier?.length &&
                    formData?.purposeOfRequest?.length &&
                    formData?.healthInfoFromDate?.length &&
                    formData?.healthInfoToDate?.length &&
                    // formData?.healthInfoType?.length &&
                    hiTypes &&
                    formData?.consentExpiryDate?.length
                  )
                }
                type="submit"
              >
                Request Consent
              </CustomButton>
            </ModalFooter>
          </Form>
        </Dialog>
      )}
    </>
  );
};

export default ConsentModal;
