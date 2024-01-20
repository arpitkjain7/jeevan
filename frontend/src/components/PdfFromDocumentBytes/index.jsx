import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import ListItemText from '@mui/material/ListItemText';
import ListItem from '@mui/material/ListItem';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';
import { useState, useEffect } from 'react';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

function getWindowDimensions() {
    const { innerWidth: width, innerHeight: height } = window;
    return {
      width,
      height
    };

}
function useWindowDimensions() {
        const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());
      
        useEffect(() => {
          function handleResize() {
            setWindowDimensions(getWindowDimensions());
          }
      
          window.addEventListener('resize', handleResize);
          return () => window.removeEventListener('resize', handleResize);
        }, []);
        return windowDimensions;
    }
const PdfFromDocumentBytes = ({open, handleClose, documentType, docBytes}) => {
  const { height, width } = useWindowDimensions();
  const isMobile = window.innerWidth < 600;
  const docType = documentType;
    return (
        <React.Fragment>
      <Dialog
        fullScreen
        open={open}
        onClose={handleClose}
        TransitionComponent={Transition}
      >
        <AppBar sx={{ position: 'relative', zIndex: '1301x' }}>
          <Toolbar>
          <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
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
          {!isMobile && (
            <embed style={{ width: "auto", height: height }} src={`data:${docType};base64,${docBytes}`}/>
          )}
          {isMobile && (
            <embed style={{ width: width, height: "auto" }} src={`data:${docType};base64,${docBytes}`}/>
          )}
      </Dialog>
    </React.Fragment>
    )
}

export default PdfFromDocumentBytes