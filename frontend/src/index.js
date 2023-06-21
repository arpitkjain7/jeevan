import React from "react";
import ReactDOM from "react-dom/client";
import "./index.scss";
import App from "./app";
import { ThemeProvider } from "@emotion/react";
import { themes } from "./styles/theme";
import { Provider } from "react-redux";
import store from "./store";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Provider store={store}>
    <React.StrictMode>
      <ThemeProvider theme={themes}>
        <App />
      </ThemeProvider>
    </React.StrictMode>
  </Provider>
);
