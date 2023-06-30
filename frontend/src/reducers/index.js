import { combineReducers } from "redux";
import authReducer from "../app/auth.slice";
import listReducer from "../pages/HospitalList/hospitalList.slice";
import patientListReducer from "../pages/PatientPage/patientpage.slice";
import PatientRegistrationReducer from "../pages/PatientRegistration/PatientRegistration.slice";

const rootReducer = combineReducers({
  auth: authReducer,
  hospitalList: listReducer,
  patientList: patientListReducer,
  PatientRegistartion: PatientRegistrationReducer,
});

export default rootReducer;
