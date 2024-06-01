import { Button, Card, Typography, styled } from "@mui/material";
import React from "react";
import base64js from "base64-js";

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
  function getDataSize(base64String) {
    const byteArray = base64js.toByteArray(base64String);
    const size = byteArray.length / 1024;
    return size.toFixed(2);
  }

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
                onClick={async (event) => {
                  event.preventDefault();
                  try {
                    const size = getDataSize(contentItem.attachment.data);
                    alert(`Size of the file: ${size} KB`);
                  } catch (error) {
                    console.error("Error calculating size:", error);
                  }
                }}
              >
                <li>{contentItem.attachment.title}</li>
              </Button>
            ))
          )}
        </ul>
      </ReportCardSection>
    </>
  );
}
export default AttachmentSection;
