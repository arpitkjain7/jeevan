import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { makeStyles, styled } from "@mui/material";
import Header from "../components/Header";
import "./global.scss";
import SignInPage from "../pages/SignIn";
import HospitalList from "../pages/HospitalList";
import ProtectedRoute from "../routes/ProtectedRoute";

const Wrapper = styled("div")(({ theme }) => ({
  "&": {
    maxWidth: "1440px",
    margin: "0 auto",
  },
}));

function App() {
  return (
    <div>
      <Header />
      <Wrapper>
        <Router>
          <Switch>
            <Route exact path="/login" component={SignInPage} />
            <ProtectedRoute exact path="/hospitals" component={HospitalList} />
            <Route path="/" component={SignInPage} />
            {/* <ProtectedRoute path="/about" component={Patient} />
          <ProtectedRoute path="/contact" component={Appointment} /> */}
          </Switch>
        </Router>
      </Wrapper>
    </div>
  );
}

export default App;
