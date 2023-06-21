import React from "react";
import { Button, styled } from "@mui/material";

const HeaderWrapper = styled("div")(({ theme }) => ({
  "&": {
    maxWidth: "1440px",
    margin: "0 auto",
    // backgroundColor: theme.primaryWhite,
  },
  ".header-container": {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "20px 80px",
  },
  ".header-logo-container": {
    display: "flex",
    alignItems: "center",
  },
  ".header-content": {
    display: "flex",
    alignItems: "center",
    gap: "12px",
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
      backgroundColor: theme.primaryGrey,
      color: theme.primaryBlack,
      padding: "8px 12px",
    },
  },
}));

const Header = () => {
  return (
    <HeaderWrapper>
      <div className="header-container">
        <div className="header-logo-container">
          {/* <img src="/path/to/logo.png" alt="Logo" className="h-8" /> */}
          <span className="logo">Cliniq360</span>
        </div>
        <div className="header-content">
          <span className="header-question-text">Have A Question?</span>
          <Button variant="contained" className="header-btn">
            Contact Us
          </Button>
        </div>
      </div>
    </HeaderWrapper>
  );
};

export default Header;
