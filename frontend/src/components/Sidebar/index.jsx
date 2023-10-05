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
          padding: "120px 0 30px 0",
          minWidth: "100px",
        },
      }}
    >
      <List sx={{ margin: "0 auto" }}>
        <ListItem sx={{ marginBottom: "16px" }}>
          <img
            src={HomeIcon}
            alt="Home"
            onClick={() => redirectRoutes("/dashboard")}
            style={{ cursor: "pointer" }}
          />
        </ListItem>
        <ListItem sx={{ marginBottom: "16px" }}>
          <img
            src={PersonIcon}
            alt="person"
            onClick={() => redirectRoutes("/patient-list")}
            style={{ cursor: "pointer" }}
          />
        </ListItem>
        <ListItem sx={{ marginBottom: "16px" }}>
          <img
            src={AppointmentIcon}
            alt="appointment"
            onClick={() => redirectRoutes("/appointment-list")}
            style={{ cursor: "pointer" }}
          />
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Sidebar;
