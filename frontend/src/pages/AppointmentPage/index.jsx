import React, { useEffect, useState } from "react";
import MyTable from "../../components/TableComponent";
import MenuIcon from "@mui/icons-material/Menu";
import { Typography, styled } from "@mui/material";
import { useDispatch } from "react-redux";
import { fetchAppointmentList } from "./AppointmentPage.slice";
import { convertDateFormat, convertTimeSlot } from "../../utils/utils";
import { useNavigate } from "react-router";

const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const ListWrapper = styled("div")(({ theme }) => ({
  "&": {
    padding: "40px 10px 10px",
    [theme.breakpoints.down('sm')]: {
      padding: "10px",
    }
  },
  ".patientList-title-wrapper": {
    marginBottom: "25px",
    [theme.breakpoints.down('sm')]: {
      marginBottom: "20px",
    }
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
      "& > tr >th": {
        "&": theme.typography.h3,
        [theme.breakpoints.down('md')]: {
          "&": theme.typography.body2
        },
        padding: theme.spacing(4),
      },
    },
    "& .MuiTableBody-root": {
      "& > tr >td": {
        "&": theme.typography.body1,
        cursor: "pointer",
        padding: theme.spacing(4),
      },
    },
  },
  ".search-class": {
    "&.MuiFormControl-root": {
      flex: 0.3,
      padding: 0,
      margin: 0,
      [theme.breakpoints.down('sm')]: {
        flex: "1 "
      },
      "& .MuiInputBase-input": {
        padding: "12px 16px",
      },
    },
  },
}));

const searchInputStyle = {
  width: "200px",
  height: "40px",
  backgroundColor: "#f1f1f1",
};

const AppointmentPage = () => {
  const hospital = sessionStorage?.getItem("selectedHospital");
  const [tableData, setTableData] = useState([]);
  const [hospitalDetails, setHospitalDetails] = useState({});
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const columns = [
    { key: "patientDetails", header: "Patient Name" },
    { key: "patientId", header: "Patient ID" },
    { key: "mobileNumber", header: "Contact Number" },
    { key: "encounterType", header: "Encounter Type" },
    { key: "docName", header: "Doctor" },
    { key: "slotDate", header: "Date" },
    { key: "slotTime", header: "Slot" },
    { key: "status", header: "Status" },
    {
      key: "actions",
      actions: [
        {
          key: "action",
          type: "link",
          onClick: (item) => {
            navigate("/patient-emr");
            sessionStorage.setItem("selectedPatient", JSON.stringify(item));
          },
        },
      ],
    },
  ];

  const mobileColumns = [
    { key: "patientDetails", header: "Patient Name" },
    {
      key: "actions",
      header: "Start Visit",
      actions: [
        {
          key: "action",
          type: "link",
          onClick: (item) => {
            navigate("/patient-emr");
            sessionStorage.setItem("selectedPatient", JSON.stringify(item));
          },
        },
      ],
    },
    { key: "patientId", header: "Patient ID" },
    { key: "mobileNumber", header: "Contact Number" },
    { key: "encounterType", header: "Encounter Type" },
    { key: "docName", header: "Doctor" },
    { key: "slotDate", header: "Date" },
    { key: "slotTime", header: "Slot" },
    { key: "status", header: "Status" }
  ];

  useEffect(() => {
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      setHospitalDetails(currentHospital);
      const payload = {
        hip_id: currentHospital?.hip_id,
      };
      dispatch(fetchAppointmentList(payload)).then((res) => {
        const mainList = res.payload;
        // let patientList = [];
        // mainList?.map((item) => {
        //   patientList?.push(item[1]);
        // });
        const formattedAppointmentList = mainList?.map((item) => {
          const patientId = item?.patient_id;
          const patientGender = item?.patient_details?.gender
            .toLowerCase()
            ?.includes("m")
            ? "M"
            : "F";
          const mobileNumber = item?.patient_details?.mobile_number;
          const encounterType = item?.appointment_type;
          const docName = item?.doc_details?.doc_name;
          const slotDate = convertDateFormat(item?.slot_details?.date, "dd/MM/yyyy");
          const slotTime = convertTimeSlot(item?.slot_time);
          const status = item?.consultation_status;
          let action = "Start Visit";
          if(status === "Completed") {
            action = "Edit"
          }
          else if(status === "InProgress") {
            action = "Resume"
          }
          // const updatedDate = convertDateFormat(item?.updated_at);
          // const createdDate = convertDateFormat(item?.created_at);
          return {
            patientDetails: `${item?.patient_details?.name} | ${patientGender}`,
            patientId: patientId,
            mobileNumber: mobileNumber,
            encounterType: encounterType,
            docName: docName,
            slotDate: slotDate,
            slotTime: slotTime,
            status: status,
            action: action,
            // updatedDate: updatedDate,
            // createdDate: createdDate,
            ...item,
          };
        });
        if(formattedAppointmentList.slotDate){
          const sortedData = formattedAppointmentList.sort((a, b) => {
            return new Date(a.slotDate) - new Date(b.slotDate);
          })
          setTableData(sortedData);
        } else setTableData(formattedAppointmentList);
       
      });
    }
  }, []);
  const isMobile = window.innerWidth < 600;
  return (
    <ListWrapper>
      <div className="patientList-title-wrapper">
        <Typography className="patientList-heading">
          Appointment List
        </Typography>
        <Typography className="patientList-desc">Description</Typography>
      </div>
      <div className="table-container">
        {isMobile ? (
          <MyTable
          columns={mobileColumns}
          data={tableData}
          tableStyle={tableStyle}
          searchInputStyle={searchInputStyle}
          tableClassName="table-class"
          searchClassName="search-class"
        />
        ) : (
        <MyTable
          columns={columns}
          data={tableData}
          tableStyle={tableStyle}
          searchInputStyle={searchInputStyle}
          tableClassName="table-class"
          searchClassName="search-class"
        />
        )}
      </div>
    </ListWrapper>
  );
};

export default AppointmentPage;