import React from "react";
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
// const Alert = React.forwardRef(function Alert(props, ref) {
//   return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
// });

const CustomLoader = ({ open, onClose }) => {
    // const [open, setOpen] = useState(false);
    // const handleClose = () => {
    //   setOpen(false);
    // };
    // const handleOpen = () => {
    //   setOpen(true);
    // };
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
