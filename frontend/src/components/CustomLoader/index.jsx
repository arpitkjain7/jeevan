import React from "react";
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';

const CustomLoader = ({ open, onClose }) => {
    return (
      <div>
        <Backdrop
          sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
          open={open}
          onClose={onClose}
        >
          <CircularProgress color="inherit" />
        </Backdrop>
      </div>
    );
};

export default CustomLoader;
