import { Button, Card, Typography, styled } from "@mui/material";
import React, { useState } from "react";
import PdfFromDocumentBytes from "../../../PdfFromDocumentBytes";

const TableTitle = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primaryGrey,
  marginBottom: "1px",
  padding: theme.spacing(0, 5),
}));

const ReportCardSection = styled(Card)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  marginBottom: theme.spacing(2),
}));

function AttachmentSection({ data }) {
  const [base64data, setBase64data] = useState(null);
  const [open, setOpen] = useState(false);
  const [documentType, setDocumentType] = useState(null);

  const handlePdfViewer = (base64Data, docType) => () => {
    setBase64data(base64Data);
    setDocumentType(docType);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  if (!Array.isArray(data)) {
    console.error('Invalid prop: "data" is not an array.');
    return null;
  }
  return (
    <>
      <Typography variant="h6" fontSize={18} fontWeight={600}>
        #Attachements
      </Typography>
      <ReportCardSection>
        <TableTitle>
          <Typography variant="h6">Titles:</Typography>
        </TableTitle>
        <ul
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "start",
          }}
        >
          {data?.map((Values) =>
            Values.content.map((contentItem, index) => (
              <Button
                variant="text"
                color="inherit"
                key={index}
                onClick={handlePdfViewer(
                  contentItem.attachment.data,
                  contentItem.attachment.contentType
                )}
              >
                <li>{contentItem.attachment.title}</li>
              </Button>
            ))
          )}
        </ul>
      </ReportCardSection>
      {base64data && (
        <PdfFromDocumentBytes
          open={open}
          handleClose={handleClose}
          documentType={documentType}
          docBytes={base64data}
        />
      )}
    </>
  );
}
export default AttachmentSection;
