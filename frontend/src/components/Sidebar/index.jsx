import React from "react";
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import HomeIcon from "../../assets/icons/home-icon.svg";
import PersonIcon from "../../assets/icons/person-icon.svg";
import AppointmentIcon from "../../assets/icons/appointment-icon.svg";
import { useState } from "react";

const Sidebar = ({ open, onClose, list }) => {
  const navigate = useNavigate();

  const redirectRoutes = (route) => {
    navigate(route);
  };
  const selectedIndex = JSON.parse(sessionStorage.getItem("PageSelected")) || 0;
  
  const handleListItemClick = (event, index) => {
    // setSelectedIndex(index);
    sessionStorage.setItem("PageSelected", index)
  };
  return (
    <Drawer
      anchor="left"
      variant="permanent"
      sx={{
        "& .MuiDrawer-paper": {
          backgroundColor: "#fff",
          padding: "80px 0 30px 0",
          minWidth: "60px",
        },
      }}
    >
      {/* sx={{ margin: "0 auto" }} */}
      <List sx={{ marginTop: "5px" }}>
      <ListItemButton sx={{ padding: "0 16px"}}
          selected={selectedIndex === 0}
          onClick={(event) => handleListItemClick(event, 0)}
        >
        <ListItem sx={{ padding: "0"}}
          onClick={() => redirectRoutes("/dashboard")}>
          <img
            src={HomeIcon}
            alt="Home"
            style={{ cursor: "pointer" }}
          /> <h3 className="page_name">Dashboard</h3>
        </ListItem>
        </ListItemButton>
        <ListItemButton sx={{ padding: "0 16px"}}
          selected={selectedIndex === 1}
          onClick={(event) => handleListItemClick(event, 1)}
        >
        <ListItem sx={{ padding: "5px 0"}}
            onClick={() => redirectRoutes("/patient-list")}>
          <img
            src={PersonIcon}
            alt="person"
            style={{ cursor: "pointer" }}
          /> <h3 className="page_name">Patient List</h3>
        </ListItem>
        </ListItemButton>
        <ListItemButton sx={{ padding: "0 16px"}}
          selected={selectedIndex === 2}
          onClick={(event) => handleListItemClick(event, 2)}
        >
        <ListItem sx={{ padding: "5px 0"}}
            onClick={() => redirectRoutes("/appointment-list")}>
          <img
            src={AppointmentIcon}
            alt="appointment"
            style={{ cursor: "pointer" }}
          /> <h3 className="page_name">Appointment List</h3>
        </ListItem>
        </ListItemButton>
      </List>
    </Drawer>
  );
};

export default Sidebar;