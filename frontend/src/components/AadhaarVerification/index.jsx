import {
  Button,
  CircularProgress,
  InputLabel,
  TextField,
  Typography,
  styled,
} from "@mui/material";
import React, { useEffect, useRef, useState } from "react";
import OtpInput from "../OTPValidation";
import { useDispatch, useSelector } from "react-redux";

const AadhaarVerificationWrapper = styled("div")(({ theme }) => ({
  ".validate-aadhaar-form": {
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
        [theme.breakpoints.down("sm")]: {
          width: "auto",
        },
      },
    },
  },
  ".otp-title": {
    "&.MuiTypography-root": theme.typography.body3,
  },
}));

const OtpInputWrapperWrapper = styled("div")(({ theme }) => ({
  ".otp-textfield": {
    "&.MuiFormControl-root": {
      width: "48px",
      marginRight: "16px",
      [theme.breakpoints.down('sm')]: {
        width: "40px",
        marginRight: "10px",
      }
    },
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
  seconds,
  handleOpen,
  openConsent,
  create_abha,
  handleNumberChange,
  isMobileError,
  number,
}) => {
  const dispatch = useDispatch();
  const dataState = useSelector((state) => state);
  const fetchingAadhaarOtp = dataState?.PatientRegistartion?.loading;
  const [otp, setOTP] = useState(["", "", "", "", "", ""]);
  const inputRefs = useRef([]);
  const [OTPValue, setOTPValue] = useState("");

  useEffect(() => {
    const isOTPComplete = otp.every((value) => value !== "");
    if (isOTPComplete) {
      const otpString = otp.join("");
      setOTPValue(otpString);
    }
  }, [otp, dispatch]);

  const handleInputChange = (event, index) => {
    const { value } = event.target;
    
    if (/^\d*$/.test(value)) {
      setOTP((prevOTP) => {
        const newOTP = [...prevOTP];
        newOTP[index] = value;
        return newOTP;
      });
      if (value !== "") {
        focusNextInput(index);
      }
    }
  };

  const focusNextInput = (index) => {
    if (index < 5) {
      inputRefs.current[index + 1].focus();
    }
  };

  // const focusPreviousInput = (index) => {
  //   if (index > 0) {
  //     inputRefs.current[index - 1].focus();
  //   }
  // };
  const handleKeyChange = (event, index) => {
    if(event.key == "Backspace" && index > 0){
      inputRefs.current[index - 1].focus();
    }
  }

  const handleInputPaste = (event) => {
    event.preventDefault();
    const pastedText = event.clipboardData.getData("text/plain");
    const otpArray = pastedText
      ?.slice(0, 6)
      .split("")
      .map((char) => (/^\d$/.test(char) ? char : ""));
    setOTP(otpArray);
  };

  
  const handleVerifyOTP = () => {
    verifyOTP(OTPValue, "aadhaar");
  };

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
        {openConsent ? 
          <Button
            disabled={!isAadhaarValid}
            onClick={handleOpen}
            variant="contained"
            className="verification-btn"
          >
              Submit
          </Button>
        : 
        (
          seconds > 0 || seconds < 0 ? (
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
              disabled={!isAadhaarValid}
              style={{
                color: seconds > 0 || seconds < 0 ? "#DFE3E8" : "#FFF",
              }}
              onClick={() => handleSubmit("aadhaar")}
              variant="contained"
              className="verification-btn"
            >
              {fetchingAadhaarOtp ? (
                <CircularProgress size={24} />
              ) : (
                " Resend OTP"
              )}
            </Button>
          
        )
        )}
      </div>
      <div>
        <span style={{ color: "red" }}>
          {isAadhaarError ? "Please enter correct Aadhaar Number" : ""}
        </span>
      </div>
      {seconds < 0 ? null : (
        <h4>
          Resend OTP in: 00:
          {seconds < 10 ? `0${seconds}` : seconds}
        </h4>
      )}
 
      {!create_abha && aadhaarOTP && (
        <div>
          <Typography className="otp-title">Enter OTP</Typography>
          <OtpInput
            setSixDigitOTP={setSixDigitOTP}
            verifyOTP={verifyOTP}
            type="aadhaar"
          />
        </div>
      )}
      
      {create_abha && aadhaarOTP && (
        <>
          <br/>
          <Typography className="otp-title">Enter OTP</Typography>
          {/* <OtpInput
            setSixDigitOTP={setSixDigitOTP}
            // verifyOTP={verifyOTP}
            type="aadhaar"
          />  */}
          <OtpInputWrapperWrapper>
            {otp?.map((value, index) => (
              <TextField
                key={index}
                type="text"
                value={value}
                onChange={(event) => handleInputChange(event, index)}
                onKeyUp={(event) => handleKeyChange(event, index)}
                onPaste={handleInputPaste}
                inputRef={(el) => (inputRefs.current[index] = el)}
                inputProps={{ maxLength: 1 }}
                className="otp-textfield"
              />
            ))}
          </OtpInputWrapperWrapper>
          <br/>
          <InputLabel className="phone-label">Enter mobile number</InputLabel>
          <TextField
            type="number"
            value={number}
            onChange={handleNumberChange}
            error={isMobileError}
            className="phone-text"
          />
           <br/>
          <Button
            onClick={handleVerifyOTP}
            variant="contained"
            className="verification-btn"
          > 
            Verify
          </Button>
        </>
      )}
    </AadhaarVerificationWrapper>
  );
};

export default AadhaarVerification;
