import React, { useEffect, useState } from "react";
import { Button, styled, Avatar, Menu, MenuItem } from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import { useNavigate } from "react-router-dom";
import { Person } from "@mui/icons-material";

// import DoctorProfilePage from "../../pages/DoctorProfilePage";

const HeaderWrapper = styled("div")(({ theme }) => ({
  "&": {
    width: "100%",
    // margin: "0 auto",
    backgroundColor: theme.palette.primaryWhite,
    zIndex: "1201",
    // height: "80px",
    // borderBottom: `1px solid ${theme.palette.tertiaryGrey}`,
    pposition: "-webkit-sticky",
    position: "sticky",
    top: 0,
  },
  ".header-container": {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "10px 32px",
    zIndex: "9999",
    [theme.breakpoints.down('sm')]: {
     padding: "10px 0"
    },
  },
  ".header-logo-container": {
    display: "flex",
    alignItems: "center",
    gap: theme.spacing(4),

    ".hospital-name": {
      "&": theme.typography.sectionBody2,
      [theme.breakpoints.down('sm')]: {
        fontSize: "16px",
      }
    },
  },
  ".logo": {
    fontFamily: "Red Hat Display",
    fontSize: "24px",
  },
  ".logo-login": {
    fontFamily: "Red Hat Display",
    fontSize: "24px",
    paddingRight: "16px",
    borderRight: "1px solid #9e9e9e",
    [theme.breakpoints.down('sm')]: {
      fontSize: "21px",
      paddingRight: "10px",
    }
  },
  ".header-content": {
    display: "flex",
  },
  // ".header-username-desktop": {
  //   [theme.breakpoints.up('sm')]: {
  //     alignItems: "center",
  //     display: "flex",
  //     marginRight: "10px",
  //   },
  // },
  ".header-question-text": {
    color: theme.palette.secondaryGrey,
    fontFamily: "Inter",
    fontWeight: "500",
    fontSize: "16px",
    lineHeight: "16px",
    marginRight: theme.spacing(8),
    [theme.breakpoints.down('sm')]: {
      marginRight: theme.spacing(0),
    },
  },
  ".header-no-login": {
    [theme.breakpoints.down('sm')]: {
      textAlign: "end"
    },
  }
}));

const ProfileIconWrapper = styled("div")({
  position: "relative",
  cursor: "pointer",
  display: "inline-block",
});

const ProfileIcon = styled(Avatar)(({ theme }) => ({
  backgroundColor: "#000",
  [theme.breakpoints.down('sm')]: {
    width: "35px",
    height: "35px",
  }
}));

const ProfileMenu = styled(Menu)(({ theme }) => ({
  position: "absolute",
  top: 10,
  [theme.breakpoints.down('sm')]: {
    top: 10,
    left: 11
  }
}));

const Header = () => {
  const accessToken = sessionStorage.getItem("accesstoken");
  const hospital = sessionStorage?.getItem("selectedHospital");
  const username = sessionStorage.getItem("userName");
  const currentHospital = JSON.parse(hospital);

  const [anchorEl, setAnchorEl] = useState(null);
  const navigate = useNavigate();

  const handleLogout = () => {
    sessionStorage.clear();
    // navigate("/login");
    window.location.replace("/login");
    handleClose();
  };

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <HeaderWrapper>
      <div className="header-container">
        <div className="header-logo-container">
          <span className={accessToken ? `logo-login` : `logo`}>Cliniq360</span>
          {accessToken && (
            <span className="hospital-name">{currentHospital?.name}</span>
          )}
        </div>
        {accessToken ? (
          <div className="header-content">
            <ProfileIconWrapper>
              <ProfileIcon onClick={handleClick}>
                <Person />
              </ProfileIcon>
              <ProfileMenu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
                className="profile_menu"
              >
                <MenuItem> {username} </MenuItem>
                <MenuItem onClick={() => navigate("/view-profile")}>View Profile</MenuItem>
                <MenuItem onClick={() => navigate("/forgot-password")}>Change Password</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </ProfileMenu>
            </ProfileIconWrapper>
          </div>
        ) : (
          <div className="header-no-login">
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