import { createTheme } from "@mui/material/styles";

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
    secondaryOpacityBlue : "rgba(5, 97, 160, 0.10)"
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
    h3: {
      fontSize: "18px",
      fontFamily: "Source Sans Pro",
      fontWeight: 600,
      lineHeight: "150%",
      color: "#171717",
    },
    successText:{
      fontSize: "20px",
      fontFamily: "Source Sans Pro",
      fontWeight: 600,
      lineHeight: "150%",
      color: "#00A91C",
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
    body4:{
      fontSize: "14px",
      fontWeight: 400,
      lineHeight: "150%",
      fontFamily: "Source Sans Pro",
      color: "#5A5A5A",
    },
    link: {
      fontSize: "16px",
      fontWeight: 400,
      lineHeight: "150%",
      fontFamily: "Source Sans Pro",
      color: "#0561A0",
      textDecoration: "underline",
    },
    customKeys:{
      fontSize: "16px",
      fontWeight: 400,
      lineHeight: "150%",
      fontFamily: "Source Sans Pro",
      color: "#5a5a5a",
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
      border: "none",
    },
    // Add more typography styles as needed
  },
  spacing: 4,
});

export default theme;
