import {
    Button,
    CircularProgress,
    FormControl,
    FormControlLabel,
    RadioGroup,
    TextField,
    Typography,
    styled,
    Radio,
  } from "@mui/material";
  import React from "react";
  import OtpInput from "../OTPValidation";
  import { useSelector } from "react-redux";
  
  const AbhaVerificationWrapper = styled("div")(({ theme }) => ({
    ".validate-abha-form": {
      display: "flex",
      alignItems: "center",
      marginBottom: "4px",
      gap: "24px",
      [theme.breakpoints.down("sm")]: {
        gap: "10px",
      },
      "input[type=password i]": {
        "-webkitTextSecurity": "square",
      },
    },
    ".verification-btn": {
      "&.MuiButtonBase-root": {
        "&": theme.typography.primaryButton,
        [theme.breakpoints.down("sm")]: {
          padding: "10px",
        },
      },
    },
    ".abha-text": {
      "&.MuiFormControl-root": {
        "& > .MuiInputBase-root": {
          display: "flex",
          height: "48px",
          width: "320px",
          justifyContent: "center",
          alignItems: "center",
          flex: "1 0 0",
          alignSelf: "stretch",
          [theme.breakpoints.down("sm")]: {
            width: "auto",
          },
        },
      },
    },
    ".otp-title": {
      "&.MuiTypography-root": theme.typography.body2,
      marginTop: "20px",
      marginRight: "10px",
    },
  }));
  
  const AbhaVerification = ({
    abha,
    handleAbhaChange,
    isAbhaError,
    // handleSubmit,
    isAbhaValid,
    abhaOTP,
    setSixDigitOTP,
    verifyOTP,
    seconds,
    isAbhaAuthMode,
    handleAbhaAuthModeChange,
    abhaAuthModeOptions,
    abhaAuthModeValue,
    handleAbhaGenerateOTP,
    handleAbhaResetOTP
  }) => {
    const dataState = useSelector((state) => state);
    const fetchingAbhaOtp = dataState?.PatientRegistartion?.loading;
  
    return (
      <AbhaVerificationWrapper>
        <div className="validate-abha-form">
          <TextField
            // type="password"
            value={abha}
            onChange={handleAbhaChange}
            error={isAbhaError}
            className="abha-text"
          />
           {/* <Button
              onClick={() => handleSubmit("abha")}
              variant="contained"
              className="verification-btn"
            >
                Submit
            </Button> */}
        </div>
        <div>
          <span style={{ color: "red" }}>
            {isAbhaError ? "Please enter correct Abha Number" : ""}
          </span>
        </div>

        {isAbhaAuthMode && (
            <div style={{ paddingBottom: "1px" }}>
                <Typography className="otp-title">Select Mode</Typography>
                <FormControl>
                    <div component="fieldset">
                        <RadioGroup
                            row
                            value={abhaAuthModeValue}
                            onChange={handleAbhaAuthModeChange}
                            style= {{ marginBottom: "10px" }}
                            >
                            {abhaAuthModeOptions?.map((option) => (
                                <FormControlLabel
                                    key={option.value}
                                    value={option.value}
                                    control={<Radio />}
                                    label={option.label}
                                />
                            ))}
                        </RadioGroup>
                        {seconds === -1 ? ( //> 0 || seconds < 0
                            <Button
                                disabled={isAbhaValid}
                                onClick={() => handleAbhaGenerateOTP()}
                                variant="contained"
                                className="verification-btn"
                            >
                            {fetchingAbhaOtp ? <CircularProgress size={24} /> : " Get OTP"}
                            </Button>
                        ) : (
                            <Button
                            disabled={!isAbhaValid}
                            style={{
                                color: seconds > 0 ? "#DFE3E8" : "#FFF",
                            }}
                            onClick={() => handleAbhaResetOTP()}
                            variant="contained"
                            className="verification-btn"
                            >
                            {fetchingAbhaOtp ? (
                                <CircularProgress size={24} />
                            ) : (
                                " Resend OTP"
                            )}
                            </Button>
                        )}
                    </div>
                </FormControl>
                {seconds < 0 ? null : (
                    <h4>
                        Resend OTP in: 00:
                        {seconds < 10 ? `0${seconds}` : seconds}
                    </h4>
                )}
            </div>
        )}

        {abhaOTP && (
          <div>
            <Typography className="otp-title">Enter OTP</Typography>
            <OtpInput
              setSixDigitOTP={setSixDigitOTP}
              verifyOTP={verifyOTP}
              type="abha"
            />
          </div>
        )}
      </AbhaVerificationWrapper>
    );
  };
  
  export default AbhaVerification;
  