import axios from "axios";

const BASE_URL = "https://engine.cliniq360.com/v1";

const defaultHeader = () => {
  const access_token = localStorage.getItem("accesstoken");
  return {
    Authorization: `Bearer ${access_token}`,
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "DELETE, POST, GET, OPTIONS",
    "Access-Control-Allow-Headers":
      "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
    Accept: "application/json",
  };
};

// Common utility function for making API requests
export const apiRequest = async (
  method,
  endpoint,
  data = null,
  params,
  headers = {}
) => {
  try {
    const url = `${BASE_URL}/${endpoint}`;

    const config = {
      method,
      url,
      params,
      data,
      headers: Object.keys(headers)?.length ? headers : defaultHeader(),
    };

    const response = await axios(config);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || error.message);
  }
};

export const get = async (url) => {
  return apiRequest("GET", url);
};

export const post = async (url, data) => {
  return apiRequest("POST", url, data);
};
