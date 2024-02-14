import {
  styled
} from "@mui/material";
import React, { useEffect, useState } from "react";
import ExpandableCard from "../../components/ExpandableCard";
import { useDispatch, useSelector } from "react-redux";
import {
  getAbhaProfile,
  // registerAADHAAR,
  registerAadhaarAbha,
  suggestAbhaAddress,
  verifyAadhaarAbhaOTP,
  // registerPhone,
  // verifyAadhaarOTP,
  // verifyAadhaarPhoneOTP,
  verifyAbhaNumber,
  verifyAbhaOTP,
  verifyAbhaUser,
  verifyPhoneOTP,
} from "./PatientRegistration.slice";
import PatientRegistartionForm from "../../components/PatientRegistrationForm";
import VerificationSelection from "../../components/VerificationSelection";
import AadhaarVerification from "../../components/AadhaarVerification";
import AadhaarConsent from "../../components/AadhaarConsent";
import PhoneVerification from "../../components/PhoneVerification";
import { apis } from "../../utils/apis";
import AadhaarPatientRegForm from "../../components/AadhaarPatientRegistrationForm";
import CustomSnackbar from "../../components/CustomSnackbar";
import CustomLoader from "../../components/CustomLoader";
import AbhaModeSelection from "../../components/AbhaModeSelection";

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
  const [selectedAbhaModeOption, setSelectedAbhaModeOption] = useState("link_abha");
  const [selectedAbhaRegistrationOption, setSelectedAbhaRegistrationOption] = useState("mobile");
  const [abhaRegistration, setAbhaRegistration] = useState(true);
  const [registration, setRegistration] = useState(true);
  const [verifyAadhaar, setVerifyAadhaar] = useState(true);
  const [verifyNumber, setVerifyNumber] = useState(true);
  const [userDetailsForm, setUserDeatilsForm] = useState(true);
  const [sixDigitOTP, setSixDigitOTP] = useState("");
  const [number, setNumber] = useState();
  const dataState = useSelector((state) => state);
  const aadhaarData = dataState?.PatientRegistartion?.registerAadhaar;
  const [aadhaarDataTxn, setAadhaarDataTxn] = useState("");
  const phoneData = dataState?.PatientRegistartion?.registerPhone;
  const [phoneDataTxn, setPhoneDataTxn] = useState("");
  const [stepAbha, setStepAbha] = useState(false);
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
  const [mobileNumber, setMobileNumber] = useState("");
  const [PhoneDisabled, setPhoneDisabled] = useState(true);
  const [patientAbhaData, setPatientAbhaData] = useState({});
  const [abhaSuggestionList, setAbhaSuggestionList] = useState([]);
  const [abhaSuggestionTxnId, setAbhaSuggestionTxnId] = useState("");
  const [aadhaarOTPseconds, setAadhaarOTPSeconds] = useState(-1);
  const [seconds, setSeconds] = useState(-1);
  const [open, setOpen] = useState(false);
  const userRole = sessionStorage?.getItem("userRole");
  const currentHospital = JSON.parse(sessionStorage?.getItem("selectedHospital"));
  const scroll = 'paper';

  const adminModes = [
    {
      label: "Abha",
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

  const abhaModes = [
    {
      label: "Create Abha",
      value: "create_abha",
    },
    {
      label: "Link Abha",
      value: "link_abha",
    },
  ];
  const registrationModes = [
    {
      label: "Mobile number",
      value: "mobile",
    },
    {
      label: "Aadhaar Number",
      value: "aadhaar",
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
    setAbhaRegistration(true);
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

  const handleAbhaModeChange = (event) => {
    if (selectedAbhaModeOption?.length) {
      setStepOne(false);
      setStepTwo(false);
      setStepThree(false);
      setStepFour(false);
    }
    setSelectedAbhaModeOption(event.target.value);
  };

  const handleAbhaRegistrationChange = (event) => {
    if (selectedAbhaRegistrationOption?.length) {
      setStepOne(false);
      setStepTwo(false);
      setStepThree(false);
      setStepFour(false);
    }
    setSelectedAbhaRegistrationOption(event.target.value);
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
  };

  const handleNumberChange = (event) => {
    const inputValue = event.target.value;
    setNumber(inputValue)
    // const numericValue = parseInt(inputValue);
    // if (isNaN(numericValue) || numericValue !== "") {
    //   console.log(numericValue);
    //   setNumber(numericValue)
    // }
    let new_Number_length = inputValue.length;
    if (new_Number_length > 10 || new_Number_length < 10) {
      // setErrorMessage("Please enter valid number")
      setIsMobileError(true);
      setPhoneDisabled(true);
    } else if (new_Number_length === 10) {
      setIsMobileError(false);
      setPhoneDisabled(false);
    }
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
        console.log("Form submitted:");
        if(selectedAbhaModeOption === "link_abha"){
          const payload = {
            "mode": "aadhaar",
            aadhaar: (aadhaar).replace(/\D/g, "")
          };
          const url = apis?.generateOTPAbha;
          dispatch(verifyAbhaNumber({url, payload})).then((res) => {
            setShowLoader(false);
            if (res?.error && Object.keys(res?.error)?.length > 0) {
              setErrorMessage("Aadhaar Number is not linked to any mobile number");
              setShowSnackbar(true);
              return;
            }
            if(res?.payload){
              setAadhaarDataTxn(res?.payload?.txn_id);
              setAadhaarOTPSeconds(60);
              setAadhaarOTP(true);
              setIsAadhaarValid(true);
            }
          });
        } else if(selectedAbhaModeOption === "create_abha"){
          const aadhaarPayload = {
            aadhaarNumber: (aadhaar).replace(/\D/g, "")
          };
          dispatch(registerAadhaarAbha(aadhaarPayload)).then((res) => {
            setShowLoader(false);
            if (res?.error && Object.keys(res?.error)?.length > 0) {
              setErrorMessage("Aadhaar Number is not linked to any mobile number");
              setShowSnackbar(true);
              return;
            }
            if(res?.payload){
              setAadhaarDataTxn(res?.payload?.txn_id);
              setAadhaarOTPSeconds(60);
              setAadhaarOTP(true);
              setIsAadhaarValid(true);
            }
          })
        }
         
      } else {
        console.log("Failed");
        setErrorMessage("Please enter a correct Aadhaar Number");
        setShowSnackbar(true);
      }
    } else if (type === "phone_number") {
      const mobile_pattern = new RegExp(/^[0-9]{10}$/);
      if (mobile_pattern.test(number)){
        setPhoneDisabled(false);
        setMobileNumber(number);
        let payload;
        let url;
        if(selectedOption === "aadhaar" && selectedAbhaModeOption === "link_abha"){
          payload ={
            "mode": "mobile",
            mobile: number,
          }
          url = apis?.generateOTPAbha;
        } else if(selectedOption === "phone_number"){
          payload ={
            mobileNumber: number,
          }
          url = apis?.restigerNumber;
        }
        dispatch(verifyAbhaNumber({ payload, url })).then((res) => {
          setShowLoader(false);
          // if (res?.error && Object.keys(res?.error)?.length > 0) {
          //   setShowSnackbar(true);
          //   return;
          // }
          const resData = res?.payload;
         
          if (resData?.txn_id && selectedOption === "aadhaar") {
            // setPhoneNumberUsed(resData?.mobileLinked);
            // setStepTwo(true);
            setPhoneDataTxn(resData?.txn_id);
            setSeconds(60);
            setPhoneNumberUsed(false);
            setPhoneDisabled(false);
          } else if(!resData?.txn_id && selectedOption === "aadhaar"){
            setErrorMessage("The phone number entered does not match with any of the records");
            setShowSnackbar(true);
            setStepTwo(true);
          } else if(selectedOption === "phone_number"){
            setPhoneDataTxn(resData?.txn_id);
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
      if(selectedAbhaModeOption === "link_abha"){
        const payload = {
          txnId: aadhaarDataTxn,
          mode: "aadhaar",
          otp: otp,
        };
        dispatch(verifyAbhaOTP(payload)).then((res) => {
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            // setErrorMessage("Please enter correct OTP");
            setShowSnackbar(true);
            setStepThree(false);
            return;
          } else {
            const profileParameters = {
              transactionId: res?.payload?.txnId,
              hipId: currentHospital?.hip_id,
            }
            dispatch(getAbhaProfile(profileParameters)).then(profileResponse => {
              if(profileResponse?.error && Object.keys(profileResponse?.error)?.length > 0) {
                setShowSnackbar(true);
                setStepThree(false);
                return;
              }
              else if(profileResponse?.payload?.ABHAProfile){
                setPatientAbhaData(profileResponse?.payload?.ABHAProfile);
                setStepThree(true);
              }
            })
          }
        });
      } else if(selectedAbhaModeOption === "create_abha"){
        const payload = {
          otp: otp,
          mobileNumber: number,
          txnId: aadhaarDataTxn,
          hipId: currentHospital?.hip_id,
        };
        dispatch(verifyAadhaarAbhaOTP(payload)).then((res) => {
          console.log(res);
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            // setErrorMessage("Please enter correct OTP");
            setShowSnackbar(true);
            setStepThree(false);
            return;
          }
          if(res?.payload?.ABHAProfile) {
            dispatch(suggestAbhaAddress(res?.payload?.txnId)).then((result) => {
              console.log(result);
              setPatientAbhaData(res?.payload?.ABHAProfile);
              setAbhaSuggestionList(result?.payload?.abhaAddressList);
              setAbhaSuggestionTxnId(result?.payload?.txnId);
              setStepThree(true);
            })
          }
        });
      }
      // if (stepTwo) {
      //   setStepThree(true);
      // }
    } else if (selectedOption === "phone_number" && type === "phone_number") {
      const payload = {
        txnId: phoneDataTxn,
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
      if(selectedAbhaModeOption === "link_abha"){
        const payload = {
          txnId: phoneDataTxn,
          mode: "mobile",
          otp: otp,
        };
        dispatch(verifyAbhaOTP(payload)).then((res) => {
          console.log("abhaOTP", res);
          if (res?.error && Object.keys(res?.error)?.length > 0) {
            setShowSnackbar(true);
            return;
          }
          else {
            const abhaUserPayload = {
              txnId: res?.payload?.txnId,
              abhaNumber: res?.payload?.accounts[0]?.ABHANumber,
              token: res?.payload?.token
            }
            dispatch(verifyAbhaUser(abhaUserPayload)).then((result) => {
              if (result?.error && Object.keys(result?.error)?.length > 0) {
                setShowSnackbar(true);
                return;
              }
              console.log("abhaUser", result);
              // if(result?.payload?.ABHAProfile) {
              //   setPatientAbhaData(result?.payload?.ABHAProfile);
              //   setStepThree(true);
              // }
              // else setStepTwo(true);
            })
          }
        });
      }
    }
  };

  useEffect(() => {
    if(stepAbha){
      setRegistration(false);
    }
    if (stepOne) {
      setRegistration(false);
      if (selectedOption === "aadhaar") {
        setAbhaRegistration(false);
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
        setRegistration(false);
        setAbhaRegistration(false);
        setVerifyAadhaar(true);
        setVerifyNumber(true);
      }

      if (selectedOption === "phone_number") {
        setVerifyNumber(false);
        setUserDeatilsForm(true);
      }
    }

    if (stepThree) {
      setRegistration(false);
      setAbhaRegistration(false);
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
        setPhoneDisabled(false);      
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
    if(selectedOption === "aadhaar") {
      setOpen(true);
      // setStepAbha(true);
    } else {
      setStepOne(true);
    }
  };

  const handleConfirmAbhaSelection = () => {
    if(selectedAbhaModeOption === "link_abha" && selectedAbhaRegistrationOption === "mobile") {
      setStepOne(true);
    } else if(selectedAbhaModeOption === "link_abha" && selectedAbhaRegistrationOption === "aadhaar") {
      setStepTwo(true);
    } else if(selectedAbhaModeOption === "create_abha") {
      setRegistration(false);
      setAbhaRegistration(false);
      setStepOne(true);
      setStepTwo(true);
    }
  };

  const handleConsentConfirmation = () => {
    setStepAbha(true);
    setRegistration(false);
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
        />
      <ExpandableCard
        title={`Mode of Registration ${
          selectedOption ? "|" + " " + selectedOption?.replace("_", " ") : ""
        }`}
        expanded={registration}
        setExpanded={setRegistration}
        completed={(selectedOption === "aadhaar" && stepAbha) || (selectedOption === "phone_number" && stepOne)}
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
      {(selectedOption === "aadhaar" && stepAbha && !checkedOption &&
       <ExpandableCard
        title="Create/Link Abha"
        expanded={abhaRegistration}
        setExpanded={setAbhaRegistration}
        completed={(selectedOption === "aadhaar" && stepOne) || (selectedOption === "aadhaar" && stepTwo)}
      >
        <AbhaModeSelection
          abhaModes={abhaModes}
          registrationModes={registrationModes}
          handleAbhaModeChange={handleAbhaModeChange}
          handleAbhaRegistrationChange={handleAbhaRegistrationChange}
          selectedAbhaModeOption={selectedAbhaModeOption}
          selectedAbhaRegistrationOption={selectedAbhaRegistrationOption}
          handleConfirmAbhaSelection={handleConfirmAbhaSelection}
        />
      </ExpandableCard>
       )}
      {(selectedOption === "aadhaar" && stepOne && !checkedOption &&
        <ExpandableCard
          title="Patient's Mobile Number"
          expanded={verifyNumber}
          setExpanded={setVerifyNumber}
          completed={(selectedOption === "aadhaar" && stepThree)}
        >
          <p style={{ marginTop: 0 }}>If the patient has an ABHA, kindly provide the linked mobile number. Otherwise, it is preferable to enter their Aadhaar-linked mobile number for easy registration</p>
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
           selectedAbhaModeOption={selectedAbhaModeOption}
         /> 
       </ExpandableCard>
      )}
      {selectedOption === "aadhaar" && stepTwo && !checkedOption && (
        <ExpandableCard
          title="AADHAAR number"
          expanded={verifyAadhaar}
          setExpanded={setVerifyAadhaar}
          completed={(selectedOption === "aadhaar" && stepThree)}
        >
          <p style={{ marginTop: 0 }}>No ABHA linked to the given mobile number. To proceed with registration, kindly enter the patient's Aadhaar number</p>
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
                txnId={aadhaarDataTxn || phoneDataTxn}
                isForAbha={checkedOption}
                patientAbhaData={patientAbhaData}
                abhaSuggestionList={abhaSuggestionList}
                setAbhaSuggestionTxnId={setAbhaSuggestionTxnId}
              />
            ) : (
              <PatientRegistartionForm
                setUserCreated={setUserCreated}
                isForAbha={checkedOption}
                txnId={phoneDataTxn} //{phoneData.txn_id}
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
