import {
  Card,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  styled,
} from "@mui/material";
import React from "react";

const TableHeader = styled(TableHead)(({ theme }) => ({
  backgroundColor: theme.palette.primaryGrey,
  height: "50px",
}));

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

function MedicalHistoryTable({ data }) {
  // console.log("condition:", data);
  if (!Array.isArray(data)) {
    console.error('Invalid prop: "data" is not an array.');
    return null;
  }
  return (
    <>
      <Typography variant="h6" fontSize={18} fontWeight={600}>
        #History And Physical Report: Medical History
      </Typography>
      <ReportCardSection>
        <TableTitle>
          <Typography variant="h6">Condition:</Typography>
        </TableTitle>
        <TableContainer>
          <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
            <TableHeader>
              <TableRow>
                <TableCell>Recorded Dates</TableCell>
                <TableCell align="right">Condition</TableCell>
                <TableCell align="right">Status</TableCell>
                <TableCell align="right">Aditional Notes</TableCell>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data
                ?.filter((Value) => Value.clinicalStatus.text === "HISTORY")
                .map((Value) => (
                  <TableRow
                    key={Value.id}
                    sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                  >
                    <TableCell component="th" scope="row">
                      {new Date(Value.recordedDate).toLocaleDateString(
                        "en-GB",
                        {
                          year: "2-digit",
                          month: "2-digit",
                          day: "2-digit",
                        }
                      )}
                    </TableCell>
                    <TableCell align="right">{Value.code.text}</TableCell>
                    <TableCell align="right">
                      {Value.clinicalStatus.text}
                    </TableCell>
                    <TableCell align="right"></TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
      </ReportCardSection>
    </>
  );
}
export default MedicalHistoryTable;
