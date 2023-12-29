import {
  styled
} from "@mui/material";
import React, { useEffect, useState } from "react";
import ExpandableCard from "../../components/ExpandableCard";
import { CheckBox } from "@mui/icons-material";
import OtpInput from "../../components/OTPValidation";
import { useDispatch, useSelector } from "react-redux";
import {
  registerAADHAR,
  registerPhone,
  verifyAadharOTP,
  verifyAadharPhoneOTP,
  verifyPhoneOTP,
} from "./PatientRegistration.slice";
import PatientRegistartionForm from "../../components/PatientRegistrationForm";
import VerificationSelection from "../../components/VerificationSelection";
import AadharVerification from "../../components/AadharVerification";
import AadharConsent from "../../components/AadharConsent";
import PhoneVerification from "../../components/PhoneVerification";
import RegisterationConfirmation from "../../components/RegistrationConfirmation";
import { apis } from "../../utils/apis";
import AadharPatientRegForm from "../../components/AadharPatientRegistrationForm";
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
  ".displayHeaderContainer": {
    display: "none"
  }
}));
const PatientRegistration = () => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [checkedOption, setCheckedOption] = useState(null);
  const [registration, setRegistration] = useState(true);
  const [verifyAadhar, setVerifyAadhar] = useState(true);
  const [verifyNumber, setVerifyNumber] = useState(true);
  const [userDetailsForm, setUserDeatilsForm] = useState(true);
  const [sixDigitOTP, setSixDigitOTP] = useState("");
  const [number, setNumber] = useState();
  const dataState = useSelector((state) => state);
  const aadharData = dataState?.PatientRegistartion?.registerAadhar;
  const phoneData = dataState?.PatientRegistartion?.registerPhone;
  const [stepOne, setStepOne] = useState(false);
  const [stepTwo, setStepTwo] = useState(false);
  const [stepThree, setStepThree] = useState(false);
  const [stepFour, setStepFour] = useState(false);
  const [aadhar, setAadhar] = useState("");
  const dispatch = useDispatch();
  const [userCreated, setUserCreated] = useState(false);
  const [phoneNumberUsed, setPhoneNumberUsed] = useState(true);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [showLoader, setShowLoader] = useState(false);
  const [errorMessage, setErrorMessage] = useState('Something went wrong');
  const [isMobileError, setIsMobileError] = useState(false);
  const [isAadharError, setIsAadharError] = useState(false);
  const [isAadharValid, setIsAadharValid] = useState(false);
  const [aadharOTP, setAadharOTP] = useState(false);
  const [PhoneDisabled, setPhoneDisabled] = useState(true);
  const [aadharOTPseconds, setAadharOTPSeconds] = useState(-1);
  const [seconds, setSeconds] = useState(-1);
  const [open, setOpen] = useState(false);
  const userRole = sessionStorage?.getItem("userRole");
  const scroll = 'paper';

  const adminModes = [
    {
      label: "Aadhar",
      value: "aadhar",
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
    setAadhar("");
    setSixDigitOTP("");
    setVerifyNumber(true);
    setVerifyAadhar(true);
    setRegistration(true);
    setCheckedOption(null);
    setIsAadharValid(false);
    setAadharOTP(false);
    setAadharOTPSeconds(-1);
    setSeconds(-1);
  };

  const aadhar_regex = new RegExp('^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}|[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}|[2-9]{1}[0-9]{3}-[0-9]{4}-[0-9]{4}$');
  const handleOptionChange = (event) => {
    if (selectedOption?.length) {
      resetFields();
    }
    console.log(event.target.value);
    setSelectedOption(event.target.value);
  };

  const handleOptionCheck = (event) => {
    setCheckedOption((prevValue) => !prevValue);
  };

  const handleAadharChange = (event) => {
    const inputValue = event.target.value;
    // Check if the input value is empty string
    if (inputValue !== null) {
      setAadhar(inputValue);
      console.log(aadhar_regex.test(event.target.value));
      if (!aadhar_regex.test(event.target.value)) {
        setIsAadharError(true);
        setIsAadharValid(false);
      } else {
        setIsAadharError(false);
        setIsAadharValid(true);
      }
    }
  
    // if (isNaN(numericValue) || inputValue === "") {
    //   console.log(isNaN(numericValue));
    //   setErrorMessage('Please enter valid Aadhar number!');
    // } else {    
    //   setAadhar(inputValue);
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
    console.log(open);
    setOpen(false);
  };

  const handleSubmit = (type) => {
    // Handle the form submission
     setShowLoader(true);
    if (type === "aadhar") {
      
    //validation
    if (aadhar_regex.test(aadhar)){
      setIsAadharValid(false);
      console.log("Form submitted:", aadhar);
        const payload = {
          aadhaarNumber: (aadhar).replace(/\D/g, ""),
        };
        dispatch(registerAADHAR(payload)).then((res) => {
          console.log(res?.payload);
          setShowLoader(false);
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            setErrorMessage("Please enter valid Aadhar Number");
            setShowSnackbar(true);
            return;
          }
          setAadharOTPSeconds(30);
          setAadharOTP(true);
          setIsAadharValid(true);
        });
      } else {
        console.log("Failed");
        setErrorMessage("Please enter a correct Aadhar Number");
        setShowSnackbar(true);
      }
    } else if (type === "phone_number") {
     
      const mobile_pattern = new RegExp(/^[0-9]{10}$/);
      if (mobile_pattern.test(number)){
        setPhoneDisabled(true);
        const payload =
          selectedOption === "aadhar"
            ? {
                txnId: aadharData?.txn_id,
                mobileNumber: number,
              }
            : {
                mobileNumber: number,
              };
        const url =
          selectedOption === "aadhar"
            ? apis?.registerAadharNumber
            : apis?.restigerNumber;
        dispatch(registerPhone({ payload, url })).then((res) => {
          console.log(res);
          setShowLoader(false);
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            setShowSnackbar(true);
            return;
          }
          const resData = res?.payload;
         
          if (resData?.mobileLinked && selectedOption === "aadhar") {
            setPhoneNumberUsed(resData?.mobileLinked);
            setStepThree(true);
          } else if(!resData?.mobileLinked && selectedOption === "aadhar"){
            setSeconds(30);
            setPhoneNumberUsed(false);
            setPhoneDisabled(false);
          } else if(selectedOption === "phone_number"){
            setSeconds(30);
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
    if (selectedOption === "aadhar" && type === "aadhar") {
      const payload = {
        txnId: aadharData?.txn_id,
        otp: otp,
      };
      dispatch(verifyAadharOTP(payload)).then((res) => {
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
        console.log(res);
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
    } else if (selectedOption === "aadhar" && type === "phone_number") {
      const payload = {
        txnId: phoneData?.txn_id,
        otp: otp,
      };
      dispatch(verifyAadharPhoneOTP(payload)).then((res) => {
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
      if (selectedOption === "aadhar") {
        setVerifyAadhar(true);       
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

      if (selectedOption === "aadhar") {
        setVerifyAadhar(false);
        setVerifyNumber(true);
      }

      if (selectedOption === "phone_number") {
        setVerifyNumber(false);
        setUserDeatilsForm(true);
      }
    }

    if (stepThree) {
      setRegistration(false);
      setVerifyAadhar(false);
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
      if (aadharOTPseconds > 0) {
        setAadharOTPSeconds(aadharOTPseconds - 1);
      }
  
      if (aadharOTPseconds === 0) {
        clearInterval(interval);       
      }
    }, 1000);
    return () => {
      clearInterval(interval);
    };
  }, [aadharOTPseconds]);

  const handleConfirmSelection = () => {
    if(selectedOption == "aadhar") {
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
       
        <AadharConsent
          open={open}
          handleClose={handleClose}
          scroll={scroll}
          handleConsentConfirmation={handleConsentConfirmation}
          aria-labelledby="scroll-dialog-title"
          aria-describedby="scroll-dialog-description"
        >
        </AadharConsent>
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
     
      {selectedOption === "aadhar" && stepOne && !checkedOption && (
        <ExpandableCard
          title="AADHAR Verification"
          expanded={verifyAadhar}
          setExpanded={setVerifyAadhar}
          completed={stepTwo}
        >
          <AadharVerification
            aadhar={aadhar}
            handleAadharChange={handleAadharChange}
            isAadharError={isAadharError}
            handleSubmit={handleSubmit}
            isAadharValid={isAadharValid}
            aadharOTP={aadharOTP}
            setSixDigitOTP={setSixDigitOTP}
            verifyOTP={verifyOTP}
            seconds={aadharOTPseconds}
          /> 
        </ExpandableCard>
      )}
      {(selectedOption === "aadhar" && stepTwo && !checkedOption &&
         <ExpandableCard
         title="Mobile Number Verification"
         expanded={verifyNumber}
         setExpanded={setVerifyNumber}
         completed={(selectedOption === "aadhar" && stepThree)}
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
      (selectedOption === "aadhar" && stepThree && !checkedOption) ||
      (!checkedOption && stepOne && selectedOption === "phone_number") ? (
        <ExpandableCard
          title="Patient Details"
          expanded={userDetailsForm}
          setExpanded={setUserDeatilsForm}
        >
          <div className="patient-registration-form">
            {selectedOption === "aadhar" ? (
              <AadharPatientRegForm
                setUserCreated={setUserCreated}
                txnId={aadharData.txn_id}
                isForAabha={checkedOption}
              />
            ) : (
              <PatientRegistartionForm
                setUserCreated={setUserCreated}
                isForAabha={checkedOption}
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
