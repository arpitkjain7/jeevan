// VitalsDetailSlice.js

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { apiRequest } from "../../utils/request";
import { apis } from "../../utils/apis";

// Define the async thunk for fetching data
export const fetchVitalDetails = createAsyncThunk(
  "list/vitalsById",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      apis?.getVitalDetail,
      null,
      payload
    );
    return response;
  }
);

// Create the slice
const VitalsDetailSlice = createSlice({
  name: "list-vital",
  initialState: {
    vitalData: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchVitalDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchVitalDetails.fulfilled, (state, action) => {
        state.loading = false;
        state.vitalData = action.payload;
      })
      .addCase(fetchVitalDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

// Export the async thunk and reducer
export const { reducer } = VitalsDetailSlice;
export default VitalsDetailSlice;
