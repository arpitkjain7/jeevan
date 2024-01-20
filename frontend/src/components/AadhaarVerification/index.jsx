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

const AadhaarVerificationWrapper = styled("div")(({ theme }) => ({
  ".validate-aadhaar-form": {
    display: "flex",
    alignItems: "center",
    marginBottom: "4px",
    gap: "24px",
    [theme.breakpoints.down('sm')]: {
      gap: "10px",
    },
    "input[type=password i]": {
      "-webkitTextSecurity": "square"
    },
  },
  ".verification-btn": {
    "&.MuiButtonBase-root": {
      "&": theme.typography.primaryButton,
      [theme.breakpoints.down('sm')]: {
        padding: "10px"
      },
    }   
  },
  ".aadhaar-text": {
    "&.MuiFormControl-root": {
      "& > .MuiInputBase-root": {
        display: "flex",
        height: "48px",
        width: "320px",
        justifyContent: "center",
        alignItems: "center",
        flex: "1 0 0",
        alignSelf: "stretch",
        [theme.breakpoints.down('sm')]: {
          width: "auto",
        },
      },
    },
  },
  ".otp-title": {
    "&.MuiTypography-root": theme.typography.body3,
  },
}));

const AadhaarVerification = ({
  aadhaar,
  handleAadhaarChange,
  isAadhaarError,
  handleSubmit,
  isAadhaarValid,
  aadhaarOTP,
  setSixDigitOTP,
  verifyOTP,
  seconds
}) => {
  const dataState = useSelector((state) => state);
  const fetchingAadhaarOtp = dataState?.PatientRegistartion?.loading;

  console.log(fetchingAadhaarOtp, "loading");
  return (
    <AadhaarVerificationWrapper>
      <div className="validate-aadhaar-form">
        <TextField
          type="password"
          value={aadhaar}
          onChange={handleAadhaarChange}
          error={isAadhaarError}
          className="aadhaar-text"
        />
        {seconds > 0 || seconds < 0 ? (
          <Button
            disabled={!isAadhaarValid}
            onClick={() => handleSubmit("aadhaar")}
            variant="contained"
            className="verification-btn"
          >
            {fetchingAadhaarOtp ? <CircularProgress size={24} /> : " Get OTP"}
          </Button>
            ) : (
              <Button
              disabled={!isAadhaarValid }
              style={{
                color: seconds > 0 || seconds < 0 ? "#DFE3E8" : "#FFF",
              }}
              onClick={() => handleSubmit("aadhaar")}
              variant="contained"
              className="verification-btn"
            >
              {fetchingAadhaarOtp ? <CircularProgress size={24} /> : " Resend OTP"}
            </Button>
            )}
      </div>
      <div>
        <span style={{ color: 'red'}}>{isAadhaarError ? "Please enter correct Aadhaar Number" : ""}</span>
      </div>
      {seconds < 0 ? (
        null
      ):( <h4>
        Resend OTP in: 00:
        {seconds < 10 ? `0${seconds}` : seconds}
      </h4>)}
     
      {aadhaarOTP && (
      <div>
        <Typography className="otp-title">Enter OTP</Typography>
        <OtpInput
          setSixDigitOTP={setSixDigitOTP}
          verifyOTP={verifyOTP}
          type="aadhaar"
        />
      </div>
      )}
    </AadhaarVerificationWrapper>
  );
};

export default AadhaarVerification;
