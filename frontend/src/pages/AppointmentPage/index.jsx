import React, { useEffect, useState } from "react";
import MyTable from "../../components/TableComponent";
import MenuIcon from "@mui/icons-material/Menu";
import { Typography, styled } from "@mui/material";
import { useDispatch } from "react-redux";
import { fetchAppointmentList } from "./AppointmentPage.slice";
import { convertDateFormat } from "../../utils/utils";

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

const columns = [
  { key: "patientDetails", header: "Patient Name" },
  { key: "abha_number", header: "Abha Id" },
  { key: "mobile_number", header: "Contact Number" },
  { key: "updatedDate", header: "Last Visited" },
  { key: "createdDate", header: "Follow Up" },
  { key: "abha_status", header: "Status" },
  {
    key: "actions",
    header: "",
    actions: [
      {
        link: "Start Visit",
        type: "link",
        onClick: (item) => {
          // Handle edit action for the specific item
        },
      },
    ],
  },
  {
    key: "actions",
    header: "",
    actions: [
      {
        icon: <MenuIcon />,
        type: "icon",
        onClick: (item) => {
          // Handle edit action for the specific item
        },
      },
    ],
  },
];

const searchInputStyle = {
  width: "200px",
  height: "40px",
  backgroundColor: "#f1f1f1",
};

const AppointmentPage = () => {
  const hospital = localStorage?.getItem("selectedHospital");
  const [tableData, setTableData] = useState([]);
  const [hospitalDetails, setHospitalDetails] = useState({});
  const dispatch = useDispatch();

  useEffect(() => {
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      console.log(currentHospital);
      setHospitalDetails(currentHospital);
      const payload = {
        hip_id: currentHospital?.hip_id,
      };
      dispatch(fetchAppointmentList(payload)).then((res) => {
        const mainList = res.payload;
        let patientList = [];
        mainList?.map((item) => {
          patientList?.push(item[0]);
        });
        const formattedPatientList = patientList?.map((item) => {
          // const patientGender = item?.gender.toLowerCase()?.includes("m")
            // ? "M"
            // : "F";
          // const updatedDate = convertDateFormat(item?.updated_at);
          // const createdDate = convertDateFormat(item?.created_at);
          return {
            // patientDetails: `${item.name} | ${patientGender}`,
            // updatedDate: updatedDate,
            // createdDate: createdDate,
            // ...item,
          };
        });
        console.log(formattedPatientList, "patient");
        setTableData(formattedPatientList);
      });
    }
  }, []);
  return (
    <ListWrapper>
      <div className="patientList-title-wrapper">
        <Typography className="patientList-heading">Appointment List</Typography>
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

export default AppointmentPage;
