import React, { useEffect, useState } from "react";
import AppointmentTable from "../../components/AppointmentTable";
import { Typography, styled } from "@mui/material";
import { useDispatch } from "react-redux";
import {
  AppointmentPageActions,
  fetchAppointmentList,
  fetchPatientDetails,
  listAppointmentByDate,
} from "./AppointmentPage.slice";
import { convertDateFormat, convertTimeSlot } from "../../utils/utils";
import { useNavigate } from "react-router";
import CustomLoader from "../../components/CustomLoader";
import CustomSnackbar from "../../components/CustomSnackbar";

const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const ListWrapper = styled("div")(({ theme }) => ({
  "&": {
    padding: "20px 10px 10px",
    [theme.breakpoints.down("sm")]: {
      padding: "10px",
    },
  },
  ".patientList-title-wrapper": {
    marginBottom: "25px",
    [theme.breakpoints.down("sm")]: {
      marginBottom: "20px",
    },
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
        [theme.breakpoints.down("md")]: {
          "&": theme.typography.body2,
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
      [theme.breakpoints.up("sm")]: {
        width: "300px !important",
      },
      [theme.breakpoints.down("sm")]: {
        flex: "1 ",
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
  const [followUpData, setFollowUpData] = useState([]);
  const [appointmentData, setAppointmentData] = useState([]);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [filterDateValue, setFilterDateValue] = useState(
    convertDateFormat(new Date(), "yyyy-MM-dd")
  );

  const columns = [
    {
      key: "p_name",
      header: "Patient Name",
      actions: [
        {
          type: "link",
          onClick: (row) => {
            // dispatch(AppointmentPageActions.setSelectedPatientData(row));
            dispatch(fetchPatientDetails(row?.patient_id)).then((response) => {
              if (response?.payload) {
                sessionStorage.setItem(
                  "selectedPatient",
                  JSON.stringify(response?.payload)
                );
                navigate("/patient-details");
              } else {
                setShowSnackbar(true);
                setErrorMessage("Error while fetching details");
              }
            });
          },
        },
      ],
    },
    { key: "patientUid", header: "Patient ID" },
    { key: "mobileNumber", header: "Contact Number" },
    { key: "encounterType", header: "Encounter Type" },
    { key: "doc_name", header: "Doctor" },
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
    {
      key: "p_name",
      header: "Patient Name",
      actions: [
        {
          type: "link",
          onClick: (row) => {
            dispatch(fetchPatientDetails(row?.patient_id)).then((response) => {
              if (response?.payload) {
                sessionStorage.setItem(
                  "selectedPatient",
                  JSON.stringify(response?.payload)
                );
                navigate("/patient-details");
              } else {
                setShowSnackbar(true);
                setErrorMessage("Error while fetching details");
              }
            });
          },
        },
      ],
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
    { key: "patientUid", header: "Patient ID" },
    { key: "mobileNumber", header: "Contact Number" },
    { key: "encounterType", header: "Encounter Type" },
    { key: "doc_name", header: "Doctor" },
    { key: "slotDate", header: "Date" },
    { key: "slotTime", header: "Slot" },
    { key: "status", header: "Status" },
  ];

  const followUpColumns = [
    {
      key: "p_name",
      header: "Patient Name",
      actions: [
        {
          type: "link",
          onClick: (row) => {
            dispatch(fetchPatientDetails(row?.patient_id)).then((response) => {
              if (response?.payload) {
                sessionStorage.setItem(
                  "selectedPatient",
                  JSON.stringify(response?.payload)
                );
                navigate("/patient-details");
              } else {
                setShowSnackbar(true);
                setErrorMessage("Error while fetching details");
              }
            });
          },
        },
      ],
    },
    { key: "patientUid", header: "Patient ID" },
    { key: "mobileNumber", header: "Contact Number" },
    { key: "type", header: "Encounter Type" },
    { key: "doc_name", header: "Doctor" },
    { key: "slotDate", header: "Date" },
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

  const mobilefollowUpColumns = [
    {
      key: "p_name",
      header: "Patient Name",
      actions: [
        {
          type: "link",
          onClick: (row) => {
            dispatch(fetchPatientDetails(row?.patient_id)).then((response) => {
              if (response?.payload) {
                sessionStorage.setItem(
                  "selectedPatient",
                  JSON.stringify(response?.payload)
                );
                navigate("/patient-details");
              } else {
                setShowSnackbar(true);
                setErrorMessage("Error while fetching details");
              }
            });
          },
        },
      ],
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
    { key: "patientUid", header: "Patient ID" },
    { key: "mobileNumber", header: "Contact Number" },
    { key: "type", header: "Encounter Type" },
    { key: "doc_name", header: "Doctor" },
    { key: "slotDate", header: "Date" },
  ];
  useEffect(() => {
    fetchList();
  }, []);

  const fetchList = (date) => {
    setShowLoader(true);
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = {
        hipId: currentHospital?.hip_id,
        appointmentDate: date || filterDateValue,
      };
      dispatch(listAppointmentByDate(payload)).then((res) => {
        setShowLoader(false);
        let mainList = res?.payload?.appointments;
        let followUpList = res?.payload?.follow_ups;
        // let patientList = [];
        // mainList?.map((item) => {
        //   patientList?.push(item[1]);
        // });
        const formattedAppointmentList = mainList?.map((item) => {
          const patientId = item?.patient_id;
          const patientUid = item?.patient_details?.patient_uid;
          const patientGender = item?.patient_details?.gender
            .toLowerCase()
            ?.includes("m")
            ? "M"
            : "F";
          const mobileNumber = item?.patient_details?.mobile_number;
          const encounterType = item?.appointment_type;
          const slotDate = item?.appointment_date
            ? convertDateFormat(item?.appointment_date, "dd/MM/yyyy")
            : "";
          const slotTime = item?.slot_time
            ? convertTimeSlot(item?.slot_time)
            : "";
          const status = item?.consultation_status;
          let action = "Start Visit";
          if (status === "Completed") {
            action = "Edit";
          } else if (status === "InProgress") {
            action = "Resume";
          }
          const updatedDate = item?.updated_at
            ? convertDateFormat(item?.updated_at, "dd/MM/yyyy")
            : "";
          const createdDate = item?.created_at
            ? convertDateFormat(item?.created_at, "dd/MM/yyyy")
            : "";
          return {
            patientDetails: `${item?.patient_details?.name} | ${patientGender}`,
            p_name: `${item?.patient_details?.name}`,
            patientId: patientId,
            patientUid: patientUid,
            mobileNumber: mobileNumber,
            encounterType: encounterType,
            doc_name: item?.doc_details?.doc_name,
            slotDate: slotDate,
            slotTime: slotTime,
            status: status,
            action: action,
            updatedDate: updatedDate,
            createdDate: createdDate,
            type: "appointment",
            ...item,
          };
        });

        if (formattedAppointmentList) {
          const sortedApmntData = formattedAppointmentList.sort((a, b) => {
            const dateA = new Date(a.slotDate); //slot_details.date);
            const dateB = new Date(b.slotDate);

            if (dateA < dateB) {
              return -1;
            } else return 1;
          });
          // setTableData(sortedApmntData);
          setAppointmentData(sortedApmntData);
        }
        // if(formattedAppointmentList){
        //   const sortedData = formattedAppointmentList.sort((a, b) => {
        //     const dateA = new Date(a.slotDate);//slot_details.date);
        //     const dateB = new Date(b.slotDate);

        //     if (dateA < dateB) {
        //       return -1;
        //     }
        //     else return 1;
        //   });
        //   setTableData(sortedData);
        // }

        const formattedFollowUpList = followUpList?.map((item) => {
          const patient_id = item?.patient_details?.id;

          const patientUid = item?.patient_details?.patient_uid;
          const patientGender = item?.patient_details?.gender
            .toLowerCase()
            ?.includes("m")
            ? "M"
            : "F";
          const mobileNumber = item?.patient_details?.mobile_number;
          const slotDate = item?.followup_date
            ? convertDateFormat(item?.followup_date, "dd/MM/yyyy")
            : "";
          // const slotTime = item?.slot_time ? convertTimeSlot(item?.slot_time) : "";
          // const status = item?.consultation_status;
          let action = "Start Visit";
          const updatedDate = item?.updated_at
            ? convertDateFormat(item?.updated_at, "dd/MM/yyyy")
            : "";
          const createdDate = item?.created_at
            ? convertDateFormat(item?.created_at, "dd/MM/yyyy")
            : "";
          return {
            patientDetails: `${item?.patient_details?.name} | ${patientGender}`,
            p_name: `${item?.patient_details?.name}`,
            patient_id,
            patientUid: patientUid,
            mobileNumber: mobileNumber,
            doc_name: item?.doc_details?.doc_name,
            slotDate: slotDate,
            action: action,
            updatedDate: updatedDate,
            createdDate: createdDate,
            type: "Follow Up",
            ...item,
          };
        });

        // const finalData = formattedAppointmentList.concat(formattedFollowUpList);

        if (formattedFollowUpList) {
          const sortedFollowUpData = formattedFollowUpList.sort((a, b) => {
            const dateA = new Date(a.slotDate); //slot_details.date);
            const dateB = new Date(b.slotDate);

            if (dateA < dateB) {
              return -1;
            } else return 1;
          });
          setFollowUpData(sortedFollowUpData);
        }
      });
    }
  };
  const handleDateChange = (event) => {
    setFilterDateValue(event.target.value);
    fetchList(event.target.value);
  };

  const onSnackbarClose = () => {
    setShowSnackbar(false);
  };

  const isMobile = window.innerWidth < 600;
  return (
    <ListWrapper>
      <CustomLoader open={showLoader} />
      <CustomSnackbar
        message={errorMessage || "Something went wrong"}
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
      <div className="patientList-title-wrapper">
        <Typography className="patientList-heading">
          Appointment List
        </Typography>
        <Typography className="patientList-desc">Description</Typography>
      </div>
      <div className="table-container">
        {isMobile ? (
          <AppointmentTable
            apmntColumns={mobileColumns}
            followUpColumns={mobilefollowUpColumns}
            data={tableData}
            tableStyle={tableStyle}
            searchInputStyle={searchInputStyle}
            handleDateChange={handleDateChange}
            filterDateValue={filterDateValue}
            followUpData={followUpData}
            appointmentData={appointmentData}
            showFilter="true"
            tableClassName="table-class"
            searchClassName="search-class"
          />
        ) : (
          <AppointmentTable
            apmntColumns={columns}
            followUpColumns={followUpColumns}
            data={tableData}
            tableStyle={tableStyle}
            searchInputStyle={searchInputStyle}
            handleDateChange={handleDateChange}
            filterDateValue={filterDateValue}
            followUpData={followUpData}
            appointmentData={appointmentData}
            showFilter="true"
            tableClassName="table-class"
            searchClassName="search-class"
          />
        )}
      </div>
    </ListWrapper>
  );
};

export default AppointmentPage;
