import { Checkbox, FormControlLabel, Typography, styled } from "@mui/material";
import React from "react";

const VerificationSelectionWrapper = styled("div")(({ theme }) => ({
  ".select-mode": {
    display: "flex",
    alignItems: "center",
    gap: "24px",
    paddingBottom: "40px",
    borderBottom: `1px solid ${theme.palette.primaryGrey}`,
  },
  ".form-radio-group": {
    width: "300px",
    padding: theme.spacing(4),
    border: `1px solid ${theme.palette.tertiaryGrey}`,
    borderRadius: theme.spacing(2),

    "& > label": theme.typography.body1 ,
  },
  ".radio-input": { marginRight: theme.spacing(4) },

  ".select-header": {
    marginTop: theme.spacing(4),
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
    "&.MuiTypography-root": theme.typography.body3,
    marginBottom: theme.spacing(4),
  },
}));

function VerificationSelection({
  modes,
  handleOptionChange,
  selectedOption,
  checkedOption,
  handleOptionCheck,
}) {
  return (
    <VerificationSelectionWrapper>
      <div className="select-mode">
        {modes?.map((item) => {
          return (
            <div className="form-radio-group">
              <label>
                <input
                  type="radio"
                  value={item?.value}
                  checked={selectedOption === item?.value}
                  onChange={handleOptionChange}
                  className="radio-input"
                />
                {item?.label}
              </label>
            </div>
          );
        })}
      </div>
      <div className="select-header-container">
        <div className="select-header">
          <FormControlLabel
            control={
              <Checkbox checked={checkedOption} onChange={handleOptionCheck} />
            }
            label="Create ABHA for the patient"
            className="form-control-checkbox"
          />
          <Typography className="form-control-subtext">
            Lorem Ipsum is simply dummy text of the printing and typesetting
            industry. Lorem Ipsum has been the industry's standard dummy text
            ever since the 1500s, when an unknown printer took a galley of type
            and scrambled it to make a type specimen book.
          </Typography>
        </div>
      </div>
    </VerificationSelectionWrapper>
  );
}

export default VerificationSelection;