import React, { useEffect, useState } from "react";
import AppointmentTable from "../../components/AppointmentTable";
import { Typography, styled } from "@mui/material";
import { useDispatch } from "react-redux";
import { AppointmentPageActions, fetchAppointmentList, listAppointmentByDate } from "./AppointmentPage.slice";
import { convertDateFormat, convertTimeSlot } from "../../utils/utils";
import { useNavigate } from "react-router";
import CustomLoader from "../../components/CustomLoader";

const tableStyle = {
  backgroundColor: "#f1f1f1",
};

const ListWrapper = styled("div")(({ theme }) => ({
  "&": {
    padding: "20px 10px 10px",
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
  const [followUpData, setFollowUpData] = useState([]);
  const [appointmentData, setAppointmentData] = useState([]);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [filterDateValue, setFilterDateValue] = useState(convertDateFormat(new Date(), "yyyy-MM-dd"));
//   const res = {
//     "payload": {
//         "appointments": [
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1387,
//                 "doc_id": 1,
//                 "id": 1356,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T12:10:51.978508",
//                 "patient_id": "C360-PID-337084625274822016",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T00:48:16.930884",
//                 "patient_details": {
//                     "mobile_number": "9871711177",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T23:47:02.690228",
//                     "name": "Rahul  M Mahant",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-20T09:31:30.984378",
//                     "primary_abha_address": null,
//                     "gender": "F",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID90",
//                     "DOB": "1985-06-15",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "rahul@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1985",
//                     "id": "C360-PID-337084625274822016",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 38,
//                     "age_in_months": 11
//                 },
//                 "slot_time": "00:48 - 01:03",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1389,
//                 "doc_id": 1,
//                 "id": 1358,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T10:17:57.074725",
//                 "patient_id": "C360-PID-337084625274822016",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T00:55:44.775385",
//                 "patient_details": {
//                     "mobile_number": "9871711177",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T23:47:02.690228",
//                     "name": "Rahul  M Mahant",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-20T09:31:30.984378",
//                     "primary_abha_address": null,
//                     "gender": "F",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID90",
//                     "DOB": "1985-06-15",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "rahul@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1985",
//                     "id": "C360-PID-337084625274822016",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 38,
//                     "age_in_months": 11
//                 },
//                 "slot_time": "00:55 - 01:10",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1390,
//                 "doc_id": 1,
//                 "id": 1359,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T09:14:44.349537",
//                 "patient_id": "C360-PID-337084625274822016",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T01:16:43.505768",
//                 "patient_details": {
//                     "mobile_number": "9871711177",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T23:47:02.690228",
//                     "name": "Rahul  M Mahant",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-20T09:31:30.984378",
//                     "primary_abha_address": null,
//                     "gender": "F",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID90",
//                     "DOB": "1985-06-15",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "rahul@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1985",
//                     "id": "C360-PID-337084625274822016",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 38,
//                     "age_in_months": 11
//                 },
//                 "slot_time": "01:16 - 01:31",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1391,
//                 "doc_id": 1,
//                 "id": 1360,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T01:17:07.304657",
//                 "patient_id": "C360-PID-690921785381560456",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T01:17:06.621371",
//                 "patient_details": {
//                     "mobile_number": "9511878113",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T13:40:06.709428",
//                     "name": "Rachit  Khandelwal",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-19T13:40:06.709462",
//                     "primary_abha_address": null,
//                     "gender": "M",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID89",
//                     "DOB": "1999-08-04",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "samarth@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1999",
//                     "id": "C360-PID-690921785381560456",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 24,
//                     "age_in_months": 9
//                 },
//                 "slot_time": "01:17 - 01:32",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1392,
//                 "doc_id": 1,
//                 "id": 1361,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T09:25:02.869867",
//                 "patient_id": "C360-PID-230601464943294727",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T09:25:00.651806",
//                 "patient_details": {
//                     "mobile_number": "9511878113",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-20T09:24:37.524075",
//                     "name": "Rachit  Test 3",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-20T09:44:06.712956",
//                     "primary_abha_address": null,
//                     "gender": "M",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID91",
//                     "DOB": "1992-12-29",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "rachitkh04@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1992",
//                     "id": "C360-PID-230601464943294727",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 31,
//                     "age_in_months": 5
//                 },
//                 "slot_time": "09:25 - 09:40",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1393,
//                 "doc_id": 1,
//                 "id": 1362,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T10:02:50.439118",
//                 "patient_id": "C360-PID-337084625274822016",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T10:02:49.825471",
//                 "patient_details": {
//                     "mobile_number": "9871711177",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T23:47:02.690228",
//                     "name": "Rahul  M Mahant",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-20T09:31:30.984378",
//                     "primary_abha_address": null,
//                     "gender": "F",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID90",
//                     "DOB": "1985-06-15",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "rahul@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1985",
//                     "id": "C360-PID-337084625274822016",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 38,
//                     "age_in_months": 11
//                 },
//                 "slot_time": "10:02 - 10:17",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1380,
//                 "doc_id": 1,
//                 "id": 1349,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-19T13:40:26.763330",
//                 "patient_id": "C360-PID-690921785381560456",
//                 "appointment_type": "follow-up visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-19T13:40:22.395705",
//                 "patient_details": {
//                     "mobile_number": "9511878113",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T13:40:06.709428",
//                     "name": "Rachit  Khandelwal",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-19T13:40:06.709462",
//                     "primary_abha_address": null,
//                     "gender": "M",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID89",
//                     "DOB": "1999-08-04",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "samarth@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1999",
//                     "id": "C360-PID-690921785381560456",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 24,
//                     "age_in_months": 9
//                 },
//                 "slot_time": "10:45 - 11:00",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1398,
//                 "doc_id": 1,
//                 "id": 1367,
//                 "encounter_type": "observation encounter",
//                 "consultation_status": "Scheduled",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T12:24:50.112675",
//                 "patient_id": "C360-PID-230601464943294727",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "OBSENC",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T12:24:50.112646",
//                 "patient_details": {
//                     "mobile_number": "9511878113",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-20T09:24:37.524075",
//                     "name": "Rachit  Test 3",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-20T09:44:06.712956",
//                     "primary_abha_address": null,
//                     "gender": "M",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID91",
//                     "DOB": "1992-12-29",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "rachitkh04@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1992",
//                     "id": "C360-PID-230601464943294727",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 31,
//                     "age_in_months": 5
//                 },
//                 "slot_time": "12:45 - 13:00",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1407,
//                 "doc_id": 1,
//                 "id": 1376,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T13:20:00.989220",
//                 "patient_id": "C360-PID-337084625274822016",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T13:20:00.341359",
//                 "patient_details": {
//                     "mobile_number": "9871711177",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T23:47:02.690228",
//                     "name": "Rahul  M Mahant",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-20T09:31:30.984378",
//                     "primary_abha_address": null,
//                     "gender": "F",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID90",
//                     "DOB": "1985-06-15",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "rahul@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1985",
//                     "id": "C360-PID-337084625274822016",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 38,
//                     "age_in_months": 11
//                 },
//                 "slot_time": "13:20 - 13:35",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1408,
//                 "doc_id": 1,
//                 "id": 1377,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T13:20:28.685433",
//                 "patient_id": "C360-PID-337084625274822016",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T13:20:27.997358",
//                 "patient_details": {
//                     "mobile_number": "9871711177",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T23:47:02.690228",
//                     "name": "Rahul  M Mahant",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-20T09:31:30.984378",
//                     "primary_abha_address": null,
//                     "gender": "F",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID90",
//                     "DOB": "1985-06-15",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "rahul@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1985",
//                     "id": "C360-PID-337084625274822016",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 38,
//                     "age_in_months": 11
//                 },
//                 "slot_time": "13:20 - 13:35",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             },
//             {
//                 "hip_id": "123123",
//                 "slot_id": 1409,
//                 "doc_id": 1,
//                 "id": 1378,
//                 "encounter_type": "emergency",
//                 "consultation_status": "InProgress",
//                 "followup_date": null,
//                 "notes": null,
//                 "updated_at": "2024-05-20T13:20:49.034901",
//                 "patient_id": "C360-PID-690921785381560456",
//                 "appointment_type": "first visit",
//                 "encounter_type_code": "EMER",
//                 "token_number": null,
//                 "appointment_date": "2024-05-20",
//                 "created_at": "2024-05-20T13:20:48.441400",
//                 "patient_details": {
//                     "mobile_number": "9511878113",
//                     "town": null,
//                     "hip_id": "123123",
//                     "created_at": "2024-05-19T13:40:06.709428",
//                     "name": "Rachit  Khandelwal",
//                     "town_code": null,
//                     "abha_s3_location": null,
//                     "updated_at": "2024-05-19T13:40:06.709462",
//                     "primary_abha_address": null,
//                     "gender": "M",
//                     "district": null,
//                     "linking_token": null,
//                     "patient_uid": "PID89",
//                     "DOB": "1999-08-04",
//                     "district_code": null,
//                     "refresh_token": null,
//                     "abha_number": null,
//                     "email": "samarth@gmail.com",
//                     "pincode": null,
//                     "access_token": null,
//                     "address": null,
//                     "state_name": null,
//                     "is_verified": true,
//                     "abha_address": null,
//                     "village": null,
//                     "state_code": null,
//                     "year_of_birth": "1999",
//                     "id": "C360-PID-690921785381560456",
//                     "aadhar_number": null,
//                     "village_code": null,
//                     "auth_methods": {
//                         "authMethods": [
//                             "AADHAAR_OTP",
//                             "MOBILE_OTP",
//                             "DEMOGRAPHICS"
//                         ]
//                     },
//                     "abha_status": null,
//                     "age_in_years": 24,
//                     "age_in_months": 9
//                 },
//                 "slot_time": "13:20 - 13:35",
//                 "doc_details": {
//                     "hip_id": "123123",
//                     "id": 1,
//                     "doc_degree": null,
//                     "doc_specialization": "DUMMY",
//                     "doc_working_days": "Monday,Tuesday,Wednesday",
//                     "avg_consultation_time": "15",
//                     "consultation_end_time": "18:00:00",
//                     "created_at": "2023-12-29T21:20:45.819800",
//                     "doc_name": "Dr Arpit Jain",
//                     "affiliated": null,
//                     "doc_department": "DUMMY",
//                     "doc_licence_no": "12312",
//                     "consultation_start_time": "10:00:00",
//                     "consultation_fees": null,
//                     "follow_up_fees": null,
//                     "updated_at": "2023-12-29T21:20:45.819833"
//                 }
//             }
//         ],
//         "follow_ups": [
//           {
//             "hip_id": "123123",
//             "slot_id": 1387,
//             "doc_id": 1,
//             "id": 1356,
//             "encounter_type": "emergency",
//             "consultation_status": "InProgress",
//             "followup_date": null,
//             "notes": null,
//             "updated_at": "2024-05-20T12:10:51.978508",
//             "patient_id": "C360-PID-337084625274822016",
//             "appointment_type": "first visit",
//             "encounter_type_code": "EMER",
//             "token_number": null,
//             "appointment_date": "2024-05-20",
//             "created_at": "2024-05-20T00:48:16.930884",
//             "patient_details": {
//                 "mobile_number": "9871711177",
//                 "town": null,
//                 "hip_id": "123123",
//                 "created_at": "2024-05-19T23:47:02.690228",
//                 "name": "ABCD  M Mahant",
//                 "town_code": null,
//                 "abha_s3_location": null,
//                 "updated_at": "2024-05-20T09:31:30.984378",
//                 "primary_abha_address": null,
//                 "gender": "F",
//                 "district": null,
//                 "linking_token": null,
//                 "patient_uid": "PID90",
//                 "DOB": "1985-06-15",
//                 "district_code": null,
//                 "refresh_token": null,
//                 "abha_number": null,
//                 "email": "rahul@gmail.com",
//                 "pincode": null,
//                 "access_token": null,
//                 "address": null,
//                 "state_name": null,
//                 "is_verified": true,
//                 "abha_address": null,
//                 "village": null,
//                 "state_code": null,
//                 "year_of_birth": "1985",
//                 "id": "C360-PID-337084625274822016",
//                 "aadhar_number": null,
//                 "village_code": null,
//                 "auth_methods": {
//                     "authMethods": [
//                         "AADHAAR_OTP",
//                         "MOBILE_OTP",
//                         "DEMOGRAPHICS"
//                     ]
//                 },
//                 "abha_status": null,
//                 "age_in_years": 38,
//                 "age_in_months": 11
//             },
//             "slot_time": "00:48 - 01:03",
//             "doc_details": {
//                 "hip_id": "123123",
//                 "id": 1,
//                 "doc_degree": null,
//                 "doc_specialization": "DUMMY",
//                 "doc_working_days": "Monday,Tuesday,Wednesday",
//                 "avg_consultation_time": "15",
//                 "consultation_end_time": "18:00:00",
//                 "created_at": "2023-12-29T21:20:45.819800",
//                 "doc_name": "Dr Arpit Jain",
//                 "affiliated": null,
//                 "doc_department": "DUMMY",
//                 "doc_licence_no": "12312",
//                 "consultation_start_time": "10:00:00",
//                 "consultation_fees": null,
//                 "follow_up_fees": null,
//                 "updated_at": "2023-12-29T21:20:45.819833"
//             }
//         },
//         ]
//     },
// }
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
    { key: "patientUid", header: "Patient ID" },
    { key: "mobileNumber", header: "Contact Number" },
    { key: "encounterType", header: "Encounter Type" },
    { key: "doc_name", header: "Doctor" },
    { key: "slotDate", header: "Date" },
    { key: "slotTime", header: "Slot" },
    { key: "status", header: "Status" }
  ];

  const followUpColumns = [
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
        appointmentDate: date || filterDateValue
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
          const slotDate = item?.appointment_date ? convertDateFormat(item?.appointment_date, "dd/MM/yyyy") : "";
          const slotTime = item?.slot_time ? convertTimeSlot(item?.slot_time) : "";
          const status = item?.consultation_status;
          let action = "Start Visit";
          if(status === "Completed") {
            action = "Edit"
          }
          else if(status === "InProgress") {
            action = "Resume"
          }
          const updatedDate = item?.updated_at ? convertDateFormat(item?.updated_at, "dd/MM/yyyy") : "";
          const createdDate = item?.created_at ? convertDateFormat(item?.created_at, "dd/MM/yyyy") : "";
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
            type: 'appointment',
            ...item,
          };
        });

        if(formattedAppointmentList){
          const sortedApmntData = formattedAppointmentList.sort((a, b) => {
            const dateA = new Date(a.slotDate);//slot_details.date);
            const dateB = new Date(b.slotDate);
    
            if (dateA < dateB) {
              return -1;
            }
            else return 1;
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
          const patientId = item?.patient_id;
          const patientUid = item?.patient_details?.patient_uid;
          const patientGender = item?.patient_details?.gender
            .toLowerCase()
            ?.includes("m")
            ? "M"
            : "F";
          const mobileNumber = item?.patient_details?.mobile_number;
          const slotDate = item?.followup_date ? convertDateFormat(item?.followup_date, "dd/MM/yyyy") : "";
          // const slotTime = item?.slot_time ? convertTimeSlot(item?.slot_time) : "";
          // const status = item?.consultation_status;
          let action = "Start Visit";
          const updatedDate = item?.updated_at ? convertDateFormat(item?.updated_at, "dd/MM/yyyy") : "";
          const createdDate = item?.created_at ? convertDateFormat(item?.created_at, "dd/MM/yyyy") : "";
          return {
            patientDetails: `${item?.patient_details?.name} | ${patientGender}`,
            p_name: `${item?.patient_details?.name}`,
            patientId: patientId,
            patientUid: patientUid,
            mobileNumber: mobileNumber,
            doc_name: item?.doc_details?.doc_name,
            slotDate: slotDate,
            action: action,
            updatedDate: updatedDate,
            createdDate: createdDate,
            type: 'Follow Up',
            ...item,
          };
        });

        // const finalData = formattedAppointmentList.concat(formattedFollowUpList);
    

        if(formattedFollowUpList){
          const sortedFollowUpData = formattedFollowUpList.sort((a, b) => {
            const dateA = new Date(a.slotDate);//slot_details.date);
            const dateB = new Date(b.slotDate);
    
            if (dateA < dateB) {
              return -1;
            }
            else return 1;
          });
          setFollowUpData(sortedFollowUpData);
        } 
      });
    }
  }
  const handleDateChange = (event) => {
    setFilterDateValue(event.target.value);
    fetchList(event.target.value);
  };

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
          showFilter = "true"
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