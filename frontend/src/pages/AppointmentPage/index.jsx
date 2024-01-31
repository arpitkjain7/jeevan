import React, { useEffect, useState } from "react";
import MyTable from "../../components/TableComponent";
import { Typography, styled } from "@mui/material";
import { useDispatch } from "react-redux";
import { AppointmentPageActions, fetchAppointmentList } from "./AppointmentPage.slice";
import { convertDateFormat, convertTimeSlot } from "../../utils/utils";
import { useNavigate } from "react-router";
import CustomLoader from "../../components/CustomLoader";

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
      marginRight: "10px",
      [theme.breakpoints.up('sm')]: {
        width: "300px !important",
      },
      [theme.breakpoints.down('sm')]: {
        flex: "1 "
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
  const [showLoader, setShowLoader] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const columns = [
    { 
      key: "p_name", 
      header: "Patient Name",
      actions: [
        {
          type: "link",
          onClick: (row) => {
            dispatch(AppointmentPageActions.setSelectedPatientData(row));
            sessionStorage.setItem("selectedPatient", JSON.stringify(row));
            navigate("/patient-details");
          },
        },
      ]
    },
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
    { key: "p_name", 
      header: "Patient Name",
      actions: [
        {
          type: "link",
          onClick: (row) => {
            dispatch(AppointmentPageActions.setSelectedPatientData(row));
            sessionStorage.setItem("selectedPatient", JSON.stringify(row));
            navigate("/patient-details");
          },
        },
      ]
    },
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
    setShowLoader(true);
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = {
        hip_id: currentHospital?.hip_id,
      };
      dispatch(fetchAppointmentList(payload)).then((res) => {
        setShowLoader(false);
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
            p_name: `${item?.patient_details?.name}`,
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
        if(formattedAppointmentList){
          const sortedData = formattedAppointmentList.sort((a, b) => {
            const dateA = new Date(a.slot_details.date);
            const dateB = new Date(b.slot_details.date);
    
            if (dateA < dateB) {
              return -1;
            }
            else return 1;
          });
          setTableData(sortedData);
        } 
      });
    }
  }, []);
  const isMobile = window.innerWidth < 600;
  return (
    <ListWrapper>
      <CustomLoader
        open={showLoader}
      />
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
          showFilter = "true"
          tableClassName="table-class"
          searchClassName="search-class"
        />
        ) : (
        <MyTable
          columns={columns}
          data={tableData}
          tableStyle={tableStyle}
          searchInputStyle={searchInputStyle}
          showFilter = "true"
          tableClassName="table-class"
          searchClassName="search-class"
        />
        )}
      </div>
    </ListWrapper>
  );
};

export default AppointmentPage;