import { Button, TextField, Typography, styled } from "@mui/material";
import React from "react";
import OtpInput from "../OTPValidation";

const AadharVerificationWrapper = styled("div")(({ theme }) => ({
  ".validate-aadhar-form": {
    display: "flex",
    alignItems: "center",
    marginBottom: "24px",
    gap: "24px",
  },
  ".verification-btn": {
    "&.MuiButtonBase-root": {
      display: "flex",

      justifyContent: "center",
      alignItems: "center",
      border: `1px solid ${theme.primaryBlack}`,
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      backgroundColor: theme.primaryBlack,
      color: theme.primaryWhite,
      padding: "8px 32px",
      height: "40px",
    },
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
    "&.MuiTypography-root": {
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "14px",
      lineHeight: "160%",
      marginBottom: "4px",
    },
  },
}));

function AadharVerification({
  aadhar,
  handleAadharChange,
  handleSubmit,
  setSixDigitOTP,
  verifyOTP,
}) {
  return (
    <AadharVerificationWrapper>
      <div className="validate-aadhar-form">
        <TextField
          type="text"
          value={aadhar}
          onChange={handleAadharChange}
          className="aadhar-text"
        />
        <Button
          onClick={() => handleSubmit("aadhar")}
          variant="contained"
          className="verification-btn"
        >
          Get OTP
        </Button>
      </div>
      <div>
        <Typography className="otp-title">Enter OTP</Typography>
        <OtpInput setSixDigitOTP={setSixDigitOTP} verifyOTP={verifyOTP} />
      </div>
    </AadharVerificationWrapper>
  );
}

export default AadharVerification;
