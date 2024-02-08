import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { apis } from "../../../utils/apis";
import { apiRequest } from "../../../utils/request";
import axios from "axios";
import { BASE_URL, pdfUploadHeader } from "../../../utils/request";

export const searchVitalsDetails = createAsyncThunk(
  "searchVitals/EMR",
  async (params) => {
    const response = await axios.get(apis?.searchVitals, { params });
    return response;
  }
);
export const getEMRId = createAsyncThunk("getPMRId/PMRId", async (payload) => {
  const response = await apiRequest("POST", apis?.createEMR, payload);
  return response;
});

export const getPatientAuth = createAsyncThunk(
  "fetchModes/patient",
  async (payload) => {
    const response = await apiRequest("POST", apis?.authInit, payload);
    return response;
  }
);

export const verifyPatientOTP = createAsyncThunk(
  "patient/verifySyncOtp",
  async (payload) => {
    const response = await apiRequest("POST", apis?.verifySyncOtp, payload);
    return response;
  }
);

export const getPatientDetails = createAsyncThunk(
  "patient/getPatientDetails",
  async (id) => {
    const response = await apiRequest(
      "GET",
      apis?.patientDetails + "/" + id,
      null
    );
    return response;
  }
);

export const sendNotification = createAsyncThunk("notifyPMR", async (payload) => {
  const response = await apiRequest("POST", apis?.pmrSendNotification, payload);
  return response;
});

export const syncPMR = createAsyncThunk(
  "patient/verifySyncOtp",
  async (payload) => {
    const response = await apiRequest(
      "POST",
      `${apis?.syncPMREndpoint}/${payload.pmr_id}?hip_id=${payload.hip_id}`,
      payload
    );
    return response;
  }
);
export const postEMR = createAsyncThunk("submitPMR/PMR", async (payload) => {
  const response = await apiRequest("POST", apis?.submitEMR, payload);
  return response;
});

export const uploadPmrPdf = createAsyncThunk(
  "uploadPMR/PMR",
  async (pdfBlob, pmr_id, document_type) => {
    const access_token = sessionStorage.getItem("accesstoken");
    const formData = new FormData();
    formData.append("file", pdfBlob);
    try {
      const response = await axios.post(apis.uploadPmrPdf, formData, {
        headers: {
          Authorization: `Bearer ${access_token}`,
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
          "Access-Control-Allow-Headers":
            "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
          "Content-Type": "multipart/form-data",
        },
      });
      return response;
    } catch (error) {
      console.error("Error uploading PDF:", error);
    }
  }
);

// export const uploadHealthDocument = createAsyncThunk(
//   "uploadHealthDocuments",
//   async ({params, docPayload}) => {
//     console.log(docPayload);
//     const response = await apiRequest("POST", `${apis?.uploadHealthDocument}?patient_id=${params.patient_id}&appointment_id=${params.appointment_id}&hip_id=${params.hip_id}`,
//     docPayload);
//     return response;
//   }
// );

export const submitHealthDocument = createAsyncThunk(
  "PMR/uploadDocument",
  async ({params, docPayload}) => {
    const apiUrl = apis.uploadPmrPdf;
    const access_token = sessionStorage.getItem("accesstoken");
    const formData = new FormData();
    const files = docPayload.files;
    files.map((file) => {
      formData.append("files", file);
    })
    try {
      const response = await axios.post(BASE_URL + "/" + apiUrl, formData, {
        params: {
          mode: params?.mode,
          pmr_id: params?.pmr_id,
        },
        headers: {
          Authorization: `Bearer ${access_token}`,
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
          "Access-Control-Allow-Headers":
            "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
          "Content-Type": "multipart/form-data",
        },
      });
      return response;
    } catch (error) {
      console.error("Error uploading PDF:", error);
    }
    // const response = await apiRequest("POST", `${apis?.uploadPmrPdf}?pmr_id=${params.pmr_id}&document_type=${params.document_type}`,
    // formData);
    // return response;
  }
);

const EMRSlice = createSlice({
  name: "SearchVitals",
  initialState: {
    loading: false,
    searchedData: [],
    pmrIdData: {},
    pmr: {},
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
      })
      .addCase(getEMRId.pending, (state) => {
        state.loading = true;
      })
      .addCase(getEMRId.fulfilled, (state, action) => {
        state.loading = false;
        state.pmrIdData = action.payload;
      })
      .addCase(getEMRId.rejected, (state, action) => {
        state.loading = false;
      })
      .addCase(postEMR.pending, (state) => {
        state.loading = true;
      })
      .addCase(postEMR.fulfilled, (state, action) => {
        state.loading = false;
        state.pmr = action.payload;
      })
      .addCase(postEMR.rejected, (state, action) => {
        state.loading = false;
      });
  },
});

export default EMRSlice.reducer;
