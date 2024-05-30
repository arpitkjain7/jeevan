import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { apiRequest } from "../../utils/request";
import { apis } from "../../utils/apis";

export const getPatientDetails = createAsyncThunk(
  "get/patientDetails",
  async ({ payload }) => {
    const response = await apiRequest(
      "GET",
      apis?.patientDetails + `/${payload.patient_id}`,
      payload
    );
    return response;
  }
);
const PatientDetailsSlice = createSlice({
  name: "detail",
  initialState: {
    loading: false,
    error: null,
    patientDetail: {},
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(getPatientDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getPatientDetails.fulfilled, (state, action) => {
        state.loading = false;
        state.patientDetail = action.payload;
      })
      .addCase(getPatientDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default PatientDetailsSlice.reducer;
