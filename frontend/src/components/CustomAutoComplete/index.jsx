import React from "react";
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";

const CustomAutoComplete = ({
  handleInputChange,
  handleOptionChange,
  options,
  setOptions,
  autocompleteRef,
  label = "",
  placeholder = "",
}) => {
  return (
    <Autocomplete
      freeSolo
      // ref={autocompleteRef}
      options={options}
      getOptionLabel={(option) => option?.label}
      isOptionEqualToValue={(option, value) =>
        value === null || value === "" || option.label === value
      }
      filterSelectedOptions
      clearOnEscape
      renderInput={(params) => (
        <TextField
          {...params}
          label={label}
          variant="outlined"
          onChange={handleInputChange}
          placeholder={placeholder}
        />
      )}
      value={null}
      blurOnSelect={true}
      clearOnBlur={true}
      onChange={handleOptionChange}
    />
  );
};

export default CustomAutoComplete;
