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
    "&.MuiButtonBase-root": {
      display: "flex",

      justifyContent: "center",
      alignItems: "center",
      border: `1px solid ${theme.palette.primaryBlack}`,
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      backgroundColor: theme.palette.primaryBlack,
      color: theme.palette.primaryWhite,
      padding: "8px 32px",
      height: "40px",
    },
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
  handleSubmit,
  setSixDigitOTP,
  verifyOTP,
  phoneNumberUsed,
}) => {
  return (
    <PhoneVerificationWrapper>
      <div className="validate-phone-form">
        <TextField
          type="text"
          value={number}
          onChange={handleNumberChange}
          className="phone-text"
        />
        <Button
          onClick={() => handleSubmit("phone_number")}
          variant="contained"
          className="verification-btn"
        >
          Verify
        </Button>
      </div>
      {!phoneNumberUsed && (
        <div>
          <Typography className="otp-title">Enter OTP</Typography>
          <OtpInput setSixDigitOTP={setSixDigitOTP} verifyOTP={verifyOTP} />
        </div>
      )}
    </PhoneVerificationWrapper>
  );
};

export default PhoneVerification;
