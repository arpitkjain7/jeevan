import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import { apiRequest } from "../../utils/request";
import { apis } from "../../utils/apis";

export const fetchVistList = createAsyncThunk("list/pmr", async (payload) => {
  const response = await apiRequest(
    "GET",
    apis?.getPmrList + "/" + payload,
    null,
    null
  );
  return response;
});

export const fetchPMRList = createAsyncThunk(
  "list/pmr-docs",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      apis?.getPmrDocs + "/" + payload,
      null,
      null
    );
    return response;
  }
);

export const getDocument = createAsyncThunk(
  "list/document",
  async (payload) => {
    const response = await apiRequest(
      "GET",
      apis?.getDoc + "/" + payload,
      null,
      null
    );
    return response;
  }
);

const PastVisitSlice = createSlice({
  name: "list-PMR",
  initialState: {
    pmrData: [],
    docData: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchVistList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchVistList.fulfilled, (state, action) => {
        state.loading = false;
        state.pmrData = action.payload;
      })
      .addCase(fetchVistList.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(fetchPMRList.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPMRList.fulfilled, (state, action) => {
        state.loading = false;
        state.docData = action.payload;
      })
      .addCase(fetchPMRList.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

// Export the async thunk and reducer
export const { reducer } = PastVisitSlice;
export default PastVisitSlice;
