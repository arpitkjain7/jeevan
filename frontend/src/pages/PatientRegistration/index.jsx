import {
  styled
} from "@mui/material";
import React, { useEffect, useState } from "react";
import ExpandableCard from "../../components/ExpandableCard";
import { CheckBox } from "@mui/icons-material";
import OtpInput from "../../components/OTPValidation";
import { useDispatch, useSelector } from "react-redux";
import {
  registerAADHAAR,
  registerPhone,
  verifyAadhaarOTP,
  verifyAadhaarPhoneOTP,
  verifyPhoneOTP,
} from "./PatientRegistration.slice";
import PatientRegistartionForm from "../../components/PatientRegistrationForm";
import VerificationSelection from "../../components/VerificationSelection";
import AadhaarVerification from "../../components/AadhaarVerification";
import AadhaarConsent from "../../components/AadhaarConsent";
import PhoneVerification from "../../components/PhoneVerification";
import RegisterationConfirmation from "../../components/RegistrationConfirmation";
import { apis } from "../../utils/apis";
import AadhaarPatientRegForm from "../../components/AadhaarPatientRegistrationForm";
import CustomSnackbar from "../../components/CustomSnackbar";
import CustomLoader from "../../components/CustomLoader";

const PatientRegisterWrapper = styled("div")(({ theme }) => ({
  "&": {
    padding: "10px",
    display: "flex",
    flexDirection: "column",
    gap: "40px",
    [theme.breakpoints.down('sm')]: {
      gap: "20px",
      padding: "10px 5px",
    },
  },

  ".validate-aadhaar-form": {
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
  ".displayHeaderContainer": {
    display: "none"
  }
}));
const PatientRegistration = () => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [checkedOption, setCheckedOption] = useState(null);
  const [registration, setRegistration] = useState(true);
  const [verifyAadhaar, setVerifyAadhaar] = useState(true);
  const [verifyNumber, setVerifyNumber] = useState(true);
  const [userDetailsForm, setUserDeatilsForm] = useState(true);
  const [sixDigitOTP, setSixDigitOTP] = useState("");
  const [number, setNumber] = useState();
  const dataState = useSelector((state) => state);
  const aadhaarData = dataState?.PatientRegistartion?.registerAadhaar;
  const phoneData = dataState?.PatientRegistartion?.registerPhone;
  const [stepOne, setStepOne] = useState(false);
  const [stepTwo, setStepTwo] = useState(false);
  const [stepThree, setStepThree] = useState(false);
  const [stepFour, setStepFour] = useState(false);
  const [aadhaar, setAadhaar] = useState("");
  const dispatch = useDispatch();
  const [userCreated, setUserCreated] = useState(false);
  const [phoneNumberUsed, setPhoneNumberUsed] = useState(true);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [showLoader, setShowLoader] = useState(false);
  const [errorMessage, setErrorMessage] = useState('Something went wrong');
  const [isMobileError, setIsMobileError] = useState(false);
  const [isAadhaarError, setIsAadhaarError] = useState(false);
  const [isAadhaarValid, setIsAadhaarValid] = useState(false);
  const [aadhaarOTP, setAadhaarOTP] = useState(false);
  const [PhoneDisabled, setPhoneDisabled] = useState(true);
  const [aadhaarOTPseconds, setAadhaarOTPSeconds] = useState(-1);
  const [seconds, setSeconds] = useState(-1);
  const [open, setOpen] = useState(false);
  const userRole = sessionStorage?.getItem("userRole");
  const scroll = 'paper';

  const adminModes = [
    {
      label: "Aadhaar",
      value: "aadhaar",
    },
    {
      label: "Phone Number",
      value: "phone_number",
    },
  ];

  const modes = [
    {
      label: "Phone Number",
      value: "phone_number",
    },
  ];

  const resetFields = () => {
    setStepOne(false);
    setStepTwo(false);
    setStepThree(false);
    setStepFour(false);
    setPhoneNumberUsed(true);
    setNumber("");
    setUserDeatilsForm(true);
    setAadhaar("");
    setSixDigitOTP("");
    setVerifyNumber(true);
    setVerifyAadhaar(true);
    setRegistration(true);
    setCheckedOption(null);
    setIsAadhaarValid(false);
    setAadhaarOTP(false);
    setAadhaarOTPSeconds(-1);
    setSeconds(-1);
  };

  const aadhaar_regex = new RegExp('^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}|[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}|[2-9]{1}[0-9]{3}-[0-9]{4}-[0-9]{4}$');
  const handleOptionChange = (event) => {
    if (selectedOption?.length) {
      resetFields();
    }
    setSelectedOption(event.target.value);
  };

  const handleOptionCheck = (event) => {
    setCheckedOption((prevValue) => !prevValue);
  };

  const handleAadhaarChange = (event) => {
    const inputValue = event.target.value;
    // Check if the input value is empty string
    if (inputValue !== null) {
      setAadhaar(inputValue);
      if (!aadhaar_regex.test(event.target.value)) {
        setIsAadhaarError(true);
        setIsAadhaarValid(false);
      } else {
        setIsAadhaarError(false);
        setIsAadhaarValid(true);
      }
    }
  
    // if (isNaN(numericValue) || inputValue === "") {
    //   console.log(isNaN(numericValue));
    //   setErrorMessage('Please enter valid Aadhaar number!');
    // } else {    
    //   setAadhaar(inputValue);
    // }
  };

  const handleNumberChange = (event) => {
    const inputValue = event.target.value;
    const numericValue = parseInt(inputValue);
    if (isNaN(numericValue) || numericValue !== "") 
      setNumber(numericValue)
    let new_Number_length = inputValue.length;
    if (new_Number_length > 10 || new_Number_length < 10) {
      // setErrorMessage("Please enter valid number")
      setIsMobileError(true);
      setPhoneDisabled(true);
    } else if (new_Number_length === 10) {
      setIsMobileError(false);
      setPhoneDisabled(false);
      
    }
    // const numericValue = parseInt(inputValue);
    // Check if the input value is a valid number or empty string
    // if (!isNaN(numericValue) || inputValue === "") {
    //   setNumber(inputValue);
    // }
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSubmit = (type) => {
    // Handle the form submission
     setShowLoader(true);
    if (type === "aadhaar") {
      
    //validation
    if (aadhaar_regex.test(aadhaar)){
      setIsAadhaarValid(false);
      console.log("Form submitted:", aadhaar);
        const payload = {
          aadhaarNumber: (aadhaar).replace(/\D/g, ""),
        };
        dispatch(registerAADHAAR(payload)).then((res) => {
          setShowLoader(false);
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            setErrorMessage("Please enter valid Aadhaar Number");
            setShowSnackbar(true);
            return;
          }
          setAadhaarOTPSeconds(60);
          setAadhaarOTP(true);
          setIsAadhaarValid(true);
        });
      } else {
        console.log("Failed");
        setErrorMessage("Please enter a correct Aadhaar Number");
        setShowSnackbar(true);
      }
    } else if (type === "phone_number") {
     
      const mobile_pattern = new RegExp(/^[0-9]{10}$/);
      if (mobile_pattern.test(number)){
        setPhoneDisabled(true);
        const payload =
          selectedOption === "aadhaar"
            ? {
                txnId: aadhaarData?.txn_id,
                mobileNumber: number,
              }
            : {
                mobileNumber: number,
              };
        const url =
          selectedOption === "aadhaar"
            ? apis?.registerAadhaarNumber
            : apis?.restigerNumber;
        dispatch(registerPhone({ payload, url })).then((res) => {
          setShowLoader(false);
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            setShowSnackbar(true);
            return;
          }
          const resData = res?.payload;
         
          if (resData?.mobileLinked && selectedOption === "aadhaar") {
            setPhoneNumberUsed(resData?.mobileLinked);
            setStepThree(true);
          } else if(!resData?.mobileLinked && selectedOption === "aadhaar"){
            setSeconds(60);
            setPhoneNumberUsed(false);
            setPhoneDisabled(false);
          } else if(selectedOption === "phone_number"){
            setSeconds(60);
            setPhoneNumberUsed(false);
            setPhoneDisabled(false);
          }
        });
      } else {
        console.log("Failed");
        setErrorMessage("Please enter valid Number");
        setShowSnackbar(true);
      }
    }
  };

  const verifyOTP = (otp, type) => {
    if (selectedOption === "aadhaar" && type === "aadhaar") {
      const payload = {
        txnId: aadhaarData?.txn_id,
        otp: otp,
      };
      dispatch(verifyAadhaarOTP(payload)).then((res) => {
        if (res?.error && Object.keys(res?.error)?.length > 0) {
          setErrorMessage("Please enter correct OTP");
          setShowSnackbar(true);
          setStepTwo(false);
          return;
        }
        else setStepTwo(true);
      });
     
      if (stepTwo) {
        setStepThree(true);
      }
    } else if (selectedOption === "phone_number" && type === "phone_number") {
      const payload = {
        txnId: phoneData?.txn_id,
        otp: otp,
      };
      dispatch(verifyPhoneOTP(payload)).then((res) => {
        if (res?.error && Object.keys(res?.error)?.length > 0) {
          setShowSnackbar(true);
          setErrorMessage("Please enter correct OTP");
          setStepTwo(false);
          return;
        }
        // else {
          setStepTwo(true);
        // }
      });
    } else if (selectedOption === "aadhaar" && type === "phone_number") {
      const payload = {
        txnId: phoneData?.txn_id,
        otp: otp,
      };
      dispatch(verifyAadhaarPhoneOTP(payload)).then((res) => {
        if (res?.error && Object.keys(res?.error)?.length > 0) {
          setShowSnackbar(true);
          return;
        }
        console.log(res);
        setStepTwo(true);
        if (stepTwo) {
          setStepThree(true);
        }
      });
    }
  };

  useEffect(() => {
    if (stepOne) {
      setRegistration(false);
      if (selectedOption === "aadhaar") {
        setVerifyAadhaar(true);       
      }
      if (selectedOption === "phone_number" && checkedOption) {
        setUserDeatilsForm(true);
      }
      if (selectedOption === "phone_number" && !checkedOption) {
        setVerifyNumber(true);
      }
    }

    if (stepTwo) {
      setUserDeatilsForm(false);

      if (selectedOption === "aadhaar") {
        setVerifyAadhaar(false);
        setVerifyNumber(true);
      }

      if (selectedOption === "phone_number") {
        setVerifyNumber(false);
        setUserDeatilsForm(true);
      }
    }

    if (stepThree) {
      setRegistration(false);
      setVerifyAadhaar(false);
      setVerifyNumber(false);
      setUserDeatilsForm(true);
    }
  }, [stepOne, stepTwo, stepThree, stepFour, selectedOption]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (seconds > 0) {
        setSeconds(seconds - 1);
      }
  
      if (seconds === 0) {
        clearInterval(interval);       
      }
    }, 1000);
    return () => {
      clearInterval(interval);
    };
  }, [seconds]);

  useEffect(() => {
    const interval = setInterval(() => {
      if (aadhaarOTPseconds > 0) {
        setAadhaarOTPSeconds(aadhaarOTPseconds - 1);
      }
  
      if (aadhaarOTPseconds === 0) {
        clearInterval(interval);       
      }
    }, 1000);
    return () => {
      clearInterval(interval);
    };
  }, [aadhaarOTPseconds]);

  const handleConfirmSelection = () => {
    if(selectedOption == "aadhaar") {
      setOpen(true);
    } else {
      setStepOne(true);
    }
  };

  const handleConsentConfirmation = () => {
    setStepOne(true);
    setOpen(false);
  }

  const onSnackbarClose = () => {
    setShowSnackbar(false);
  };

  const onLoaderClose = () => {
    setShowLoader(false);
  };

  return (
    <PatientRegisterWrapper>
      <CustomSnackbar
        message={errorMessage}
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
       <CustomLoader
        open={showLoader}
        onClose={onLoaderClose}
      />
       
        <AadhaarConsent
          open={open}
          handleClose={handleClose}
          scroll={scroll}
          handleConsentConfirmation={handleConsentConfirmation}
          aria-labelledby="scroll-dialog-title"
          aria-describedby="scroll-dialog-description"
        >
        </AadhaarConsent>
      <ExpandableCard
        title={`Mode of Registration ${
          selectedOption ? "|" + " " + selectedOption?.replace("_", " ") : ""
        }`}
        expanded={registration}
        setExpanded={setRegistration}
        completed={stepOne}
      >
        { userRole === "ADMIN" ? (
        <VerificationSelection
          modes={adminModes}
          handleOptionChange={handleOptionChange}
          selectedOption={selectedOption}
          checkedOption={checkedOption}
          handleOptionCheck={handleOptionCheck}
          handleConfirmSelection={handleConfirmSelection}
        />) : (
          <VerificationSelection
          modes={modes}
          handleOptionChange={handleOptionChange}
          selectedOption={selectedOption}
          checkedOption={checkedOption}
          handleOptionCheck={handleOptionCheck}
          handleConfirmSelection={handleConfirmSelection}
          displayHeaderContainer="displayHeaderContainer"
        />
        )}
      </ExpandableCard>
     
      {selectedOption === "aadhaar" && stepOne && !checkedOption && (
        <ExpandableCard
          title="AADHAAR Verification"
          expanded={verifyAadhaar}
          setExpanded={setVerifyAadhaar}
          completed={stepTwo}
        >
          <AadhaarVerification
            aadhaar={aadhaar}
            handleAadhaarChange={handleAadhaarChange}
            isAadhaarError={isAadhaarError}
            handleSubmit={handleSubmit}
            isAadhaarValid={isAadhaarValid}
            aadhaarOTP={aadhaarOTP}
            setSixDigitOTP={setSixDigitOTP}
            verifyOTP={verifyOTP}
            seconds={aadhaarOTPseconds}
          /> 
        </ExpandableCard>
      )}
      {(selectedOption === "aadhaar" && stepTwo && !checkedOption &&
         <ExpandableCard
         title="Mobile Number Verification"
         expanded={verifyNumber}
         setExpanded={setVerifyNumber}
         completed={(selectedOption === "aadhaar" && stepThree)}
       >
         <PhoneVerification
           number={number}
           handleNumberChange={handleNumberChange}
           isMobileError={isMobileError}
           handleSubmit={handleSubmit}
           PhoneDisabled={PhoneDisabled}
           setSixDigitOTP={setSixDigitOTP}
           verifyOTP={verifyOTP}
           seconds={seconds}
           phoneNumberUsed={phoneNumberUsed}
         /> 
       </ExpandableCard>
      )}
      {(selectedOption === "phone_number" && stepOne && checkedOption &&
        <ExpandableCard
          title="Mobile Number Verification"
          expanded={verifyNumber}
          setExpanded={setVerifyNumber}
          completed={(selectedOption === "phone_number" && stepTwo)}
        >
          <PhoneVerification
            number={number}
            handleNumberChange={handleNumberChange}
            isMobileError={isMobileError}
            handleSubmit={handleSubmit}
            PhoneDisabled={PhoneDisabled}
            setSixDigitOTP={setSixDigitOTP}
            verifyOTP={verifyOTP}
            seconds={seconds}
            phoneNumberUsed={phoneNumberUsed}
          /> 
        </ExpandableCard>
      )}

      {(selectedOption === "phone_number" && checkedOption && stepTwo) ||
      (selectedOption === "aadhaar" && stepThree && !checkedOption) ||
      (!checkedOption && stepOne && selectedOption === "phone_number") ? (
        <ExpandableCard
          title="Patient Details"
          expanded={userDetailsForm}
          setExpanded={setUserDeatilsForm}
        >
          <div className="patient-registration-form">
            {selectedOption === "aadhaar" ? (
              <AadhaarPatientRegForm
                setUserCreated={setUserCreated}
                txnId={aadhaarData.txn_id}
                isForAbha={checkedOption}
              />
            ) : (
              <PatientRegistartionForm
                setUserCreated={setUserCreated}
                isForAbha={checkedOption}
                txnId={phoneData.txn_id}
              />
            )}
          </div>
        </ExpandableCard>
      ) : null}
      {/* {userCreated && (
        <ExpandableCard
          title="SucessFully Created"
          expanded={userDetailsForm}
          setExpanded={setUserDeatilsForm}
        >
          <div className="patient-registration-form">
            <RegisterationConfirmation />
          </div>
        </ExpandableCard>
      )} */}
      
    </PatientRegisterWrapper>
  );
};

export default PatientRegistration;
