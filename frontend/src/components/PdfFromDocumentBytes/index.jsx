import * as React from 'react';
import Dialog from '@mui/material/Dialog';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
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
  // const [isPDF, setIsPDF] = useState(false);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  useEffect(() => {
    if(docType === "application/pdf" && isMobile){
      // setIsPDF(true);
      pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`; 
      if (docBytes) {
        const decodedByteCode = atob(docBytes);
        const byteNumbers = new Array(decodedByteCode.length);
        for (let i = 0; i < decodedByteCode.length; i++) {
          byteNumbers[i] = decodedByteCode.charCodeAt(i);
        }
        const blobData = new Blob([new Uint8Array(byteNumbers)], {
          type: "application/pdf",
        });
        // const pdfUrls = URL.createObjectURL(blobData);
        setPdfUrl(URL.createObjectURL(blobData));
        return () => {
          URL.revokeObjectURL(pdfUrl);
        };
      }
    } 
    // else{
    //   setIsPDF(false);
    // }
    }, [docBytes]);
  
    const onDocumentLoadSuccess = (({ numPages }) => {
      setNumPages(numPages);
    });

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
          {/* {isMobile && !isPDF && (
            <embed style={{ width: width, height: "auto" }} src={`data:${docType};base64,${docBytes}`}/>
          )} */}
          {isMobile && pdfUrl !== null && (
            <>
            
              <Document file={pdfUrl} onLoadSuccess={onDocumentLoadSuccess} >
                {Array.apply(null, Array(numPages))
                  .map((x, i)=>i+1)
                  .map(page =>
                    <Page wrap pageNumber={page} renderTextLayer={true} width={width} height="auto" />
                )}
              </Document>
            </>
          )}
      </Dialog>
    </React.Fragment>
    )
}

export default PdfFromDocumentBytes