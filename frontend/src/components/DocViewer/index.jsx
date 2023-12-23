import React, { useEffect } from "react";
// import pdfjs from "pdfjs-dist/build/pdf";
import { styled } from "@mui/material";
import { useState } from "react";
import { useRef } from "react";
import ArrowRight from "../../assets/arrows/arrow-right.svg";

const DocViewerContainer = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primaryWhite,
  padding: theme.spacing(0, 6),
}));
const Views = styled("div")(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(8),
  padding: theme.spacing(8, 0),
  minHeight: "600px",
}));
const PdfContainer = styled("div")(({ theme }) => ({
  flex: "1",
  height: "100%",
}));
const SideList = styled("List")(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(8),
}));

const DiagnosisDetails = styled("ListItem")(({ theme }) => ({
  padding: theme.spacing(4),
  borderRadius: theme.spacing(1),
  border: `1px solid ${theme.palette.primaryGrey}`,
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",

  "&.selected-vital": {
    border: `1px solid ${theme.palette.primaryBlue}`,
  },
}));
const DocList = styled("p")(({ theme }) => ({
  margin: "0",
}));

const DocViewer = ({ docData }) => {
  console.log(docData, "docData");
  const [byteCode, setByteCode] = useState("");
  const [selectedDocument, setSelectedDocument] = useState("");
  const pdfViewerRef = useRef(null);
  const onDocClick = (selectedItem) => {
    setByteCode(selectedItem?.documentContent);
    setSelectedDocument(selectedItem?.id);
  };
  const [pdfUrl, setPdfUrl] = useState(null);

  const convertToDoc = () => {};

  useEffect(() => {
    setByteCode(docData[0]?.documentContent);
  }, []);

  useEffect(() => {
    if (byteCode) {
      const decodedByteCode = atob(byteCode);
      const byteNumbers = new Array(decodedByteCode.length);
      for (let i = 0; i < decodedByteCode.length; i++) {
        byteNumbers[i] = decodedByteCode.charCodeAt(i);
      }
      const blob = new Blob([new Uint8Array(byteNumbers)], {
        type: "application/pdf",
      });

      const pdfUrl = URL.createObjectURL(blob);
      setPdfUrl(pdfUrl);
      return () => {
        URL.revokeObjectURL(pdfUrl);
      };
    }
  }, [byteCode]);

  return (
    <DocViewerContainer>
      <Views>
        <SideList>
          {docData?.length &&
            docData?.map(
              (item) =>
                item?.id && (
                  <DiagnosisDetails
                    onClick={() => onDocClick(item)}
                    className={
                      selectedDocument === item?.id ? "selected-vital" : ""
                    }
                  >
                    <DocList>{item?.id}</DocList>
                    <img src={ArrowRight} alt={`select-${item.type}`} />
                  </DiagnosisDetails>
                )
            )}
        </SideList>
        <PdfContainer>
          <embed
            src={pdfUrl}
            type="application/pdf"
            width="100%"
            height="700px"
          />
        </PdfContainer>
      </Views>
    </DocViewerContainer>
  );
};

export default DocViewer;
