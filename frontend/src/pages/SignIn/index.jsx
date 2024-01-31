import React, { useEffect, useState } from "react";
import StepperComponent from "../../components/CustomStepper";
import LoginPage from "../../components/Login";
import HospitalList from "../HospitalList";
import { styled } from "@mui/material";
import banner from "../../assets/sidebar-login.png";

const LoginPageWrapper = styled("div")(({ theme }) => ({
  "&": {
    // paddingTop: theme.spacing(0),
    height: "70vh",
  },
  ".login-page-container": {
    display: "flex",
    gap: theme.spacing(10),
    height: "100%",
    maxWidth: "1440px",
    margin: "0 50px",
    [theme.breakpoints.down('sm')]: {
      margin: "0",
      display: "block"
    },
  },
  ".hospital-page-container":{
    paddingTop: theme.spacing(20)
  },
  ".login-left-banner": {
    backgroundColor: "#0089E9",
    backgroundImage: `url(${banner})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    maxWidth: "550px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    padding: theme.spacing(8),
    flex: "0.5",
  },
  ".sign-in-image": {
    height: "100%",
  },
  ".login-right-form": {
    flex: "0.5",
    margin: "0 auto",
  },
}));

const LogoText = styled("h1")(({ theme }) => ({
  fontFamily: "Red Hat Display",
  fontSize: "28px",
  fontWeight: 400,
  color: theme.palette.primaryWhite,
  [theme.breakpoints.down('sm')]: {
    fontSize: "20px"
  },
}));

const BannerInfo = styled("h1")(({ theme }) => ({
  "&": theme.typography.bannerText,
  margin: 0,
  [theme.breakpoints.down('md')]: {
    fontSize: "24px"
  },
}));

const StyledDiv = styled("div")``;

function SignInPage() {
  const [index, setIndex] = useState(0);
  useEffect(() => {
    const token = sessionStorage.getItem("accesstoken");
    if (token) {
      setIndex(1);
    } else {
      setIndex(0);
    }
  }, []);

  return (
    <LoginPageWrapper>
      <div className="login-page-container">
         <div className="login-left-banner">
           <LogoText>cliniQ360</LogoText>
           <BannerInfo>
             Elevate patient care with a seamless experience and innovative
             technology
           </BannerInfo>
         </div>
         <div className="login-right-form">
          <LoginPage setIndex={setIndex} />
         </div>
       </div>
      {/* {index == 0 ? (
        <div className="login-page-container">
         <div className="login-left-banner">
           <LogoText>cliniQ360</LogoText>
           <BannerInfo>
             Elevate patient care with a seamless experience and innovative
             technology
           </BannerInfo>
         </div>
         <div className="login-right-form">
           {index === 0 && <LoginPage setIndex={setIndex} />}
         </div>
       </div>
      ) : (
        <div className="login-page-container hospital-page-container">
          <div className="login-left-banner">
            <LogoText>cliniQ360</LogoText>
            <BannerInfo>
              Elevate patient care with a seamless experience and innovative
              technology
            </BannerInfo>
          </div>
          <div className="login-right-form">
            {index === 1 && <HospitalList setIndex={setIndex} />}
          </div>
        </div>
      )} */}
    </LoginPageWrapper>
  );
}

export default SignInPage;
