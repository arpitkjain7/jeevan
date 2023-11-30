import { Button, TextField, Typography, styled } from "@mui/material";
import React from "react";
import OtpInput from "../OTPValidation";

const PhoneVerificationWrapper = styled("div")(({ theme }) => ({
  ".validate-phone-form": {
    display: "flex",
    alignItems: "center",
    marginBottom: "24px",
    gap: "24px",
  },
  ".verification-btn": {
    "&.MuiButtonBase-root": theme.typography.primaryButton,
  },
  ".phone-text": {
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
    "&.MuiTypography-root": {
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "14px",
      lineHeight: "160%",
      marginBottom: "4px",
    },
  },
}));
const PhoneVerification = ({
  number,
  handleNumberChange,
  isMobileError,
  handleSubmit,
  PhoneDisabled,
  setSixDigitOTP,
  verifyOTP,
  phoneNumberUsed,
  seconds
}) => {
  return (
    <PhoneVerificationWrapper>
      <div className="validate-phone-form">
        <TextField
          type="number"
          value={number}
          onChange={handleNumberChange}
          error={isMobileError}
          className="phone-text"
        />
        {seconds > 0 || seconds < 0 ? (
        <Button
          disabled={PhoneDisabled}
          onClick={() => handleSubmit("phone_number")}
          variant="contained"
          className="verification-btn"
        >
          Verify
        </Button>         
        ) : (
          <Button
          disabled={seconds > 0 || seconds < 0}
          style={{
            color: seconds > 0 || seconds < 0 ? "#DFE3E8" : "#FFF",
          }}
          variant="contained"
          className="verification-btn"
          onClick={() => handleSubmit("phone_number")}
        >
          Resend OTP
        </Button>
        )}
      </div>
      {seconds > 0 || seconds < 0 ? (
        null
     ) : ( <p>
      Resend OTP in: 00:
      {seconds < 10 ? `0${seconds}` : seconds}
    </p>)}
      {!phoneNumberUsed && (
        <div>
          <Typography className="otp-title">Enter OTP</Typography>
          <OtpInput
            setSixDigitOTP={setSixDigitOTP}
            verifyOTP={verifyOTP}
            type="phone_number"
          />
       
        </div>
      )}
    </PhoneVerificationWrapper>
  );
};

export default PhoneVerification;
