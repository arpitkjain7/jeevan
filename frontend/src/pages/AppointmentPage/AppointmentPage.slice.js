import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { apiRequest } from "../../utils/request";
import { apis } from "../../utils/apis";

// Define the async thunk for fetching data
export const fetchAppointmentList = createAsyncThunk(
  "list/fetchAppointmentList",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      apis?.listAppointments,
      null,
      payload
    );
    return response;
  }
);

export const fetchAppointmentAnalystics = createAsyncThunk(
  "list/fetchAppointmentAnalytics",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      apis?.appointmentAnalytics,
      null,
      payload
    );
    return response;
  }
);

export const listAppointmentByDate = createAsyncThunk(
  "listAppointmentByDate",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      `${apis?.listAppointmentByDate}?hip_id=${payload.hipId}&appointment_date=${payload.appointmentDate}`
    );
    return response;
  }
);

export const fetchPatientDetails = createAsyncThunk(
  "fetchPatientDetails",
  async (id) => {
    const response = await apiRequest(
      "GET",
      apis?.fetchPatientDetails + "/" + id,
      null
    );
    return response;
  }
);

// Create the slice
const AppointmentSlice = createSlice({
  name: "list",
  initialState: {
    patientDetails: {},
    patientList: [],
    patientAnalytics: {},
    loading: false,
    error: null,
  },
  reducers: {
    setSelectedPatientData: (state, action) => {
      state.patientDetails = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAppointmentList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAppointmentList.fulfilled, (state, action) => {
        state.loading = false;
        state.patientList = action.payload;
      })
      .addCase(fetchAppointmentList.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(fetchAppointmentAnalystics.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAppointmentAnalystics.fulfilled, (state, action) => {
        state.loading = false;
        state.patientAnalytics = action.payload;
      })
      .addCase(fetchAppointmentAnalystics.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export const AppointmentPageActions = AppointmentSlice.actions;
export default AppointmentSlice.reducer;
