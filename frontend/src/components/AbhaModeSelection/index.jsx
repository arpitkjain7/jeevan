import {
    Button,
    styled,
    ToggleButtonGroup,
    ToggleButton
  } from "@mui/material";
  import React from "react";
  
  const VerificationSelectionWrapper = styled("div")(({ theme }) => ({
    ".select-mode": {
      display: "flex",
      alignItems: "center",
      gap: "24px",
      paddingBottom: "40px",
      // borderBottom: `1px solid ${theme.palette.primaryGrey}`,
      [theme.breakpoints.down('sm')]: {
        paddingBottom: "20px",
        gap: "12px"
      },
    },
    ".form-radio-group": {
      width: "300px",
      padding: theme.spacing(4),
      border: `1px solid ${theme.palette.tertiaryGrey}`,
      borderRadius: theme.spacing(2),
      [theme.breakpoints.down('sm')]: {
        width: "100%",
        padding: "8px",
      },
      "& > label": theme.typography.body1,
    },
    ".radio-input": { 
      marginRight: theme.spacing(4),
        [theme.breakpoints.down('sm')]: {
          marginRight: theme.spacing(2),
        }, 
      },
    ".select-header-container": {
      display: "flex",
      alignItems: "center",
      gap: theme.spacing(4),
      borderTop: `1px solid ${theme.palette.primaryGrey}`,
      marginBottom: theme.spacing(4),
    },
    ".select-header": {
      marginTop: theme.spacing(8),
      padding: theme.spacing(4),
      backgroundColor: theme.palette.secondaryOpacityBlue,
      borderRadius: theme.spacing(2),
      border: `1px solid ${theme.palette.secondaryBlue}`,
      [theme.breakpoints.down('sm')]: {
        marginTop: "22px",
      },
    },
    ".form-control-checkbox": {
      "&.MuiFormControlLabel-root": {
        display: "flex",
        alignItems: "center",
        "& > .MuiButtonBase-root": {
          // width: "24px",
          // height: "24px",
        },
      },
  
      "& > .MuiTypography-root": theme.typography.body1,
    },
    ".form-control-subtext": {
      "&.MuiTypography-root": {
        fontFamily: "Inter",
        fontWeight: "500",
        fontSize: "14px",
        lineHeight: "160%",
        marginBottom: "4px",
      },
    },
    ".confirm-verification-btn": {
      "&.MuiButtonBase-root": theme.typography.primaryButton,
    },
  }));
  
  const AbhaModeSelection = ({
    abhaModes,
    registrationModes,
    handleAbhaModeChange,
    handleAbhaRegistrationChange,
    selectedAbhaModeOption,
    selectedAbhaRegistrationOption,
    handleConfirmAbhaSelection,
  }) => {
    return (
      <VerificationSelectionWrapper>
        <div className="select-mode">
          {abhaModes?.map((item, index) => {
            return (
              <div className="form-radio-group" key={index}>
                <label>
                  <input
                    type="radio"
                    value={item?.value}
                    checked={selectedAbhaModeOption === item?.value}
                    onChange={handleAbhaModeChange}
                    className="radio-input"
                   
                  />
                  {item?.label}
                </label>
              </div>
            );
          })}
        </div>
        {selectedAbhaModeOption === "link_abha" && (
          <div className="select-mode">               
            <ToggleButtonGroup
              color="primary"
              exclusive
              size="large"
              value={selectedAbhaRegistrationOption}
              onChange={handleAbhaRegistrationChange}
              aria-label="Platform"
            >
              {registrationModes?.map((item, index) => {
                return(
                <ToggleButton value={item?.value} key={index} style={{ fontWeight: 500, border: "1px solid #a2a2a2" }}>
                  {item?.label}
                </ToggleButton>
                )
            })}
            </ToggleButtonGroup>
          </div>
        )}
        <div>
          <Button
            className="confirm-verification-btn"
            onClick={handleConfirmAbhaSelection}
            // disabled={!selectedOption}
          >
            Continue
          </Button>
        </div>
      </VerificationSelectionWrapper>
    );
  }
  
  export default AbhaModeSelection;
  