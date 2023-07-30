import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { apis } from "../../../utils/apis";
import { apiRequest } from "../../../utils/request";
import axios from "axios";


export const searchVitalsDetails = createAsyncThunk(
  "searchVitals/EMR",
  async (params) => {
    const response = await axios.get(apis?.searchVitals, {params});
    return response;
  }
);

const EMRSlice = createSlice({
  name: "SearchVitals",
  initialState: {
    loading: false,
    searchedData: [],
  },
  reducers: {
    resetSearchData: (state, value) => {
      state.searchedData = value;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(searchVitalsDetails.pending, (state) => {
        state.loading = true;
      })
      .addCase(searchVitalsDetails.fulfilled, (state, action) => {
        state.loading = false;
        state.searchedData = action.payload;
      })
      .addCase(searchVitalsDetails.rejected, (state, action) => {
        state.loading = false;
      });
  },
});

export default EMRSlice.reducer;
