import React from "react";
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import HomeIcon from "../../assets/icons/home-icon.svg";
import PersonIcon from "../../assets/icons/person-icon.svg";
import AppointmentIcon from "../../assets/icons/appointment-icon.svg";

const Sidebar = ({ open, onClose, list }) => {
  const navigate = useNavigate();

  const redirectRoutes = (route) => {
    navigate(route);
  };
  return (
    <Drawer
      anchor="left"
      variant="permanent"
      sx={{
        "& .MuiDrawer-paper": {
          backgroundColor: "#fff",
          padding: "100px 0 30px 0",
          minWidth: "80px",
        },
      }}
    >
      <List sx={{ margin: "0 auto" }}>
        <ListItem sx={{ marginBottom: "16px" }}
          onClick={() => redirectRoutes("/dashboard")}>
          <img
            src={HomeIcon}
            alt="Home"
            style={{ cursor: "pointer" }}
          /> 
        </ListItem>
        <ListItem sx={{ marginBottom: "16px" }}
            onClick={() => redirectRoutes("/patient-list")}>
          <img
            src={PersonIcon}
            alt="person"
            style={{ cursor: "pointer" }}
          />
        </ListItem>
        <ListItem sx={{ marginBottom: "16px" }}
            onClick={() => redirectRoutes("/appointment-list")}>
          <img
            src={AppointmentIcon}
            alt="appointment"
            style={{ cursor: "pointer" }}
          />
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Sidebar;