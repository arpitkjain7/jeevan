// fhirDoc.slice.js

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { apiRequest } from "../../utils/request";
import { apis } from "../../utils/apis";

// Define the async thunk for fetching data
export const fetchFhirDocDetails = createAsyncThunk(
  "list/fetchFhirDocDetails",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      apis?.getConsentDetails + "/" + payload,
      null,
      null
    );
    return response;
  }
);

// Create the slice
const FhirDocSlice = createSlice({
  name: "list",
  initialState: {
    fhirDocDetails: {},
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchFhirDocDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchFhirDocDetails.fulfilled, (state, action) => {
        state.loading = false;
        state.error = null;
      })
      .addCase(fetchFhirDocDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

// Export the async thunk and reducer
export const { reducer } = FhirDocSlice;
export default FhirDocSlice;
