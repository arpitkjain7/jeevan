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
  DialogActions
} from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import {
  getPatientAuth,
  syncPMR,
  verifyPatientOTP,
} from "../EMRPage/EMRPage.slice";
import OtpInput from "../../../components/OTPValidation";
import { useNavigate } from "react-router-dom";

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
  marginTop: theme.spacing(8),
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
  const navigate = useNavigate();

  useEffect(() => {
    if (
      (currentPatient?.patient_details?.abha_number || currentPatient?.abha_number) !== "" &&
      (currentPatient?.patient_details?.auth_methods || currentPatient?.auth_methods)
    ) {
      const methods = currentPatient?.patient_details?.auth_methods || currentPatient?.auth_methods;
      setOptions(methods?.authMethods);
    }
  }, []);

  const handleAuthChange = (event) => {
    setSelectedAuthOption(event.target.value);
    const payload = {
      abha_number: currentPatient?.patient_details?.abha_number || currentPatient?.abha_number,
      purpose: "KYC_AND_LINK",
      auth_mode: event.target.value,
      hip_id: currentPatient?.patient_details?.hip_id || currentPatient?.hip_id,
    };
    dispatch(getPatientAuth(payload)).then((res) => {
      setTxnId(res.payload?.txn_id);
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
      handleModalClose();
      sessionStorage.removeItem("pmrId");
      navigate("/appointment-list");
    });
  };
  return (
    <Dialog
      open={showSync}
      onClose={handleModalClose}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
      fullWidth={true}
      maxWidth={'sm'}
    >
      <DialogTitle>Sync ABHA</DialogTitle>
      <IconButton
        aria-label="close"
        onClick={handleModalClose}
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
                disabled={
                  !(option === "AADHAAR_OTP" || option === "MOBILE_OTP") ||
                  selectedAuthOption
                }
              />
            ))}
          </RadioGroup>
        </FormControl>
        <OTPWrapper>
          {txnId !== "" && (<OtpInput verifyOTP={verifyOTP} isSync={true} />)}
        </OTPWrapper>
      </DialogContent>
      <DialogActions>
        <SecondaryButton onClick={clearData}>Clear</SecondaryButton>
        <PrimaryButton onClick={onSync}>Sync PMR</PrimaryButton>
      </DialogActions>
    </Dialog>
  );
};

export default SyncAbha;
