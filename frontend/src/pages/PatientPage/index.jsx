import React, { useEffect, useState } from "react";
import MyTable from "../../components/TableComponent";
import MenuIcon from "@mui/icons-material/Menu";
import { Typography, styled } from "@mui/material";
import { useDispatch } from "react-redux";
import { fetchPatientList } from "./patientpage.slice";
import { useNavigate } from "react-router-dom";

const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const ListWrapper = styled("div")(({ theme }) => ({
  "&": {},
  ".patientList-title-wrapper": {
    marginBottom: "40px",
  },
  ".patientList-heading": {
    "&.MuiTypography-root": {
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "28px",
      lineHeight: "160%",
    },
  },
  ".patientList-desc": {
    "&.MuiTypography-root": {
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      lineHeight: "160%",
    },
  },
  ".table-class": {
    "&.MuiPaper-root": {
      borderRadius: "0",
      boxShadow: "none",
    },
    "& .MuiTableHead-root": {
      backgroundColor: theme.palette.primaryGrey,
      "& > tr >th": {
        color: theme.palette.primaryBlack,
        fontFamily: "Inter",
        fontWeight: "500",
        fontSize: "16px",
        lineHeight: "16px",
      },
    },
    "& .MuiTableBody-root": {
      "& > tr >td": {
        color: theme.palette.primaryBlack,
        fontFamily: "Inter",
        fontWeight: "500",
        fontSize: "16px",
        lineHeight: "16px",
      },
    },
  },
  ".search-class": {
    "&.MuiFormControl-root": {
      flex: 0.3,
      padding: 0,
      margin: 0,
      "& .MuiInputBase-input": {
        padding: "12px 16px",
      },
    },
  },
}));



const data = [
  {
    id: 1,
    patient_name: "Item 1",
    abha_id: "12345",
    contact_number: "9876543210",
    last_visited: "yesterday",
    status: "",
  },
  {
    id: 2,
    patient_name: "Item 2",
    abha_id: "12345",
    contact_number: "9876543210",
    status: "",
    last_visited: "yesterday",
  },
  {
    id: 3,
    patient_name: "Item 3",
    abha_id: "12345",
    contact_number: "9876543210",
    status: "",
    last_visited: "yesterday",
  },
];

const searchInputStyle = {
  width: "200px",
  height: "40px",
  backgroundColor: "#f1f1f1",
};

const PatientPage = () => {
  const hospital = localStorage?.getItem("selectedHospital");
  const [tableData, setTableData] = useState([]);
  const [hospitalDetails, setHospitalDetails] = useState({});
  const dispatch = useDispatch();
  const navigate = useNavigate()

  const columns = [
    { key: "name", header: "Patient Name" },
    { key: "abha_number", header: "Abha Id" },
    { key: "mobile_number", header: "Contact Number" },
    { key: "state_code", header: "Last Visited" },
    { key: "abha_status", header: "Status" },
    {
      key: "actions",
      header: "",
      actions: [
        {
          icon: <MenuIcon />,
          onClick: (item) => {
            // Handle edit action for the specific item
          },
        },
      ],
    },
  ];

  useEffect(() => {
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      console.log(currentHospital);
      setHospitalDetails(currentHospital);
      const payload = {
        hip_id: currentHospital?.hip_id,
      };
      dispatch(fetchPatientList(payload)).then((res) => {
        const mainList = res.payload
        
        console.log(mainList,"patient");
        setTableData(mainList)
      });
    }
  }, []);
  return (
    <ListWrapper>
      <div className="patientList-title-wrapper">
        <Typography className="patientList-heading">Patient List</Typography>
        <Typography className="patientList-desc">Description</Typography>
      </div>
      <div className="table-container">
        <MyTable
          columns={columns}
          data={tableData}
          tableStyle={tableStyle}
          searchInputStyle={searchInputStyle}
          tableClassName="table-class"
          searchClassName="search-class"
        />
      </div>
    </ListWrapper>
  );
};

export default PatientPage;
