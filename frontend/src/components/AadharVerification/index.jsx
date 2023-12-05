import {
  Button,
  CircularProgress,
  TextField,
  Typography,
  styled
} from "@mui/material";
import React from "react";
import OtpInput from "../OTPValidation";
import { useSelector } from "react-redux";

const AadharVerificationWrapper = styled("div")(({ theme }) => ({
  ".validate-aadhar-form": {
    display: "flex",
    alignItems: "center",
    marginBottom: "4px",
    gap: "24px",
  },
  ".verification-btn": {
    "&.MuiButtonBase-root": theme.typography.primaryButton,
  },
  ".aadhar-text": {
    "&.MuiFormControl-root": {
      "& > .MuiInputBase-root": {
        display: "flex",
        height: "48px",
        width: "320px",
        justifyContent: "center",
        alignItems: "center",
        flex: "1 0 0",
        alignSelf: "stretch",
      },
    },
  },
  ".otp-title": {
    "&.MuiTypography-root": theme.typography.body3,
  },
}));

const AadharVerification = ({
  aadhar,
  handleAadharChange,
  isAadharError,
  handleSubmit,
  isAadharValid,
  aadharOTP,
  setSixDigitOTP,
  verifyOTP,
  seconds
}) => {
  const dataState = useSelector((state) => state);
  const fetchingAadharOtp = dataState?.PatientRegistartion?.loading;

  console.log(fetchingAadharOtp, "loading");
  return (
    <AadharVerificationWrapper>
      <div className="validate-aadhar-form">
        <TextField
          type="text"
          value={aadhar}
          onChange={handleAadharChange}
          error={isAadharError}
          className="aadhar-text"
        />
        {seconds > 0 || seconds < 0 ? (
          <Button
            disabled={!isAadharValid}
            onClick={() => handleSubmit("aadhar")}
            variant="contained"
            className="verification-btn"
          >
            {fetchingAadharOtp ? <CircularProgress size={24} /> : " Get OTP"}
          </Button>
            ) : (
              <Button
              disabled={!isAadharValid }
              style={{
                color: seconds > 0 || seconds < 0 ? "#DFE3E8" : "#FFF",
              }}
              onClick={() => handleSubmit("aadhar")}
              variant="contained"
              className="verification-btn"
            >
              {fetchingAadharOtp ? <CircularProgress size={24} /> : " Resend OTP"}
            </Button>
            )}
      </div>
      <div style={{ marginBottom: "24px"}} >
        <span style={{ color: 'red', marginBottom: "24px"}}>{isAadharError ? "Please enter correct Aadhar Number" : ""}</span>
      </div>
      {seconds < 0 ? (
        null
      ):( <h4>
        Resend OTP in: 00:
        {seconds < 10 ? `0${seconds}` : seconds}
      </h4>)}
     
      {aadharOTP && (
      <div>
        <Typography className="otp-title">Enter OTP</Typography>
        <OtpInput
          setSixDigitOTP={setSixDigitOTP}
          verifyOTP={verifyOTP}
          type="aadhar"
        />
      </div>
      )}
    </AadharVerificationWrapper>
  );
};

export default AadharVerification;
