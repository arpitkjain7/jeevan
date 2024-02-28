import React, { useEffect, useState } from "react";
import MyTable from "../../components/TableComponent";
import { Typography, styled, Button } from "@mui/material";
import { useDispatch } from "react-redux";
import { fetchPatientList, verifyAbhaPatient} from "./patientpage.slice";
import { createAppointment } from "../../components/ScheduleAppointment/scheduleAppointment.slice";
import { convertDateFormat } from "../../utils/utils";
import { useNavigate } from "react-router-dom";
import { AppointmentPageActions } from "../AppointmentPage/AppointmentPage.slice";
import { fetchDoctorList } from "../../components/AppointmentForm/AppointmentForm.slice";
import CustomLoader from "../../components/CustomLoader";
const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const ListWrapper = styled("div")(({ theme }) => ({
  "&": {
    padding: "20px 10px 10px",
    [theme.breakpoints.down('sm')]: {
      padding: "10px"
    }
  },
  ".patientList-title-wrapper": {
    marginBottom: "20px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    [theme.breakpoints.down('md')]: {
      display: "block",
    },
  },
  ".patientList-heading": {
    "&.MuiTypography-root": theme.typography.h1,
    [theme.breakpoints.down('sm')]: {
      fontSize: "30px"
    },
  },
  ".patientList-desc": theme.typography.h2,
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
        backgroundColor: theme.palette.primaryWhite,
      },
      "& .MuiButtonBase-root .MuiSvgIcon-root": {
        color: theme.palette.secondaryBlue,
      },
    },
  },
  ".header-btn": {
    "&.MuiButtonBase-root": theme.typography.primaryButton,
    [theme.breakpoints.down('md')]: {
      marginTop: "10px"
    },
  },
}));

const searchInputStyle = {
  width: "200px",
  height: "40px",
  backgroundColor: "#f1f1f1",
};

const PatientPage = () => {
  const hospital = sessionStorage?.getItem("selectedHospital");
  const [tableData, setTableData] = useState([]);
  // const [hospitalDetails, setHospitalDetails] = useState({});
  const [showLoader, setShowLoader] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const isMobile = window.innerWidth < 600;

  const currentDateAndTime = () => {
    const currentDatetime = new Date();
    const year = currentDatetime.getFullYear();
    const month = String(currentDatetime.getMonth() + 1).padStart(2, "0"); // Month is zero-indexed
    const day = String(currentDatetime.getDate()).padStart(2, "0");
    const hours = String(currentDatetime.getHours()).padStart(2, "0");
    const minutes = String(currentDatetime.getMinutes()).padStart(2, "0");
    const formattedDatetime = `${year}-${month}-${day} ${hours}:${minutes}`;
    return formattedDatetime;
  };

  const currentDateEndTime = () => {
    const currentDatetime = new Date();
    const year = currentDatetime.getFullYear();
    const month = String(currentDatetime.getMonth() + 1).padStart(2, "0"); // Month is zero-indexed
    const day = String(currentDatetime.getDate()).padStart(2, "0");
    currentDatetime.setMinutes(currentDatetime.getMinutes() + 15);
    const hours = String(currentDatetime.getHours()).padStart(2, "0");
    const minutes = String(currentDatetime.getMinutes()).padStart(2, "0");
    const formattedDatetime = `${year}-${month}-${day} ${hours}:${minutes}`;
    return formattedDatetime;
  };
  
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
      ],
    },
    { key: "id", header: "Patient ID" },
    { key: "abha_number", header: "ABHA Number" },
    { key: "mobile_number", header: "Contact Number" },
    { key: "updatedDate", header: "Last Visited" },
    { key: "createdDate", header: "Follow Up" },
    {
      key: "actions",
      header: "Create Appointment",
      actions: [
        {
          link: "Create Appointment",
          type: "link",
          onClick: (item) => {
            if(item.is_verified){
              sessionStorage.setItem("selectedPatient", JSON.stringify(item));
              sessionStorage.removeItem("doctorName");
              sessionStorage.removeItem("encounterTypeValue");
              sessionStorage.removeItem("appointmentTypeValue");
              sessionStorage.removeItem("visitTypeValue");
              sessionStorage.removeItem("billingTypeValue");
              dispatch(AppointmentPageActions.setSelectedPatientData(item));
              navigate("/create-appointment");
            } else {
              dispatch(verifyAbhaPatient({ patient_id: item?.id}));
              window.location.reload();
            }
          },
        },
      ],
    },
    {
      key: "start_visit",
      header: "Start Appointment",
      actions: [
        {
          link: "Start Visit",
          type: "link",
          onClick: (row) => {
            if(row.is_verified){
              let currentHospital = {};
              if (hospital) {
                currentHospital = JSON.parse(hospital);
                const doctorListpayload = {
                  hip_id: currentHospital?.hip_id,
                };
        
                dispatch(fetchDoctorList(doctorListpayload)).then((doctorListResponse) => {
                  const payload = {
                    doc_id: doctorListResponse?.payload[0]?.id,
                    patient_id: row?.id,
                    appointment_type: "first visit",
                    encounter_type: "emergency",
                    hip_id: currentHospital?.hip_id,
                    appointment_start: currentDateAndTime(),
                    appointment_end: currentDateEndTime()
                  };
                  
                  dispatch(createAppointment(payload)).then((res) => {
                    if (res.payload?.appointment_id) {
                      const AllPatientData = Object.assign(
                        row,
                        { patientId: row.id },
                        { doc_id: doctorListResponse?.payload[0]?.id },
                        { doc_name: doctorListResponse?.payload[0]?.doc_name },
                        { hip_id: currentHospital?.hip_id }, 
                        { id: res.payload?.appointment_id }
                      )
                      sessionStorage.setItem("selectedPatient", JSON.stringify(AllPatientData));
                      setTimeout(() => navigate("/patient-emr"), 500);
                    }
                  });
                })
              }
            } else {
              dispatch(verifyAbhaPatient({ patient_id: row?.id}));
              window.location.reload();
            }
          },
        },
      ],
    },
    // {
    //   key: "actions",
    //   header: "",
    //   actions: [
    //     {
    //       icon: <img src={MenuIcon} alt="menu" />,
    //       type: "icon",
    //       onClick: (item) => {
    //         console.log(item, "item");
    //       },
    //     },
    //   ],
    // },
  ];
  const mobileColumns = [
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
      ],
    },
    {
      key: "actions",
      header: "Create Appointment",
      actions: [
        {
          link: "Create Appointment",
          type: "link",
          onClick: (item) => {
            if(item.is_verified){
              sessionStorage.setItem("selectedPatient", JSON.stringify(item));
              sessionStorage.removeItem("doctorName");
              sessionStorage.removeItem("encounterTypeValue");
              sessionStorage.removeItem("appointmentTypeValue");
              sessionStorage.removeItem("visitTypeValue");
              sessionStorage.removeItem("billingTypeValue");
              dispatch(AppointmentPageActions.setSelectedPatientData(item));
              navigate("/create-appointment");
            } else {
              dispatch(verifyAbhaPatient({ patient_id: item?.id}));
              window.location.reload();
            }
          },
        },
      ],
    },
    {
      key: "start_visit",
      header: "Start Appointment",
      actions: [
        {
          link: "Start Visit",
          type: "link",
          onClick: (row) => {
            if(row.is_verified){
              let currentHospital = {};
              if (hospital) {
                currentHospital = JSON.parse(hospital);
                const doctorListpayload = {
                  hip_id: currentHospital?.hip_id,
                };
        
                dispatch(fetchDoctorList(doctorListpayload)).then((doctorListResponse) => {
                  const payload = {
                    doc_id: doctorListResponse?.payload[0]?.id,
                    patient_id: row?.id,
                    appointment_type: "first visit",
                    encounter_type: "emergency",
                    hip_id: currentHospital?.hip_id,
                    appointment_start: currentDateAndTime(),
                    appointment_end: currentDateEndTime()
                  };
                  
                  dispatch(createAppointment(payload)).then((res) => {
                    if (res.payload?.appointment_id) {
                      const AllPatientData = Object.assign(
                        row,
                        { patientId: row.id },
                        { doc_id: doctorListResponse?.payload[0]?.id },
                        { hip_id: currentHospital?.hip_id }, 
                        { id: res.payload?.appointment_id }
                      )
                      sessionStorage.setItem("selectedPatient", JSON.stringify(AllPatientData));
                      setTimeout(() => navigate("/patient-emr"), 500);
                    }
                  });
                })
              }
            } else {
              dispatch(verifyAbhaPatient({ patient_id: row?.id}));
              window.location.reload();
            }
          },
        },
      ],
    },
    { key: "id", header: "Patient ID" },
    { key: "abha_number", header: "ABHA Number" },
    { key: "mobile_number", header: "Contact Number" },
    { key: "updatedDate", header: "Last Visited" },
    { key: "createdDate", header: "Follow Up" },
  ];

  useEffect(() => {
    setShowLoader(true);
    dispatch(AppointmentPageActions.setSelectedPatientData({}));
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      // setHospitalDetails(currentHospital);
      const payload = {
        hip_id: currentHospital?.hip_id,
      };
      dispatch(fetchPatientList(payload)).then((res) => {
        setShowLoader(false);
        const patientList = res?.payload;
        const formattedPatientList = patientList?.map((item) => {
          const patientGender = item?.gender.toLowerCase()?.includes("m")
            ? "M"
            : "F";
          const updatedDate = convertDateFormat(item?.updated_at, "dd/MM/yyyy");
          const createdDate = convertDateFormat(item?.created_at, "dd/MM/yyyy");
          return {
            patientDetails: `${item.name || ""} | ${patientGender || ""}`,
            p_name: `${item.name}`,
            updatedDate: updatedDate,
            createdDate: createdDate,
            ...item,
          };
        });
        setTableData(formattedPatientList);
      });
    }
  }, []);

  const onTableRowClick = (row) => {};

  return (
    <ListWrapper>
      <CustomLoader
        open={showLoader}
      />
      <div className="patientList-title-wrapper">
        <div>
          <Typography className="patientList-heading">Patient List</Typography>
          <Typography className="patientList-desc">
            Manage your patient information
          </Typography>
        </div>
        <Button
          variant="contained"
          className="header-btn"
          onClick={() => navigate("/patient-registration")}
        >
          Register New Patient
        </Button>
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
            onRowClick={(row) => onTableRowClick(row)}
          />
        ) : (
          <MyTable
          columns={columns}
          data={tableData}
          tableStyle={tableStyle}
          searchInputStyle={searchInputStyle}
          tableClassName="table-class"
          searchClassName="search-class"
          onRowClick={(row) => onTableRowClick(row)}
        />
        )}
      </div>
    </ListWrapper>
  );
};

export default PatientPage;
