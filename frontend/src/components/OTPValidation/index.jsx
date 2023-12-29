import React, { useState, useEffect, useRef } from "react";
import { useDispatch } from "react-redux";
import { TextField, Grid, styled } from "@mui/material";

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
const OtpInput = ({ verifyOTP, type, isSync = false }) => {
  const dispatch = useDispatch();
  const [otp, setOTP] = useState(["", "", "", "", "", ""]);
  const inputRefs = useRef([]);

  useEffect(() => {
    const isOTPComplete = otp.every((value) => value !== "");
    if (isOTPComplete) {
      const otpString = otp.join("");
      if (type && !isSync) {
        verifyOTP(otpString, type);
      } else {
        verifyOTP(otpString);
      }
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
        // else {
        //   focusPreviousInput(index);
        // }
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

  return (
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
  );
};

export default OtpInput;
