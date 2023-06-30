import React from "react";
import { Button, styled } from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import { useNavigate } from "react-router-dom";

const HeaderWrapper = styled("div")(({ theme }) => ({
  "&": {
    // maxWidth: "1440px",
    // margin: "0 auto",
    backgroundColor: theme.primaryWhite,
    zIndex: "9999",
    height: "80px",
    borderBottom: `1px solid ${theme.tertiaryGrey}`,
  },
  ".header-container": {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "20px 32px",
    zIndex: "9999",
  },
  ".header-logo-container": {
    display: "flex",
    alignItems: "center",
  },
  ".header-content": {
    display: "flex",
    alignItems: "center",
    gap: "42px",
  },
  ".logo": {
    fontFamily: "Red Hat Display",
    fontSize: "24px",
  },
  ".header-question-text": {
    color: theme.secondaryGrey,
    fontFamily: "Inter",
    fontWeight: "500",
    fontSize: "16px",
    lineHeight: "16px",
  },
  ".header-btn": {
    "&.MuiButtonBase-root": {
      border: `1px solid ${theme.primaryBlack}`,
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      backgroundColor: theme.primaryBlack,
      color: theme.primaryWhite,
      padding: "8px 32px",
    },
  },
}));

const Header = () => {
  const accessToken = localStorage.getItem("accesstoken");
  const navigate = useNavigate();
  return (
    <HeaderWrapper>
      <div className="header-container">
        <div className="header-logo-container">
          {/* <img src="/path/to/logo.png" alt="Logo" className="h-8" /> */}
          <span className="logo">Cliniq360</span>
        </div>
        {accessToken ? (
          <div className="header-content">
            {" "}
            <Button
              variant="contained"
              className="header-btn"
              onClick={() => navigate("/patient-registration")}
            >
              Register Now
            </Button>
            <PersonIcon sx={{ fontSize: 40, width: 40, height: 40 }} />
          </div>
        ) : (
          <div className="header-content">
            {" "}
            <span className="header-question-text">Have A Question?</span>
            <Button variant="contained" className="header-btn">
              Contact Us
            </Button>
          </div>
        )}
      </div>
    </HeaderWrapper>
  );
};

export default Header;
