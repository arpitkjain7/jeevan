import React, { useEffect, useState } from "react";
import StepperComponent from "../../components/CustomStepper";
import LoginPage from "../../components/Login";
import HospitalList from "../HospitalList";

function SignInPage() {
  const [index, setIndex] = useState(0);
  useEffect(() => {
    const token = localStorage.getItem("accesstoken");
    if (token) {
      setIndex(1);
    } else {
      setIndex(0);
    }
  }, []);
  
  return (
    <>
      {index === 0 && <LoginPage setIndex={setIndex} />}
      {index === 1 && <HospitalList setIndex={setIndex} />}
    </>
  );
}

export default SignInPage;
