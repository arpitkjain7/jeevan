import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import {
  styled,
  Box,
  CssBaseline,
  Toolbar,
  Drawer,
} from "@mui/material";
import Header from "../components/Header";
import "./global.scss";
import SignInPage from "../pages/SignIn";
import Dashboard from "../pages/Dashboard";
import PatientPage from "../pages/PatientPage";
import Sidebar from "../components/Sidebar";
import PatientRegistration from "../pages/PatientRegistration";
import AppointmentPage from "../pages/AppointmentPage";
import CreateAppointment from "../pages/CreateAppointment";
import PatientEMRDetails from "../pages/DoctorPage/EMRPage";
import RegisterationConfirmation from "../components/RegistrationConfirmation";
import PatientDetails from "../pages/PatientDetails";
import ConsentDocumentPage from "../pages/ConsentDocumentPage";
import MuiDrawer from "@mui/material/Drawer";
import MuiAppBar from "@mui/material/AppBar";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import ForgotPasswordPage from "../pages/ForgotPassword";
import DoctorProfilePage from "../pages/DoctorProfilePage";

const drawerWidth = 235;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
});

const openedMobileMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  // width: `calc(${theme.spacing(9)} + 20px)`,
  [theme.breakpoints.up("md")]: {
    width: `calc(${theme.spacing(11)} + 20px)`,
  },
});

const closedMobileMixin = (theme) => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  width: "0px",
});

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  // necessary for content to be below app bar
  ...theme.mixins.toolbar,
}));

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const DesktopDrawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  width: drawerWidth,
  flexShrink: 0,
  whiteSpace: "nowrap",
  boxSizing: "border-box",
  ...(open && {
    [theme.breakpoints.up("md")]: {
      ...openedMixin(theme),
      "& .MuiDrawer-paper": openedMixin(theme),
    },
    [theme.breakpoints.down("md")]: {
      ...openedMobileMixin(theme),
      "& .MuiDrawer-paper": openedMobileMixin(theme),
    },
  }),
  ...(!open && {
    [theme.breakpoints.up("md")]: {
      ...closedMixin(theme),
      "& .MuiDrawer-paper": closedMixin(theme),
    },
    [theme.breakpoints.down("md")]: {
      ...closedMobileMixin(theme),
      "& .MuiDrawer-paper": closedMobileMixin(theme),
    },
  }),
}));

function App() {
  const isMobile = window.innerWidth < 600;
  // const dataState = useSelector((state) => state);
  const [sidebarState, setSidebarState] = React.useState(false);

  const toggleDrawer = (open) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }

    setSidebarState(open);
  };

  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen((prevCheck) => !prevCheck);
  };

  const isAuthenticated = sessionStorage.getItem("accesstoken");

  // useEffect(() => {
  //   console.log("reduxStore", dataState);
  // }, [dataState]);

  return (
    <Router>
      {!isMobile && (
        <>
          <Box>
            {isAuthenticated ? (
              <>
                <CssBaseline />
                <AppBar
                  position="fixed"
                  style={{ backgroundColor: "#fff", color: "#000" }}
                >
                  <Toolbar>
                    <IconButton
                      color="inherit"
                      aria-label="open drawer"
                      onClick={handleDrawerOpen}
                      edge="start"
                      sx={{ marginLeft: 1 }}
                    >
                      <MenuIcon />
                    </IconButton>
                    <Header />
                  </Toolbar>
                </AppBar>
              </>
            ) : (
              <Header />
            )}
          </Box>

          <Box display={{ xs: "block", md: "flex" }}>
            <CssBaseline />
            {isAuthenticated && (
              <DesktopDrawer variant="permanent" open={open}>
                <DrawerHeader></DrawerHeader>
                <Divider />
                <Sidebar />
              </DesktopDrawer>
            )}

            <Box
              component="main"
              style={{ flexGrow: 1, backgroundColor: "#f0f0f0a8" }}
              sx={{ overflow: "auto" }}
              p={{ xs: 1, md: 1 }}
            >
              <DrawerHeader />
              {/* <div style={{ flex: 1, padding: "46px 32px" }}> */}
              <Routes>
                <Route path="/login" element={<SignInPage />} />
                {isAuthenticated ? (
                  <>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/patient-list" element={<PatientPage />} />
                    <Route
                      path="/patient-registration"
                      element={<PatientRegistration />}
                    />
                    <Route
                      path="/appointment-list"
                      element={<AppointmentPage />}
                    />
                    <Route
                      path="/create-appointment"
                      element={<CreateAppointment />}
                    />
                    <Route
                      path="/patient-emr"
                      element={<PatientEMRDetails />}
                    />
                    <Route
                      path="/registered-patient"
                      element={<RegisterationConfirmation />}
                    />
                    <Route
                      path="/patient-details"
                      element={<PatientDetails />}
                    />
                    <Route
                      path="/consent-detail"
                      element={<ConsentDocumentPage />}
                    />
                  </>
                ) : (
                  <Route path="*" element={<SignInPage />} />
                )}
                {/* <Route path="/view-profile" element={<DoctorProfilePage />} /> */}
                <Route path="/view-profile/dr-prasad" element={<DoctorProfilePage />} />
                <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                <Route path="/" element={<SignInPage />} />
              </Routes>
              {/* </div> */}
            </Box>
          </Box>
        </>
      )}
      {isMobile && (
        <>
          <Box>
            {isAuthenticated ? (
              <>
                <CssBaseline />
                <AppBar
                  position="fixed"
                  style={{ backgroundColor: "#fff", color: "#000" }}
                >
                  <Toolbar>
                    <IconButton
                      color="inherit"
                      aria-label="open drawer"
                      onClick={toggleDrawer(true)}
                      edge="start"
                      sx={{ marginLeft: 1 }}
                    >
                      <MenuIcon />
                    </IconButton>
                    <Header />
                  </Toolbar>
                </AppBar>
              </>
            ) : (
              <Header />
            )}
          </Box>

          <Box
            display={{ xs: "block", md: "flex" }}
            onClick={toggleDrawer(false)}
            onKeyDown={toggleDrawer(false)}
          >
            <CssBaseline />
            {isAuthenticated && (
              <Drawer open={sidebarState}>
                <DrawerHeader></DrawerHeader>
                <Divider />
                <Sidebar />
              </Drawer>
            )}

            <Box
              component="main"
              style={{ backgroundColor: "#f0f0f0a8" }}
              p={{ xs: 1, md: 3 }}
            >
              <DrawerHeader />
              <Routes>
                <Route path="/login" element={<SignInPage />} />
                {isAuthenticated ? (
                  <>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/patient-list" element={<PatientPage />} />
                    <Route
                      path="/patient-registration"
                      element={<PatientRegistration />}
                    />
                    <Route
                      path="/appointment-list"
                      element={<AppointmentPage />}
                    />
                    <Route
                      path="/create-appointment"
                      element={<CreateAppointment />}
                    />
                    <Route
                      path="/patient-emr"
                      element={<PatientEMRDetails />}
                    />
                    <Route
                      path="/registered-patient"
                      element={<RegisterationConfirmation />}
                    />
                    <Route
                      path="/patient-details"
                      element={<PatientDetails />}
                    />
                    <Route
                      path="/consent-detail"
                      element={<ConsentDocumentPage />}
                    />
                  </>
                ) : (
                  <Route path="*" element={<SignInPage />} />
                )}
                <Route path="/view-profile/dr-prasad" element={<DoctorProfilePage />} />
                <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                <Route path="/" element={<SignInPage />} />
              </Routes>
            </Box>
          </Box>
        </>
      )}
    </Router>
  );
}

export default App;
