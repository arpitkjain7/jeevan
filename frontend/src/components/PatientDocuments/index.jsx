import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import AssignmentIcon from '@mui/icons-material/Assignment';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';
import { forwardRef } from 'react';
import PastVisits from '../PastVisits';

const Transition = forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

const PatientDocuments = ({handleClickOpen, open, handleClose}) => {
  const isPatientHistory = true;
  return (
    <React.Fragment>
      <Button variant="outlined" onClick={handleClickOpen} >

      <AssignmentIcon />&nbsp; Documents
      </Button>
      <Dialog
        fullScreen
        open={open}
        onClose={handleClose}
        TransitionComponent={Transition}
      >
        <AppBar sx={{ position: 'relative' }}>
          <Toolbar>
            <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
              Patient History
            </Typography>
            <IconButton
              edge="start"
              color="inherit"
              onClick={handleClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
       <PastVisits
         isPatientHistory={isPatientHistory}
       >
       </PastVisits>
      </Dialog>
    </React.Fragment>
  );
}

export default PatientDocuments
