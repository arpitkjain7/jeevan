export const apis = {
  login: "v1/user/signIn",
  list: "v1/HIP/listAll",
  listHospitalByUser: "v1/HIP/listForUser",
  listPtaient: "v1/patient/listAll",
  registerAadhaar: "v1/HID/registration/aadhaar/generateOTP",
  verifyOTPAadhaar: "v1/HID/registration/aadhaar/verifyOTP",
  restigerNumber: "v1/registration/mobile/generateOtp",
  registerAadhaarNumber: "v1/HID/registration/aadhaar/generateMobileOTP",
  verifyOTPNumber: "v1/registration/mobile/verifyOtp",
  verifyAadhaarotp: "v1/HID/registration/aadhaar/verifyMobileOTP",
  registerUser: "v3/patient/register",
  registerAadhaarPaient: "v1/HID/registration/aadhaar/abhaRegistration",
  registerPhonePatient: "v1/registration/mobile/createHealthId",
  downloadAbhaCard: "v1/profile/getAbhaCard",
  displayAbhaCard: "v1/profile/getAbhaCardBytes",
  getAbhaCard: "v3/HID/retrieveAbha/getAbhaCard",
  listAllDoctors: "v1/listAllDoctors",
  doctorSlotsDetails: "v1/slots",
  createAppointment: "v1/appointment/create",
  listAppointments: "v1/appointment/listAll",
  searchVitals: "https://snomed.cliniq360.com/csnoserv/api/search/search",
  createEMR: "v2/PMR/createPMR",
  submitEMR: "v1/PMR/submitPMR",
  uploadPmrPdf: "v1/PMR/uploadPrescription",
  getVitalDetail: "v1/patient/getVitals",
  listConsent: "v1/HIU/listConsent",
  consentDetails: "v1/HIU/getCareContext",
  getPmrList: "v1/PMR/list",
  getPmrDocs: "v1/PMR/listDocuments",
  getDoc: "v1/PMR/getDocument",
  getDocBytes: "v1/PMR/getDocumentBytes",
  submitConsentReq: "v1/HIU/consentInit",
  fetchModes: "v1/patient/fetchModes",
  authInit: "v2/patient/auth/init",
  verifySyncOtp: "v1/patient/auth/verifyOtp",
  syncPMREndpoint: "v1/PMR/sync",
  patientDetails: "v1/patient",
  uploadHealthDocument: "v1/PMR/uploadHealthDocuments",
  pmrSendNotification: "v1/PMR/sendDocument",
  resetUserPassword: "v1/user/resetPassword",
  genearteOTPPassword: "v1/user/generateOTP",
  generateOTPAbha: "v3/HID/retrieveAbha/generateOTP",
  verifyOTPAbha: "v3/HID/retrieveAbha/verifyOTP",
  abhaRegistrationViaAadhaar: "v3/HID/registration/aadhaar/generateOTP",
  verifyAadhaarAbha: "v3/HID/registration/aadhaar/verifyOTP",
  suggestAbhaAddress: "v3/HID/registration/aadhaar/suggestAbha",
  createAbhaAddress: "v3/HID/registration/aadhaar/createAbhaAddress",
  registerAbhaPatient: "v3/patient/register",
  verifyAbhaUser: "v3/HID/retrieveAbha/verifyUser",
  getAbhaProfile: "v3/HID/retrieveAbha/getProfile",
  patientFetchModes: "v1/patient/fetchModes",
  patientAuthInit: "v3/patient/auth/init",
  patientAuthResendOtp: "v3/patient/auth/resendOtp",
  patientAuthVerifyOTP: "v3/patient/auth/verifyOtp",
  gatewayInteraction: "v1/gatewayInteraction",
  verifyAbhaPatient: "v1.0/patients/verify",
  verifyDemographics: "v1/patient/auth/verifyDemographic",
  demographicsAuthInit: "v2/patient/auth/init",
  deepLink: "v1/deepLinkNotify",
  searchAbha: "v1/HID/searchAbha",
  googleReview: "v1/PMR/sendGoogleReviewLink",
  listAppointmentByDate: "v1/appointment/listByDate",
  fetchPatientDetails: "v1/patient"
};
