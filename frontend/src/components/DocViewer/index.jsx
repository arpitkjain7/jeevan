import React, { useEffect } from "react";
import pdfjs from "pdfjs-dist/build/pdf";

const DocViewerContainer = styled("div")(({ theme }) => ({
  backgroundColor: theme.palette.primaryWhite,
  padding: theme.spacing(0, 6),
}));
const Views = styled("div")(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(4),
  padding: theme.spacing(8, 0),
}));
const SideList = styled("List")(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  gap: theme.spacing(8),
}));

const DiagnosisDetails = styled("ListItem")(({ theme }) => ({
  padding: theme.spacing(2, 4),
  borderRadius: theme.spacing(1),
  border: `1px solid ${theme.palette.primaryGrey}`,
}));
const DocViewer = ({ list }) => {
  //list should be : {id, document, name,...extra params}
  const [byteCode, setByteCode] = useState("");
  const pdfViewerRef = useRef(null);
  const onDocClick = (selectedItem) => {
    setByteCode(selectedItem?.document);
  };

  useEffect(() => {
    const loadPdf = async () => {
      const pdfData = new Uint8Array(byteCode);
      const loadingTask = pdfjs.getDocument(pdfData);
      const pdf = await loadingTask.promise;

      // Assuming you have a single page PDF, if not, you may loop through pages here.
      const pageNumber = 1;
      const page = await pdf.getPage(pageNumber);

      const scale = 1.5; // Adjust as needed
      const viewport = page.getViewport({ scale });

      const canvas = pdfViewerRef.current;
      const context = canvas.getContext("2d");
      canvas.height = viewport.height;
      canvas.width = viewport.width;

      const renderContext = {
        canvasContext: context,
        viewport: viewport,
      };

      await page.render(renderContext);
    };

    if (byteCode) {
      loadPdf();
    }
  }, [byteCode]);

  return (
    <DocViewerContainer>
      <Views>
        <SideList>
          {list.map((item) => (
            <DiagnosisDetails onClick={() => onDocClick(item)}>
              {item?.type}
            </DiagnosisDetails>
          ))}
        </SideList>
      </Views>
    </DocViewerContainer>
  );
};

export default DocViewer;
