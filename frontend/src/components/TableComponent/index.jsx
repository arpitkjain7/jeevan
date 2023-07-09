import React, { useState } from "react";
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
} from "@mui/material";
import { Class, Search as SearchIcon } from "@mui/icons-material";
import SettingsIcon from "@mui/icons-material/Settings";

const TableComponentWrapper = styled("div")(({ theme }) => ({
  "&": {
    border: `1px solid ${theme.primaryGrey}`,
  },
  ".search-wrap": {
    padding: "16px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "18px",
  },
}));

const MyTable = ({
  columns,
  data,
  showSearch = true,
  tableStyle,
  tableClassName,
  searchClassName,
}) => {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const filteredData = data?.filter((item) => {
    if(columns){
      const lowerCaseSearchTerm = searchTerm?.toLowerCase();
      return columns?.some((column) =>
        item[column.key]?.toString()?.toLowerCase()?.includes(lowerCaseSearchTerm)
      );
    }
    
  });

  return (
    <TableComponentWrapper>
      {showSearch && (
        <div className="search-wrap">
          <TextField
            variant="outlined"
            fullWidth
            sx={{ mb: 2 }}
            InputProps={{
              endAdornment: (
                <IconButton size="small">
                  <SearchIcon />
                </IconButton>
              ),
            }}
            value={searchTerm}
            onChange={handleSearch}
            className={searchClassName}
          />
          <SettingsIcon />
        </div>
      )}
      <TableContainer
        component={Paper}
        style={tableStyle}
        className={tableClassName}
      >
        <Table>
          <TableHead>
            <TableRow>
              {columns?.map((column) => (
                <TableCell key={column.key}>{column?.header}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredData?.map((item) => (
              <TableRow key={item.id}>
                {columns?.map((column) => {
                  if (column.key !== "actions") {
                    return (
                      <TableCell key={`${item?.id}-${column?.key}`}>
                        {column?.render
                          ? column?.render(item[column?.key])
                          : item[column.key]}
                      </TableCell>
                    );
                  } else {
                    return (
                      <TableCell key={`${item.id}-${column.key}`} align="right">
                        {column?.actions &&
                          column?.actions.map((action, index) => (
                            <IconButton
                              key={index}
                              size="small"
                              onClick={() => action.onClick(item)}
                            >
                              {action?.icon}
                            </IconButton>
                          ))}
                      </TableCell>
                    );
                  }
                })}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </TableComponentWrapper>
  );
};

export default MyTable;
