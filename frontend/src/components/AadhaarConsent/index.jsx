import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Box, Checkbox, 
  FormControlLabel, FormGroup, 
  styled 
} from '@mui/material';

const CustomFormGroup = styled(FormGroup)(({ theme }) => ({
  "& .MuiFormControlLabel-root": {
    alignItems: "flex-start",
    margin: "8px 0",
  },
  "& .MuiFormControlLabel-root .MuiButtonBase-root": {
    padding: "3px 9px",
  },
}));

const AadhaarConsent = ({ open, scroll, handleClose, handleConsentConfirmation}) => {
  const descriptionElementRef = React.useRef(null);
  const [allChecked, setAllChecked] = useState(false);
  const username = sessionStorage.getItem("userName");
  const [checkboxes, setCheckboxes] = useState({
    check1: false,
    check3: false,
    check4: false,
    check5: false,
    check6: false,
    check7: false,
  });
  
  useEffect(() => {
    if (open) {
      const { current: descriptionElement } = descriptionElementRef;
      if (descriptionElement !== null) {
        descriptionElement.focus();
      }
    }
  }, [open]);

  useEffect(() => {
    const result = Object.values(checkboxes).every(v => v);
    setAllChecked(result);
  }, [checkboxes]);

  const handleChange = (e) => {
    console.log(e.target.id, e.target.name, e.target.value, e.target.checked);
    setCheckboxes({
      ...checkboxes,
      [e.target.name]: e.target.checked
    });

  }
  const children = (
    <Box sx={{ display: 'flex', flexDirection: 'column', ml: 3 }}>
      <FormControlLabel
        label={`I, ${username}, confirm that I have duly informed and explained the beneficiary of the contents of consent for aforementioned purposes.`}
        name="check6" control={<Checkbox/>} id="check6" value={checkboxes.check6} onChange={handleChange}
      />
      <FormControlLabel
        label="I, (beneficiary name), have been explained about the consent as stated above and hereby provide my consent for the aforementioned purposes."
        name="check7" control={<Checkbox/>} id="check7" value={checkboxes.check7} onChange={handleChange}
      />
    </Box>
  );

  return (
    <React.Fragment>
      <Dialog
        open={open}
        onClose={handleClose}
        scroll="paper"
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
      >
        <DialogTitle id="scroll-dialog-title"  style={{ fontWeight: "550" }}>Permission for Aadhaar Details Sharing</DialogTitle>
        <DialogContent dividers={scroll === 'paper'}>
          <DialogContentText
            id="scroll-dialog-description"
            ref={descriptionElementRef}
            tabIndex={-1}
            style={{ color: "#323232" }}
          >
           {/* I, hereby declare that I am voluntarily sharing my Aadhaar Number and demographic information issued by UIDAI, with National Health Authority (NHA) for the sole purpose of creation of ABHA number . I understand that my ABHA number can be used and shared for purposes as may be notified by ABDM from time to time including provision of healthcare services. Further, I am aware that my personal identifiable information (Name, Address, Age, Date of Birth, Gender and Photograph) may be made available to the entities working in the National Digital Health Ecosystem (NDHE) which inter alia includes stakeholders and entities such as healthcare professionals (e.g. doctors), facilities (e.g. hospitals, laboratories) and data fiduciaries (e.g. health programmes), which are registered with or linked to the Ayushman Bharat Digital Mission (ABDM), and various processes there under. I authorize NHA to use my Aadhaar number for performing Aadhaar based authentication with UIDAI as per the provisions of the Aadhaar (Targeted Delivery of Financial and other Subsidies, Benefits and Services) Act, 2016 for the aforesaid purpose. I understand that UIDAI will share my e-KYC details, or response of “Yes” with NHA upon successful authentication. I have been duly informed about the option of using other IDs apart from Aadhaar; however, I consciously choose to use Aadhaar number for the purpose of availing benefits across the NDHE. I am aware that my personal identifiable information excluding Aadhaar number / VID number can be used and shared for purposes as mentioned above. I reserve the right to revoke the given consent at any point of time as per provisions of Aadhaar Act and Regulations. */}
           I hereby declare that: 
           <CustomFormGroup>
              <FormControlLabel className="checkbox_style" name="check1" control={<Checkbox />} 
                label='I am voluntarily sharing my Aadhaar Number / Virtual ID issued by the Unique Identification Authority of India (“UIDAI”), and my demographic information for the purpose of creating an Ayushman Bharat Health Account number (“ABHA number”) and Ayushman Bharat Health Account address (“ABHA Address”). I authorize NHA to use my Aadhaar number / Virtual ID for performing Aadhaar based authentication with UIDAI as per the provisions of the Aadhaar (Targeted Delivery of Financial and other Subsidies, Benefits and Services) Act, 2016 for the aforesaid purpose. I understand that UIDAI will share my e-KYC details, or response of “Yes” with NHA upon successful authentication.' 
                id="check1" value={checkboxes.check1} onChange={handleChange}
              />
              {/* <FormControlLabel className="checkbox_style" required control={<Checkbox/>} 
                label='I intend to create Ayushman Bharat Health Account Number (“ABHA number”) and Ayushman Bharat Health Account address (“ABHA Address”) using document other than Aadhaar. (Click here to proceed further)' 
                id="check2" value={checkboxes.check2} onChange={handleChange}
              /> */}
              <FormControlLabel className="checkbox_style" name="check3" control={<Checkbox/>} 
                label='I consent to usage of my ABHA address and ABHA number for linking of my legacy (past) government health records and those which will be generated during this encounter.' 
                id="check3" value={checkboxes.check3} onChange={handleChange}
              />
              <FormControlLabel className="checkbox_style" name="check4" control={<Checkbox/>} 
                label='I authorize the sharing of all my health records with healthcare provider(s) for the purpose of providing healthcare services to me during this encounter.' 
                id="check4" value={checkboxes.check4} onChange={handleChange}
              />
              <FormControlLabel className="checkbox_style" name="check5" control={<Checkbox/>} 
                label='I consent to the anonymization and subsequent use of my government health records for public health purposes.' 
                id="check5" value={checkboxes.check5} onChange={handleChange}
              />
              {children}
            </CustomFormGroup>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} className='cancel_btn'>Disagree</Button>
          <Button onClick={handleConsentConfirmation} className='ok_btn' disabled={!allChecked}>Agree</Button>
        </DialogActions>
      </Dialog>
      </React.Fragment>
  );
}

export default AadhaarConsent