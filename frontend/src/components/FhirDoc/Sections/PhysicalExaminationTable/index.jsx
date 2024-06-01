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
}));

function PhysicalExaminationTable({ data }) {
  //   console.log("physical:", data);
  if (!Array.isArray(data)) {
    console.error('Invalid prop: "data" is not an array.');
    return null;
  }
  return (
    <>
      <Typography variant="h6" fontSize={18} fontWeight={600}>
        #Physical Exam Section: Physical Examinations
      </Typography>
      <ReportCardSection>
        <TableTitle>
          <Typography variant="h6">Observations:</Typography>
        </TableTitle>
        <TableContainer>
          <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
            <TableHeader>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell align="right">Observation</TableCell>
                <TableCell align="right">Value</TableCell>
                <TableCell align="right">Status And Interpretation</TableCell>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data?.map((Values) => (
                <TableRow
                  key={Values.id}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {/* {new Date(Value.Date).toLocaleDateString("en-GB", {
                      year: "2-digit",
                      month: "2-digit",
                      day: "2-digit",
                    })} */}
                    Date?
                  </TableCell>
                  <TableCell align="right">{Values.code.text}</TableCell>
                  <TableCell align="right">
                    {Values?.valueQuantity?.value &&
                      `${Values.valueQuantity.value} ${Values.valueQuantity.unit}`}
                  </TableCell>
                  <TableCell align="right">{Values.status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </ReportCardSection>
    </>
  );
}
export default PhysicalExaminationTable;
