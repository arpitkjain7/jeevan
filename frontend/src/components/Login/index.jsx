import React, { useState } from "react";
import { TextField, Button, Typography, styled, Checkbox } from "@mui/material";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";

const LogInWrapper = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  ".login-heading": {
    marginBottom: "48px",
  },
  ".login-content": {
    marginTop: "10%",
  },
  ".login-form": {
    "& > .MuiFormControl-root": {
      marginBottom: "32px",
    },
  },
  ".login-btn": {
    "&.MuiButtonBase-root": {
      backgroundColor: theme.primaryBlack,
    },
  },
}));

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory();

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSignIn = () => {
    // Handle sign-in logic here
    console.log("Signing in...");
    history.push("/hospitals");
  };

  return (
    <LogInWrapper>
      <div className="login-content">
        <div className="login-heading">
          <Typography variant="h2" align="center">
            Login
          </Typography>
          <Typography variant="subtitle1" align="center">
            Please enter your detail
          </Typography>
        </div>

        <div className="login-form">
          <TextField
            value={email}
            onChange={handleEmailChange}
            fullWidth
            variant="outlined"
            placeholder="UserName"
          />
          <TextField
            value={password}
            onChange={handlePasswordChange}
            fullWidth
            variant="outlined"
            type="password"
            placeholder="Password"
          />
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
