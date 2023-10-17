export const apis = {
  login: "user/signIn",
  list: "HIP/listAll",
  listPtaient: "patient/listAll",
  registerAadhar: "HID/registration/aadhaar/generateOTP",
  verifyOTPAadhar: "HID/registration/aadhaar/verifyOTP",
  restigerNumber: "registration/mobile/generateOtp",
  registerAadharNumber: "HID/registration/aadhaar/generateMobileOTP",
  verifyOTPNumber: "registration/mobile/verifyOtp",
  verifyAadharotp: "HID/registration/aadhaar/verifyMobileOTP",
  registerUser: "patient/register",
  registerAadharPaient: "HID/registration/aadhaar/abhaRegistration",
  registerPhonePatient: "registration/mobile/createHealthId",
  listAllDoctors: "listAllDoctors",
  doctorSlotsDetails: "slots",
  createAppointment: "appointment/create",
  listAppointments: "appointment/listAll",
  searchVitals: "https://snomed.cliniq360.com/csnoserv/api/search/search",
  createEMR: "PMR/createPMR",
  submitEMR: "PMR/submitPMR",
  uploadPmrPdf: "PMR/uploadDocument",
  getVitalDetail: "patient/getVitals",
  listConsent: "HIU/listConsent",
  consentDetails: "HIU/getConsentDetails",
  getPmrList: "PMR/list",
  getPmrDocs: "PMR/listDocuments",
  getDoc: "PMR/getDocument",
  submitConsentReq: "HIU/consentInit",
};
