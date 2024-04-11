import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, styled, tableCellClasses } from "@mui/material";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

const ChartWrapper = styled("div")(({ theme }) => ({
  "&": {
    padding: "20px",
  },
}));

const VaccineChart = () => {
  const dispatch = useDispatch();
  const patient = sessionStorage?.getItem("selectedPatient");

  useEffect(() => {
    const currentPatient = JSON.parse(patient);
  }, []);

  const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.head}`]: {
      backgroundColor: theme.palette.common.black,
      color: theme.palette.common.white,
    },
    [`&.${tableCellClasses.body}`]: {
      fontSize: 14,
    },
  }));
  
  const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
    // hide last border
    '&:last-child td, &:last-child th': {
      border: 0,
    },
  }));

  function createData(age, vaccine) {
    return { age, vaccine };
  }

  const rows = [
    createData('Birth', 'BCG'),
    createData('', 'OPV 0'),
    createData('', 'Hep - B1'),
    createData('6 Weeks', 'DtwP1/DtaP1'),
    createData('', 'Hep - B2'),
    createData('', 'Hib 1'),
    createData('', 'IPV 1/OPV'),
    createData('', 'Rotavirus 1'),
    createData('', 'PCV1(Pneumonia'),

    createData('10 Weeks', 'DtwP2/DtaP2'),
    createData('', 'Hib 2'),
    createData('', 'IPV 2/OPV'),
    createData('', 'Rotavirus 2'),
    createData('', 'PCV2(Pneumonia'),

    createData('14 Weeks', 'DtwP3/DtaP3'),
    createData('', 'Hib 3'),
    createData('', 'IPV 3/OPV'),
    createData('', 'Rotavirus 3'),
    createData('', 'PCV3(Pneumonia'),

    createData('06 Months', 'OPV 1'),
    createData('', 'Hap - 3'),
    createData('', 'Infuenza 1'),

    createData('07 Months', 'Infuenza 2'),

    createData('09 Months', 'OPV 2'),
    createData('', 'MMR 1'),
    createData('', 'Typhoid 1'),
    createData('', 'Meningococcal 1'),

    createData('12 Months', 'JE 1'),
    createData('', 'Hep A1'),

    createData('13 Months', 'JE 2'),

    createData('15 Months', 'MMR 2'),
    createData('', 'Vericella 1(Chicken Pox)'),
    createData('', 'PCV Booster'),

    createData('16 to 18 Months', 'DtwP B1/DtaP B1'),
    createData('', 'Hib B1'),
    createData('', 'IVP B1'),

    createData('19 Months to 2 Yrs', 'Hep - A2'),
    createData('', 'Influenza'),
    createData('', 'Vericella 2'),
    createData('', 'Typhoid 2'),

    createData('24 Months', 'Meningococcal'),
    createData('03 Years', 'Influenza'),
    createData('04 Years', 'Influenza'),

    createData('4 1/2 Years to 5 Years', 'DtwP B2/DtaP B2'),
    createData('', 'OPV 3'),
    createData('', 'MMR 3'),
    createData('', 'Influenza'),
    createData('', 'Vericella 2'),

    createData('10 to 12 Years', 'Tdap / Td'),
    createData('', 'HPV (Girls) 1'),
    createData('', 'HPV 2'),
    createData('', 'HPV 3'),

    createData('Yearly', 'Influenza'),
  ];

  return (
    <ChartWrapper>
        <div style={{ textAlign: "center" }}>
            <h3>Immunization (Indian Academy of Pediatrics) </h3>
        </div>
        <TableContainer component={Paper}>
      <Table sx={{ minWidth: 700 }} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell>Age</StyledTableCell>
            <StyledTableCell align="right">Vaccine</StyledTableCell>
            <StyledTableCell align="right">Due On</StyledTableCell>
            <StyledTableCell align="right">Given On</StyledTableCell>
            <StyledTableCell align="right">Comments/Batch</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, index) => (
            <StyledTableRow key={index} >
              <StyledTableCell component="th" scope="row">
                {row.age}
              </StyledTableCell>
              <StyledTableCell align="right">{row.vaccine}</StyledTableCell>
              <StyledTableCell align="right">
                <TextField
                  type="date"
                />
              </StyledTableCell>
              <StyledTableCell align="right">
                <TextField
                  type="date"
                />
              </StyledTableCell>
              <StyledTableCell align="right">
                <TextField
                />
              </StyledTableCell>
              {/* <StyledTableCell align="right">{row.fat}</StyledTableCell>
              <StyledTableCell align="right">{row.carbs}</StyledTableCell>
              <StyledTableCell align="right">{row.protein}</StyledTableCell> */}
            </StyledTableRow>
          ))}
           {/* <StyledTableRow>
              <StyledTableCell component="th" scope="row">
                Birth
              </StyledTableCell>
              <StyledTableCell align="right">BCG</StyledTableCell>
              <StyledTableCell align="right"></StyledTableCell>
              <StyledTableCell align="right"></StyledTableCell>
              <StyledTableCell align="right"></StyledTableCell>
            </StyledTableRow> */}
        </TableBody>
      </Table>
    </TableContainer>
    </ChartWrapper>
  );
};

export default VaccineChart;
