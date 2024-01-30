import React, { useState } from "react";
import { TextField, Button, Typography, styled, Checkbox } from "@mui/material";
import { useDispatch, useSelector } from "react-redux";
import { loginUser } from "../../app/auth.slice";
import { useNavigate } from "react-router-dom";
import CustomLoader from "../CustomLoader";

const LogInWrapper = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
  },

  ".login-heading": {
    marginBottom: "48px",
  },
  ".login-content": {
    [theme.breakpoints.down("md")]: {
      marginTop: "10%",
    },
  },
  ".login-form": {
    "& > .MuiFormControl-root": {
      marginBottom: "22px",
    },
  },
  ".login-btn": {
    "&.MuiButtonBase-root": theme.typography.primaryButton,
    marginTop: "10px"
  },
  ".login-title": {
    "&.MuiTypography-root": theme.typography.h1,
    [theme.breakpoints.down("md")]: {
      "&.MuiTypography-root": theme.typography.h4,
    },
  },
  ".login-subTitle": {
    "&.MuiTypography-root": theme.typography.h2,
    [theme.breakpoints.down("md")]: {
      "&.MuiTypography-root": theme.typography.body1,
    },
  },
  ".login-field-title": {
    "&.MuiTypography-root": theme.typography.body1,
    marginBottom: theme.spacing(2),
  },
  ".login-text-field": {
    "&.MuiFormControl-root > .MuiInputBase-root > input": {
      width: "410px",
      [theme.breakpoints.down("md")]: {
        width: "100%",
      },
    },
  },
}));

const LoginPage = (props) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showLoader, setShowLoader] = useState(false);
  const [isLoginError, setIsLoginError] = useState(false);
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const data = useSelector((state) => state?.auth?.user);

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSignIn = () => {
    setShowLoader(true);
    // Handle sign-in logic here
    // let urlencoded = new URLSearchParams();
    // urlencoded.append("username", email);
    // urlencoded.append("password", password);

    const payload = {
      username: email,
      password: password,
    };
    dispatch(loginUser(payload)).then((response) => {
      const resData = response?.payload;
      console.log(resData, "data");
      if (resData?.access_token) {
        sessionStorage.setItem("accesstoken", resData?.access_token);
        sessionStorage.setItem("userRole", resData?.user_role);
        sessionStorage.setItem("userName", resData?.username);
        let hipDetails = {};
        const hospitalDetails = resData?.hip_details;
        for (var key in hospitalDetails) {
          hipDetails.hip_id = key;
          hipDetails.name = hospitalDetails[key];
        }
        sessionStorage.setItem("selectedHospital", JSON.stringify(hipDetails));
        navigate("/dashboard");
        setShowLoader(false);
        // props?.setIndex(1);
      } else {
        setIsLoginError(true);
        setShowLoader(false);
      }
    });
  };

  return (
    <LogInWrapper>
      <CustomLoader
        open={showLoader}
      />
      <div className="login-content">
        <div className="login-heading">
          <Typography align="center" className="login-title">
            Welcome to CliniQ360
          </Typography>
          <Typography
            variant="subtitle1"
            align="center"
            className="login-subTitle"
          >
            Please enter your details to continue login
          </Typography>
        </div>

        <div className="login-form">
          <Typography className="login-field-title">Username</Typography>
          <TextField
            value={email}
            onChange={handleEmailChange}
            fullWidth
            variant="outlined"
            placeholder="Enter Your username"
            className="login-text-field"
          />
          <Typography>Password</Typography>
          <TextField
            value={password}
            onChange={handlePasswordChange}
            fullWidth
            variant="outlined"
            type="password"
            placeholder="Enter your password"
            className="login-text-field"
          />
          <span style={{ color: "red", marginBottom: "10px" }}>
            {isLoginError ? "Wrong username or password" : ""}
          </span>
          {/* <div>
              <div className="flex items-center space-x-2">
                <Checkbox />
                <span>Remember Me</span>
              </div>
              <a href="/forgot-password" className="text-blue-600">
                Forgot Password
              </a>
            </div> */}
          <Button
            variant="contained"
            onClick={handleSignIn}
            fullWidth
            className="login-btn"
          >
            Sign In
          </Button>
        </div>
      </div>
    </LogInWrapper>
  );
};

export default LoginPage;
