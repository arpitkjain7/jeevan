import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { apis } from "../../utils/apis";
import { apiRequest } from "../../utils/request";

export const resetPassword = createAsyncThunk(
    "changePassword/resetPassword",
    async (payload) => {
        const response = await apiRequest("POST", apis?.resetUserPassword, payload);
        return response;
      }
  );
  
  export const genearteOTPPassword = createAsyncThunk(
    "changePassword/resetPassword",
    async (payload) => {
        const response = await apiRequest("POST", apis?.genearteOTPPassword, payload);
        return response;
      }
  );

  const forgotPasswordSlice = createSlice({
    name: "changePassword",
    initialState: {
      userPassword: null,
      loading: false,
      error: null,
    },
    reducers: {
      resetPasswordState: (state, value) => {
        state.userPassword = null;
        state.loading = false;
        state.error = null;
      },
    },
    extraReducers: (builder) => {
      builder
        .addCase(resetPassword.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(resetPassword.fulfilled, (state, action) => {
          state.userPassword = action.payload;
          state.loading = false;
          state.UserData = action.payload;
        })
        .addCase(resetPassword.rejected, (state, action) => {
          state.loading = false;
          state.error = action.error.message;
        });
    },
  });

export const { resetPasswordState } = forgotPasswordSlice.actions;
export default forgotPasswordSlice.reducer;