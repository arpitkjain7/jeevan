// PatientRegistartionSlice.js

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { apiRequest } from "../../utils/request";
import { apis } from "../../utils/apis";

export const registerAADHAAR = createAsyncThunk(
  "registration/aadhaarregisterAADHAAR",
  async (userData) => {
    const response = await apiRequest("POST", apis?.registerAadhaar, userData);
    return response;
  }
);

export const registerPhone = createAsyncThunk(
  "registration/aadhaarregisterPhone",
  async ({ payload, url }) => {
    const response = await apiRequest("POST", url, payload);
    return response;
  }
);

export const verifyAadhaarOTP = createAsyncThunk(
  "registration/verifyAADHAAR",
  async (OTP) => {
    const response = await apiRequest("POST", apis?.verifyOTPAadhaar, OTP);
    return response;
  }
);
export const verifyPhoneOTP = createAsyncThunk(
  "registration/verifyPhone",
  async (OTP) => {
    const response = await apiRequest("POST", apis?.verifyOTPNumber, OTP);
    return response;
  }
);

export const verifyAadhaarPhoneOTP = createAsyncThunk(
  "registration/verifyAbha",
  async (OTP) => {
    const response = await apiRequest("POST", apis?.verifyAbha, OTP);
    return response;
  }
);

export const verifyAbhaNumber = createAsyncThunk(
  "registration/verifyAbha",
  async ({url, payload}) => {
    const response = await apiRequest("POST", url, payload);
    return response;
  }
);

export const verifyAbhaOTP = createAsyncThunk(
  "registration/verifyAbhaOTP",
  async (OTP) => {
    const response = await apiRequest("POST", apis?.verifyOTPAbha, OTP);
    return response;
  }
);

export const registerPatient = createAsyncThunk(
  "registration/registerPatient",
  async ({ payload, url }) => {
    const response = await apiRequest("POST", url, payload);
    return response;
  }
);

export const registerAbhaPatient = createAsyncThunk(
  "registration/registerPatient",
  async (payload) => {
    const response = await apiRequest("POST", apis?.registerAbhaPatient, payload);
    return response;
  }
);

export const registerAadhaarAbha = createAsyncThunk(
  "registration/registerAbhaPatient",
  async (payload) => {
    const response = await apiRequest("POST", apis?.abhaRegistrationViaAadhaar, payload);
    return response;
  }
);

export const verifyAadhaarAbhaOTP = createAsyncThunk(
  "registration/verifyAadhaarAbhaOTP",
  async (payload) => {
    const response = await apiRequest("POST", apis?.verifyAadhaarAbha, payload);
    return response;
  }
);

export const suggestAbhaAddress = createAsyncThunk(
  "registration/suggestAbhaAddress",
  async (transactionId) => {
    const response = await apiRequest("GET", apis?.suggestAbhaAddress+ '?' + `transaction_id=${transactionId}`);
    return response;
  }
);

export const createAbhaAddress = createAsyncThunk(
  "registration/createAbhaAddress",
  async (payload) => {
    const response = await apiRequest("POST", apis?.createAbhaAddress, payload);
    return response;
  }
);

export const verifyAbhaUser = createAsyncThunk(
  "registration/verifyAbhaUser",
  async (payload) => {
    const response = await apiRequest("POST", apis?.verifyAbhaUser, payload);
    return response;
  }
);

export const getAbhaProfile = createAsyncThunk(
  "registration/getAbhaProfile",
  async (parameters) => {
    const response = await apiRequest("POST", apis?.getAbhaProfile + `?txnId=${parameters.transactionId}&createRecord=false&hip_id=${parameters.hipId}`);
    return response;
  }
);

export const downloadAbha = createAsyncThunk(
  "registration/downloadAbha",
  async (patient_Id) => {
    const response = await apiRequest("POST", apis?.downloadAbhaCard, patient_Id);
    return response;
  }
);

export const displayAbha = createAsyncThunk(
  "registration/displayAbha",
  async (patient_Id) => {
    const response = await apiRequest("POST", apis?.displayAbhaCard, patient_Id);
    return response;
  }
);

export const patientFetchModes = createAsyncThunk(
  "registration/patientFetchModes",
  async (payload) => {
    const response = await apiRequest("POST", apis?.patientFetchModes, payload);
    return response;
  }
);

export const patientAuthInit = createAsyncThunk(
  "registration/patientAuthInit",
  async (payload) => {
    const response = await apiRequest("POST", apis?.patientAuthInit, payload);
    return response;
  }
);

export const patientAuthVerifyOTP = createAsyncThunk(
  "registration/patientAuthVerifyOTP",
  async (payload) => {
    const response = await apiRequest("POST", apis?.patientAuthVerifyOTP, payload);
    return response;
  }
);

export const gatewayInteraction = createAsyncThunk(
  "registration/gatewayInteraction",
  async (requestId) => {
    const response = await apiRequest("GET", apis?.gatewayInteraction + `/${requestId}`);
    return response;
  }
);

const PatientRegistartionSlice = createSlice({
  name: "registration",
  initialState: {
    loading: false,
    error: null,
    registerAadhaar: {},
    registerPhone: {},
    registeredPatientDetails: {},
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(registerAADHAAR.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(registerAADHAAR.fulfilled, (state, action) => {
        state.loading = false;
        state.registerAadhaar = action.payload;
      })
      .addCase(registerAADHAAR.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(registerPhone.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(registerPhone.fulfilled, (state, action) => {
        state.loading = false;
        state.registerPhone = action.payload;
      })
      .addCase(registerPhone.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(verifyAadhaarOTP.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(verifyAadhaarOTP.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(verifyAadhaarOTP.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(verifyPhoneOTP.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(verifyPhoneOTP.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(verifyPhoneOTP.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(registerPatient.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(registerPatient.fulfilled, (state, action) => {
        state.loading = false;
        state.registeredPatientDetails = action.payload;
      })
      .addCase(registerPatient.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(verifyAadhaarPhoneOTP.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(verifyAadhaarPhoneOTP.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(verifyAadhaarPhoneOTP.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default PatientRegistartionSlice.reducer;
