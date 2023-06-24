import { combineReducers } from 'redux';
import authReducer from '../app/auth.slice';

const rootReducer = combineReducers({
  auth: authReducer,
});

export default rootReducer;