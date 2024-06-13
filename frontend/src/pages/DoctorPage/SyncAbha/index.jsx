import {
  FormControl,
  FormControlLabel,
  Modal,
  RadioGroup,
  styled,
  Box,
  Button,
  Radio,
  Typography,
  Dialog,
  DialogTitle,
  IconButton,
  DialogContent, // Added Typography
  DialogActions,
  TextField,
  Grid,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import {
  getPatientAuth,
  syncPMR,
  verifyPatientOTP,
} from "../EMRPage/EMRPage.slice";
import OtpInput from "../../../components/OTPValidation";
import { useNavigate } from "react-router-dom";
import CustomLoader from "../../../components/CustomLoader";

const StyledModalBox = styled(Box)(({ theme }) => ({
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "60%",
  background: "#ffffff",
  padding: theme.spacing(8),
  borderRadius: theme.spacing(1),
  boxShadow: 24,
  p: 4,
}));

const PrimaryButton = styled("Button")(({ theme }) => ({
  "&": theme.typography.primaryButton,
}));

const PageTitle = styled(Typography)(({ theme }) => ({
  "&": theme.typography.h1,
  marginBottom: theme.spacing(8),
}));
const PageSubText = styled(Typography)(({ theme }) => ({
  "&": theme.typography.h2,
  marginBottom: theme.spacing(2),
}));
const ModalFooter = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
}));
const SecondaryButton = styled("Button")(({ theme }) => ({
  "&": theme.typography.secondaryButton,
}));

const OTPWrapper = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
}));

const SyncAbha = ({
  showSync,
  handleModalClose,
  // selectedAuthOption,
  // setSelectedAuthOption,
}) => {
  const [selectedAuthOption, setSelectedAuthOption] = useState("");
  const [options, setOptions] = useState([]);
  const dispatch = useDispatch();
  const currentPatient = JSON.parse(sessionStorage.getItem("selectedPatient"));
  const [txnId, setTxnId] = useState("");
  const [authData, setAuthData] = useState({});
  const [btnDisable, setBtnDisable] = useState(true);
  const [demographics, setDemographics] = useState(false);
  const [showLoader, setShowLoader] = useState(false);
  const [openConfirmationDialog, setOpenConfirmationDialog] = useState(false);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (
      (currentPatient?.patient_details?.abha_number ||
        currentPatient?.abha_number) !== "" &&
      (currentPatient?.patient_details?.auth_methods ||
        currentPatient?.auth_methods)
    ) {
      const methods =
        currentPatient?.patient_details?.auth_methods ||
        currentPatient?.auth_methods;
      setOptions(methods?.authMethods);
    }
  }, []);

  const handleAuthChange = (event) => {
    setShowLoader(true);
    setSelectedAuthOption(event.target.value);
    const payload = {
      patient_id: currentPatient?.id,
      purpose: "KYC_AND_LINK",
      auth_mode: event.target.value,
    };
    dispatch(getPatientAuth(payload)).then((res) => {
      setShowLoader(false);
      setTxnId(res.payload?.txn_id);
      if (event.target.value === "DEMOGRAPHICS") {
        setTxnId("");
        setDemographics(true);
      } else setDemographics(false);
    });
  };

  const clearData = () => {
    setBtnDisable(true);
    setTxnId("");
    setSelectedAuthOption("");
  };
  const verifyOTP = (value) => {
    const verifyPayload = {
      txnId: txnId,
      otp: value,
    };
    dispatch(verifyPatientOTP(verifyPayload)).then((res) => {
      setAuthData(res.payload);
      setBtnDisable(false);
    });
  };

  const onSync = () => {
    const payload = {
      hip_id: currentPatient?.patient_details?.hip_id || currentPatient?.hip_id,
      pmr_id: sessionStorage.getItem("pmrID"),
    };
    dispatch(syncPMR(payload)).then((res) => {
      if (res?.payload?.status === "success") {
        setMessage("PMR Synced Successfully");
        // handleModalClose();
        // sessionStorage.removeItem("pmrId");
        // navigate("/appointment-list");
      } else {
        setMessage("PMR Sync Failed");
      }
      setOpenConfirmationDialog(true);
    });
  };
  const handleCloseConfirmationDialog = () => {
    setOpenConfirmationDialog(false);
  };
  const handleDialogAction = () => {
    handleModalClose();
    sessionStorage.removeItem("pmrId");
    navigate("/appointment-list");
  };
  return (
    <>
      <CustomLoader open={showLoader} />
      <Dialog
        open={showSync}
        onClose={handleModalClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
        fullWidth={true}
        maxWidth={"sm"}
      >
        <DialogTitle>Sync ABHA</DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleModalClose}
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
          <FormControl component="fieldset">
            <PageSubText>Select an authentication method</PageSubText>
            <RadioGroup
              row
              aria-label="options"
              name="authMethods"
              value={selectedAuthOption}
              onChange={handleAuthChange}
            >
              {options?.map((option, index) => (
                <FormControlLabel
                  key={index}
                  value={option}
                  control={<Radio />}
                  label={option?.replace("_", " ")}
                />
              ))}
            </RadioGroup>
          </FormControl>
          {!demographics && (
            <>
              <OTPWrapper>
                {txnId !== "" && (
                  <OtpInput verifyOTP={verifyOTP} isSync={true} />
                )}
              </OTPWrapper>
              <br />
            </>
          )}
          {/* {demographics && ( */}
          <Grid container spacing={2} style={{ marginTop: "5px" }}>
            <Grid item xs={6}>
              <TextField
                label="Name"
                name="name"
                value={
                  currentPatient?.patient_details?.name || currentPatient?.name
                }
                disabled
                InputLabelProps={{ shrink: true }}
                fullWidth
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="ABHA number"
                name="abhaNumber"
                value={
                  currentPatient?.patient_details?.abha_number ||
                  currentPatient?.abha_number
                }
                disabled
                InputLabelProps={{ shrink: true }}
                fullWidth
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="ABHA Address"
                name="abhaNumber"
                value={
                  currentPatient?.patient_details?.abha_address ||
                  currentPatient?.abha_address
                }
                disabled
                InputLabelProps={{ shrink: true }}
                fullWidth
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="Mobile"
                name="mobile"
                value={
                  currentPatient?.patient_details?.mobile_number ||
                  currentPatient?.mobile_number
                }
                disabled
                InputLabelProps={{ shrink: true }}
                fullWidth
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="DOB"
                name="dob"
                value={
                  currentPatient?.patient_details?.DOB || currentPatient?.DOB
                }
                disabled
                InputLabelProps={{ shrink: true }}
                fullWidth
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                label="Gender"
                name="gender"
                value={
                  currentPatient?.patient_details?.gender ||
                  currentPatient?.gender
                }
                disabled
                InputLabelProps={{ shrink: true }}
                fullWidth
              />
            </Grid>
          </Grid>
          {/* )} */}
        </DialogContent>
        <DialogActions>
          <SecondaryButton onClick={clearData}>Clear</SecondaryButton>
          <PrimaryButton onClick={onSync}>Sync PMR</PrimaryButton>
        </DialogActions>
      </Dialog>
      <Dialog
        onClose={handleCloseConfirmationDialog}
        open={openConfirmationDialog}
        fullWidth={true}
        maxWidth={"sm"}
      >
        <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
          Sync PMR
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleCloseConfirmationDialog}
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
          <Typography gutterBottom>{message}</Typography>
        </DialogContent>
        <DialogActions>
          {message !== "PMR Synced Successfully" && (
            <Button onClick={handleCloseConfirmationDialog}>Cancel</Button>
          )}
          <Button autoFocus onClick={handleDialogAction}>
            OK
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default SyncAbha;
