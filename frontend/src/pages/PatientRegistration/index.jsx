import {
  Button,
  Checkbox,
  FormControlLabel,
  IconButton,
  InputAdornment,
  TextField,
  Typography,
  styled,
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
  verifyPhoneOTP,
} from "./PatientRegistration.slice";
import PatientRegistartionForm from "../../components/PatientRegistrationForm";
import VerificationSelection from "../../components/VerificationSelection";
import AadharVerification from "../../components/AadharVerification";
import PhoneVerification from "../../components/PhoneVerification";
import RegisterationConfirmation from "../../components/RegistrationConfirmation";

const PatientRegisterWrapper = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    flexDirection: "column",
    gap: "40px",
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
}));
const PatientRegistration = () => {
  const [selectedOption, setSelectedOption] = useState(null);
  const [checkedOption, setCheckedOption] = useState(null);
  const [registration, setRegistration] = useState(true);
  const [verifyAadhar, setVerifyAadhar] = useState(true);
  const [verifyNumber, setVerifyNumber] = useState(true);
  const [userDetailsForm, setUserDeatilsForm] = useState(true);
  const [sixDigitOTP, setSixDigitOTP] = useState("");
  const [number, setNumber] = useState("");
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

  const modes = [
    {
      label: "Aadhar",
      value: "aadhar",
    },
    {
      label: "Phone Number",
      value: "phone_number",
    },
  ];

  const handleOptionChange = (event) => {
    console.log(event.target.value);
    setSelectedOption(event.target.value);
    setStepOne(true);
  };

  const handleOptionCheck = (event) => {
    setCheckedOption((prevValue) => !prevValue);
  };

  const handleAadharChange = (event) => {
    const inputValue = event.target.value;
    const numericValue = parseInt(inputValue);
    // Check if the input value is a valid number or empty string
    if (!isNaN(numericValue) || inputValue === "") {
      setAadhar(inputValue);
    }
  };

  const handleNumberChange = (event) => {
    const inputValue = event.target.value;
    const numericValue = parseInt(inputValue);
    // Check if the input value is a valid number or empty string
    if (!isNaN(numericValue) || inputValue === "") {
      setNumber(inputValue);
    }
  };

  const handleSubmit = (type) => {
    // Handle the form submission
    if (type === "aadhar") {
      console.log("Form submitted:", aadhar);
      const payload = {
        aadhaarNumber: aadhar,
      };
      dispatch(registerAADHAR(payload)).then((res) => {
        console.log(res?.payload);
        setStepTwo(true);
      });
    } else if (type === "phone_number") {
      console.log("Form submitted:", number);
      const payload = {
        mobileNumber: number,
      };
      dispatch(registerPhone(payload)).then((res) => console.log(res?.payload));
    }
  };

  const verifyOTP = (otp, type) => {
    if (selectedOption === "aadhar") {
      const payload = {
        txnId: aadharData?.txn_id,
        otp: otp,
      };
      dispatch(verifyAadharOTP(payload)).then((res) => {
        console.log(res.payload);
        setStepTwo(true);
      });
    } else if (selectedOption === "phone_number") {
      const payload = {
        txnId: phoneData?.txn_id,
        otp: otp,
      };
      dispatch(verifyPhoneOTP(payload)).then((res) => {
        console.log(res.payload);
        setStepTwo(true);
      });
    }
  };

  useEffect(() => {
    if (stepOne) {
      setRegistration(false);
    }

    if (stepTwo) {
      setUserDeatilsForm(false);

      if (selectedOption === "aadhar") {
        setVerifyAadhar(false);
        setVerifyNumber(false);
      }

      if (selectedOption === "phone_number") {
        setVerifyAadhar(false);
      }
    }

    if (stepThree) {
      setRegistration(false);
      setVerifyAadhar(false);
      setUserDeatilsForm(false);
    }
  }, [stepOne, stepTwo, setStepThree, stepFour, selectedOption]);

  console.log(
    (selectedOption === "aadhar" && stepTwo && !checkedOption) ||
      (selectedOption === "phone_number" && stepOne && !checkedOption),
    "check"
  );

  return (
    <PatientRegisterWrapper>
      <ExpandableCard
        title={`Mode of Registration ${
          selectedOption ? "|" + " " + selectedOption?.replace("_", " ") : ""
        }`}
        expanded={registration}
        setExpanded={setRegistration}
        completed={stepOne}
      >
        <VerificationSelection
          modes={modes}
          handleOptionChange={handleOptionChange}
          selectedOption={selectedOption}
          checkedOption={checkedOption}
          handleOptionCheck={handleOptionCheck}
        />
      </ExpandableCard>
      {selectedOption === "aadhar" && stepOne && !checkedOption && (
        <ExpandableCard
          title="AADHAR Verfication"
          expanded={verifyAadhar}
          setExpanded={setVerifyAadhar}
          completed={stepTwo}
        >
          <AadharVerification
            aadhar={aadhar}
            handleAadharChange={handleAadharChange}
            handleSubmit={handleSubmit}
            setSixDigitOTP={setSixDigitOTP}
            verifyOTP={verifyOTP}
          />
        </ExpandableCard>
      )}
      {(selectedOption === "aadhar" && stepTwo && !checkedOption) ||
      (selectedOption === "phone_number" && stepOne && !checkedOption) ? (
        <ExpandableCard
          title="Mobile Number Verification"
          expanded={verifyNumber}
          setExpanded={setVerifyNumber}
          completed={
            (selectedOption === "aadhar" && stepThree) ||
            (selectedOption === "phone_number" && stepTwo)
          }
        >
          <PhoneVerification
            number={number}
            handleNumberChange={handleNumberChange}
            handleSubmit={handleSubmit}
            setSixDigitOTP={setSixDigitOTP}
            verifyOTP={verifyOTP}
          />
        </ExpandableCard>
      ) : null}
      {(selectedOption === "phone_number" && stepTwo && !checkedOption) ||
      (selectedOption === "aadhar" && stepThree && !checkedOption) ||
      (checkedOption && stepTwo) ? (
        <ExpandableCard
          title="Patient Details"
          expanded={userDetailsForm}
          setExpanded={setUserDeatilsForm}
        >
          <div className="patient-registration-form">
            <PatientRegistartionForm setUserCreated={setUserCreated} />
          </div>
        </ExpandableCard>
      ) : null}
      {userCreated && (
        <ExpandableCard
          title="SucessFully Created"
          expanded={userDetailsForm}
          setExpanded={setUserDeatilsForm}
        >
          <div className="patient-registration-form">
            {/* <RegisterationConfirmation /> */}
          </div>
        </ExpandableCard>
      )}
    </PatientRegisterWrapper>
  );
};

export default PatientRegistration;