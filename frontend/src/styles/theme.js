import { createTheme, ThemeOptions } from "@mui/material";

const theme = createTheme({
  palette: {
    primaryBlack: "#171717",
    primaryWhite: "#ffffff",
    primaryRed: "#ff0000",
    primaryGrey: "#D2D2D2",
    secondaryGrey: " #5A5A5A",
    tertiaryGrey: "#9E9E9E",
    primaryBlue: "#0089E9",
    secondaryBlue: "#0561A0",
    primaryOpacityBlue: "rgba(0, 137, 233, 0.3)",
    // Add more colors as needed
  },
  typography: {
    fontFamily: ["Arial", "Helvetica", "sans-serif"].join(","),
    h1: {
      fontSize: "36px",
      fontFamily: "Source Sans Pro",
      fontWeight: 400,
      lineHeight: "150%",
      color: "#171717",
    },
    h2: {
      fontSize: "18px",
      fontFamily: "Source Sans Pro",
      fontWeight: 400,
      lineHeight: "150%",
      color: "#5A5A5A",
    },
    body1: {
      fontSize: "16px",
      fontWeight: 400,
      lineHeight: "150%",
      fontFamily: "Source Sans Pro",
      color: "#171717",
    },
    body2: {
      fontSize: "16px",
      fontWeight: 600,
      lineHeight: "150%",
      fontFamily: "Source Sans Pro",
      color: "#171717",
      textTransform: "capitalize",
    },
  body3: {
      fontSize: "14px",
      fontWeight: 400,
      lineHeight: "150%",
      fontFamily: "Source Sans Pro",
      color: "#171717",
    },
    link: {
      fontSize: "16px",
      fontWeight: 400,
      lineHeight: "150%",
      fontFamily: "Source Sans Pro",
      color: "#0561A0",
      textDecoration: "underline",
    },
    primaryButton: {
      padding: "14px 16px",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      borderRadius: "4px",
      backgroundColor: "#0089E9",
      color: "#ffffff",
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      border: "none"
    },
    // Add more typography styles as needed
  },
  spacing: 4,
});

export const themes = createTheme(theme);
