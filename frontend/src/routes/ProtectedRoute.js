import React from "react";
import { useSelector } from "react-redux";
import { Route, Redirect, useNavigate } from "react-router-dom";

const ProtectedRoute = ({ component: Component, ...rest }) => {
  const userData = useSelector((state) => state?.auth?.user);
  const isAuthenticated = userData?.accesstoken;
  const navigate = useNavigate();

  return (
    <Route
      {...rest}
      render={(props) =>
        isAuthenticated ? <Component {...props} /> : <navigate to="/" />
      }
    />
  );
};

export default ProtectedRoute;
