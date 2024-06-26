import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { useTheme } from "@mui/material/styles";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  IconButton,
  styled,
  Typography,
  TableFooter,
  TablePagination,
  Box,
  FormControl,
  MenuItem,
  InputLabel,
  Select,
  Button,
  FormGroup,
  Switch,
  Stack,
} from "@mui/material";
import {
  Search as SearchIcon,
  KeyboardArrowLeft,
  KeyboardArrowRight,
} from "@mui/icons-material";
import FirstPageIcon from "@mui/icons-material/FirstPage";
import LastPageIcon from "@mui/icons-material/LastPage";
import { convertDateFormat } from "../../utils/utils";

const TableComponentWrapper = styled("div")(({ theme }) => ({
  "&": {
    border: `1px solid ${theme.palette.primaryGrey}`,
    backgroundColor: theme?.palette?.primaryWhite,
  },
  ".search-wrap": {
    padding: theme.spacing(4),
    alignItems: "center",
    [theme.breakpoints.down('sm')]: {
      display: "block",
    },
    "& .MuiFormControl-root": {
      [theme.breakpoints.up('sm')]: {
        marginRight: "10px",
        width: "200px",
      },
      [theme.breakpoints.down('sm')]: {
        marginBottom: "8px",
        width: "100%",
      },
    },
  },
  ".linkTypography": {
    "&.MuiTypography-root": theme.typography.link,
    cursor: "pointer",
    textAlign: "left",
  },
  ".table-body-container": {
    "&.MuiTableBody-root": {
      backgroundColor: theme.palette.primaryWhite,
    },
  },
  ".table-body-container tr td": {
    borderRight: "1px solid #e0e0e0",
  },
  ".table-component-wrapper": {},
  ".table-component-header": {
    // "&.MuiTableHead-root": {
    //   backgroundColor: theme.palette.primaryOpacityBlue,
    // },
    "& > tr >th": {
      backgroundColor: "#bde4ff",
      // borderRight: "1px solid #e0e0e0",
    },
  },
  ".followBtn" : {
    padding: "10px",
    backgroundColor: "#1976d2db",
    marginTop: "5px",
  },
}));

function TablePaginationActions(props) {
  const theme = useTheme();
  const { count, page, rowsPerPage, onPageChange } = props;

  const handleFirstPageButtonClick = (event) => {
    onPageChange(event, 0);
  };

  const handleBackButtonClick = (event) => {
    onPageChange(event, page - 1);
  };

  const handleNextButtonClick = (event) => {
    onPageChange(event, page + 1);
  };

  const handleLastPageButtonClick = (event) => {
    onPageChange(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
  };

  return (
    <Box sx={{ flexShrink: 0, ml: 2.5 }}>
      <IconButton
        onClick={handleFirstPageButtonClick}
        disabled={page === 0}
        aria-label="first page"
      >
        {theme.direction === "rtl" ? <LastPageIcon /> : <FirstPageIcon />}
      </IconButton>
      <IconButton
        onClick={handleBackButtonClick}
        disabled={page === 0}
        aria-label="previous page"
      >
        {theme.direction === "rtl" ? (
          <KeyboardArrowRight />
        ) : (
          <KeyboardArrowLeft />
        )}
      </IconButton>
      <IconButton
        onClick={handleNextButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="next page"
      >
        {theme.direction === "rtl" ? (
          <KeyboardArrowLeft />
        ) : (
          <KeyboardArrowRight />
        )}
      </IconButton>
      <IconButton
        onClick={handleLastPageButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="last page"
      >
        {theme.direction === "rtl" ? <FirstPageIcon /> : <LastPageIcon />}
      </IconButton>
    </Box>
  );
}

TablePaginationActions.propTypes = {
  count: PropTypes.number.isRequired,
  onPageChange: PropTypes.func.isRequired,
  page: PropTypes.number.isRequired,
  rowsPerPage: PropTypes.number.isRequired,
};

const AppointmentTable = ({
  apmntColumns,
  followUpColumns,
  data,
  showSearch = true,
  tableStyle,
  tableClassName,
  searchClassName,
  onRowClick,
  showFilter,
  handleDateChange,
  filterDateValue,
  appointmentData,
  followUpData
}) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [filterValue, setFilterValue] = useState("");
  const [isFollowUp, setIsFollowUp] = useState(false);
  const [filteredData, setFilteredData] = useState();
  const [columns, setColumns] = useState(apmntColumns);
  const finalData = (data) => {
    const filteredDataa = data?.filter((item) => {
    const lowerCaseSearchTerm = searchTerm.toLowerCase();
    
      if (showFilter && isFollowUp) {
        let filterSearch;
        if (filterValue === "All") filterSearch = "";
        else filterSearch = filterValue.toLowerCase();
        let formattedDate;
        if (filterDateValue === "") formattedDate = "";
        else formattedDate = convertDateFormat(filterDateValue, "dd/MM/yyyy");
        
        return columns.some(
          (column) =>
            (item["patientId"]
              ?.toString()
              ?.toLowerCase()
              ?.includes(lowerCaseSearchTerm) ||
              item["patientDetails"]
                ?.toString()
                ?.toLowerCase()
                ?.includes(lowerCaseSearchTerm) ||
              item["mobileNumber"]
                ?.toString()
                ?.toLowerCase()
                ?.includes(lowerCaseSearchTerm)) 
              && (            
              item["status"]?.toString()?.toLowerCase()?.includes(filterSearch)
              )
                // item["type"]?.toString()?.toLowerCase()?.includes(filterSearch))
            // && item["slotDate"]?.toString()?.includes(formattedDate)
        );
      } else {
        return columns.some((column) =>
          item[column.key]
            ?.toString()
            ?.toLowerCase()
            ?.includes(lowerCaseSearchTerm)
        );
      }
   
    });
    setFilteredData(filteredDataa);
  }

  useEffect(() => {
    setIsFollowUp(false);
    // if(appointmentData) {
      finalData(appointmentData);
    // }
  }, [appointmentData]);

  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows =
    page > 0 ? Math.max(0, (1 + page) * rowsPerPage - filteredData.length) : 0;

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleFilterChange = (event) => {
    setFilterValue(event.target.value);
  };

  const handleFollowUp = () => {
    if(isFollowUp){
      finalData(appointmentData);
      setColumns(apmntColumns);
    } else {
      finalData(followUpData);
      setColumns(followUpColumns);
    }
      setIsFollowUp((prevValue) => !prevValue);
  };

  return (
    <TableComponentWrapper>
      {showSearch && (
        <div style={{ backgroundColor: "#fff" }} className="search-wrap">
          <TextField
            variant="outlined"
            fullWidth
            InputProps={{
              startAdornment: (
                <IconButton size="small">
                  <SearchIcon />
                </IconButton>
              ),
            }}
            value={searchTerm}
            onChange={handleSearch}
            className={searchClassName}
          />

          {showFilter && (
            <>
              {/* <FormLabel>Date</FormLabel> */}
              <TextField
                placeholder="Select Date"
                type="date"
                value={filterDateValue}
                onChange={handleDateChange}
              />
              <FormControl className="filter_status">
                <InputLabel id="demo-simple-select-label">
                  Filter by Status
                </InputLabel>
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  label="Filter by Status"
                  value={filterValue}
                  onChange={handleFilterChange}
                >
                  <MenuItem value="All">All</MenuItem>
                  <MenuItem value="Scheduled">Scheduled</MenuItem>
                  <MenuItem value="InProgress">InProgress</MenuItem>
                  <MenuItem value="Completed">Completed</MenuItem>
                </Select>
              </FormControl>
              {/* {isFollowUp
               ? 
              <Button onClick={handleFollowUp} variant="contained" className="followBtn">Appointment</Button> 
               :
              <Button onClick={handleFollowUp} variant="contained" className="followBtn">Follow Up</Button> 
              } */}
              <FormGroup style={{ display: "inline-flex", padding: "8px" }}>
               <Stack direction="row" spacing={1} alignItems="center">
                <Typography>Appointment</Typography>
                {/* <AntSwitch defaultChecked inputProps={{ 'aria-label': 'ant design' }} /> */}
                <Switch
                  checked={isFollowUp}
                  onChange={handleFollowUp}
                  inputProps={{ 'aria-label': 'controlled' }}
                />
                <Typography>Follow Up</Typography>
               </Stack>
              </FormGroup>
            </>
          )}
        </div>
      )}
      <Paper sx={{ overflow: "hidden" }}>
        <TableContainer
          // style={tableStyle}
          className={tableClassName}
          sx={{ maxHeight: 540 }}
        >
          <Table
            stickyHeader
            sx={{ minWidth: 500, flexShrink: "0" }}
            className="table-component-wrapper"
          >
            <TableHead className="table-component-header">
              <TableRow>
                {columns?.map((column) => (
                  <TableCell key={column.key} className="table-header-cell">
                    {column.header}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody className="table-body-container">
              {filteredData ? (
                (rowsPerPage > 0
                  ? filteredData.slice(
                      page * rowsPerPage,
                      page * rowsPerPage + rowsPerPage
                    )
                  : filteredData
                ).map((item) => (
                  <TableRow
                    key={item.id}
                    onClick={() => onRowClick && onRowClick(item)}
                  >
                    {columns?.map((column) => {
                      if (column.key === "consentStatus") {
                        return (
                          <TableCell key={`${item?.id}-${column?.key}`}>
                            <Typography
                              style={{
                                color:
                                  `${item?.status}` === "GRANTED"
                                    ? "green"
                                    : "red",
                              }}
                            >
                              {item.status}
                            </Typography>
                          </TableCell>
                        );
                      }
                      if (column.key !== "actions" && column.key !== "p_name" && column.key !== "start_visit") {
                        return (
                          <TableCell key={`${item?.id}-${column?.key}`}>
                            {column?.render
                              ? column?.render(item[column?.key])
                              : item[column?.key]}
                          </TableCell>
                        );
                      } else {
                        const actions = column.actions || [];
                        return (
                          <TableCell
                            key={`${item.id}-${column.key}`}
                            align="right"
                          >
                            {actions?.map((action, index) => {
                              if (action?.type === "icon") {
                                return (
                                  <IconButton
                                    key={index}
                                    size="small"
                                    onClick={() => action?.onClick(item)}
                                  >
                                    {action.icon}
                                  </IconButton>
                                );
                              } else if (action?.type === "link") {
                                if (column.key === "p_name") {
                                  return (
                                    <Typography
                                      key={index}
                                      size="small"
                                      onClick={() => action.onClick(item)}
                                      className="linkTypography"
                                    >
                                      {item[column?.key]}
                                    </Typography>
                                  );
                                } else if (column.header === "Create Appointment") {
                                  return (
                                    <Typography
                                      key={index}
                                      size="small"
                                      onClick={() => action.onClick(item)}
                                      className="linkTypography"
                                    >
                                      {item.is_verified ? "Create Appointment" : "Verify"}
                                      {/* {action?.key
                                        ? item[action?.key]
                                        : action?.link} */}
                                    </Typography>
                                  );
                                } else if (column.header === "Start Appointment") {
                                  return (
                                    <Typography
                                      key={index}
                                      size="small"
                                      onClick={() => action.onClick(item)}
                                      className="linkTypography"
                                    >
                                      {item.is_verified ? "Start Visit" : "Verify"}
                                    </Typography>
                                  );
                                } else {
                                  return (
                                    <Typography
                                      key={index}
                                      size="small"
                                      onClick={() => action.onClick(item)}
                                      className="linkTypography"
                                    >
                                      {action?.key
                                        ? item[action?.key]
                                        : action?.link}
                                    </Typography>
                                  );
                                }
                              }
                            })}
                          </TableCell>
                        );
                      }
                    })}
                  </TableRow>
                ))) 
                : 
                  <TableRow>
                    <TableCell colSpan={columns.length} style={{ textAlign: "center" }}>
                     <h3>No data found</h3>
                    </TableCell>
                  </TableRow>
                }
              {emptyRows > 0 && (
                <TableRow style={{ height: 53 * emptyRows }}>
                  <TableCell colSpan="auto" />
                </TableRow>
              )}
            </TableBody>
            <TableFooter>
              <TableRow></TableRow>
            </TableFooter>
          </Table>
        </TableContainer>
        {filteredData &&
          <TablePagination
            rowsPerPageOptions={[5, 10, 25, { label: "All", value: -1 }]}
            component="div"
            colSpan={columns.length}
            count={filteredData.length}
            rowsPerPage={rowsPerPage}
            page={page}
            SelectProps={{
              inputProps: {
                "aria-label": "rows per page",
              },
              native: true,
            }}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
            ActionsComponent={TablePaginationActions}
          />
        }
      </Paper>
    </TableComponentWrapper>
  );
};

export default AppointmentTable;