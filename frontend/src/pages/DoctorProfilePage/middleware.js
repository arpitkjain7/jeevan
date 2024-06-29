import axios from "axios";
import { BASE_URL } from "../../utils/request";
import { apis } from "../../utils/apis";

export const getDoctorProfile = async (params) => {
    const response = await axios.get(BASE_URL + "/" + apis?.getDoctorProfile + `/${params}`);
    return response;
}

export const bookAppointment = async (payload) => {
    const response = await axios.post(BASE_URL + "/" + apis?.bookAppointment, payload);
    return response;
}