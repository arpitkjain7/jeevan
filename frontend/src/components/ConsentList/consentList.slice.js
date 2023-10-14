// ConsentListSlice.js

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { apiRequest } from "../../utils/request";
import { apis } from "../../utils/apis";

// Define the async thunk for fetching data
export const fetchConsentList = createAsyncThunk(
  "list/fetchConsentList",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      apis?.listConsent + "/" + payload,
      null,
      null
    );
    return response;
  }
);

// Create the slice
const ConsentListSlice = createSlice({
  name: "list",
  initialState: {
    consentList: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchConsentList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchConsentList.fulfilled, (state, action) => {
        state.loading = false;
        state.consentList = action.payload;
      })
      .addCase(fetchConsentList.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

// Export the async thunk and reducer
export const { reducer } = ConsentListSlice;
export default ConsentListSlice;
