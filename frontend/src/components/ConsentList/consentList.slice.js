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

export const fetchConsentDetails = createAsyncThunk(
  "list/fetchConsentDetails",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      apis?.consentDetails + "/" + payload,
      null,
      null
    );
    return response;
  }
);

export const postConsentRequest = createAsyncThunk(
  "post/consentRequest",
  async (payload) => {
    const response = await apiRequest("POST", apis?.submitConsentReq, payload);
    return response;
  }
);

export const searchAbha = createAsyncThunk(
  "post/searchAbha",
  async (payload) => {
    const response = await apiRequest("POST", apis?.searchAbha, payload);
    return response;
  }
);

export const gatewayInteraction = createAsyncThunk(
  "registration/gatewayInteraction",
  async (requestId) => {
    const response = await apiRequest(
      "GET",
      apis?.gatewayInteraction + "/" + requestId
    );
    return response;
  }
);

// Create the slice
const ConsentListSlice = createSlice({
  name: "list",
  initialState: {
    consentList: [],
    consentDetails: {},
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
      })
      .addCase(fetchConsentDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchConsentDetails.fulfilled, (state, action) => {
        state.loading = false;
        state.consentDetails = action.payload;
      })
      .addCase(fetchConsentDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

// Export the async thunk and reducer
export const { reducer } = ConsentListSlice;
export default ConsentListSlice;
