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

function MedicationTable({ data }) {
  // console.log("condition:", data);
  if (!Array.isArray(data)) {
    console.error('Invalid prop: "data" is not an array.');
    return null;
  }
  return (
    <>
      <Typography variant="h6" fontSize={18} fontWeight={600}>
        #Medical Summary Document: Medications
      </Typography>
      <ReportCardSection>
        <TableTitle>
          <Typography variant="h6">Medication:</Typography>
        </TableTitle>
        <TableContainer>
          <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
            <TableHeader>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell align="right">Medication</TableCell>
                <TableCell align="right">Dosing Instruction</TableCell>
                <TableCell align="right">Aditional Info</TableCell>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data?.map((Value) => (
                <TableRow
                  key={Value.id}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {new Date(Value.authoredOn).toLocaleDateString("en-GB", {
                      year: "2-digit",
                      month: "2-digit",
                      day: "2-digit",
                    })}
                  </TableCell>
                  <TableCell align="right">
                    {Value.medicationCodeableConcept.text}
                  </TableCell>
                  <TableCell align="right">
                    {Value.dosageInstruction[0].text}
                  </TableCell>
                  <TableCell align="right">Empty</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </ReportCardSection>
    </>
  );
}
export default MedicationTable;
