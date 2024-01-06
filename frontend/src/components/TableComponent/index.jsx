import React, { useState } from "react";
import PropTypes from 'prop-types';
import { useTheme } from '@mui/material/styles';
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
  Box
} from "@mui/material";
import {
  Class, Search as SearchIcon,
  KeyboardArrowLeft,
  KeyboardArrowRight
} from "@mui/icons-material";
import FirstPageIcon from '@mui/icons-material/FirstPage';
import LastPageIcon from '@mui/icons-material/LastPage';
import SettingsIcon from "@mui/icons-material/Settings";

const TableComponentWrapper = styled("div")(({ theme }) => ({
  "&": {
    border: `1px solid ${theme.palette.primaryGrey}`,
    backgroundColor: theme?.palette?.primaryWhite,
  },
  ".search-wrap": {
    padding: theme.spacing(4),
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: theme.spacing(4.5),
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
    border: "1px solid #e0e0e0"
  },
  ".table-component-wrapper": {},
  ".table-component-header": {
    // "&.MuiTableHead-root": {
    //   backgroundColor: theme.palette.primaryOpacityBlue,
    // },
    "& > tr >th": {
      backgroundColor: '#bde4ff',
    },
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
        {theme.direction === 'rtl' ? <LastPageIcon /> : <FirstPageIcon />}
      </IconButton>
      <IconButton
        onClick={handleBackButtonClick}
        disabled={page === 0}
        aria-label="previous page"
      >
        {theme.direction === 'rtl' ? <KeyboardArrowRight /> : <KeyboardArrowLeft />}
      </IconButton>
      <IconButton
        onClick={handleNextButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="next page"
      >
        {theme.direction === 'rtl' ? <KeyboardArrowLeft /> : <KeyboardArrowRight />}
      </IconButton>
      <IconButton
        onClick={handleLastPageButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="last page"
      >
        {theme.direction === 'rtl' ? <FirstPageIcon /> : <LastPageIcon />}
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


const MyTable = ({
  columns,
  data,
  showSearch = true,
  tableStyle,
  tableClassName,
  searchClassName,
  onRowClick,
}) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const filteredData = data?.filter((item) => {
    const lowerCaseSearchTerm = searchTerm.toLowerCase();
    return columns.some((column) =>
      item[column.key]?.toString()?.toLowerCase()?.includes(lowerCaseSearchTerm)
    );
  });
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



  return (
    <TableComponentWrapper>
      {showSearch && (
        <div style={{ backgroundColor: '#fff' }} className="search-wrap">
          <TextField
            variant="outlined"
            fullWidth
            sx={{ mb: 2 }}
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
        </div>
      )}
      <Paper sx={{ overflow: 'hidden' }} >
        <TableContainer
          // style={tableStyle}
          className={tableClassName}
          sx={{ maxHeight: 540 }}
        >
          <Table stickyHeader sx={{ minWidth: 500, flexShrink: "0" }} className="table-component-wrapper">
            <TableHead className="table-component-header" >
              <TableRow>
                {columns?.map((column) => (
                  <TableCell key={column.key} className="table-header-cell">
                    {column.header}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody className="table-body-container">
              {filteredData && (rowsPerPage > 0
                ? filteredData.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                : filteredData).map((item) => (
                  <TableRow
                    key={item.id}
                    onClick={() => onRowClick && onRowClick(item)}
                  >
                    {columns?.map((column) => {
                      if (column.key == "consentStatus"){
                        return (
                          <TableCell key={`${item?.id}-${column?.key}`}>
                            <Typography
                                style={{ color: `${item?.status}` === 'GRANTED' ? 'green' : 'red'}}
                              >
                                {item.status}
                              </Typography>
                            </TableCell>
                          );
                      }
                      if (column.key !== "actions" && column.key !== "p_name") {
                        return (
                          <TableCell key={`${item?.id}-${column?.key}`}>
                            {column?.render
                              ? column?.render(item[column?.key])
                              : item[column.key]}
                          </TableCell>
                        );
                      } else {
                        const actions = column.actions || [];
                        return (
                          <TableCell key={`${item.id}-${column.key}`} align="right">
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
                                } else {
                                  return (
                                    <Typography
                                      key={index}
                                      size="small"
                                      onClick={() => action.onClick(item)}
                                      className="linkTypography"
                                    >
                                      {action?.key ? item[action?.key] : action?.link}
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
              ))}
              {emptyRows > 0 && (
                <TableRow style={{ height: 53 * emptyRows }}>
                  <TableCell colSpan={7} />
                </TableRow>
              )}
            </TableBody>
            <TableFooter>
              <TableRow>

              </TableRow>
            </TableFooter>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25, { label: 'All', value: -1 }]}
          component="div"
          colSpan={columns.length}
          count={filteredData.length}
          rowsPerPage={rowsPerPage}
          page={page}
          SelectProps={{
            inputProps: {
              'aria-label': 'rows per page',
            },
            native: true,
          }}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          ActionsComponent={TablePaginationActions}
        />
      </Paper>
    </TableComponentWrapper>
  );
};

export default MyTable;