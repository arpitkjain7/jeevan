import { format } from "date-fns";

export const convertDateFormat = (dateString, formatNeeded) => {
  const formattedDate = format(new Date(dateString), formatNeeded);
  return formattedDate;
};

export const convertToNumber = (value) => {
  const parsedValue = parseFloat(value);
  return isNaN(parsedValue) ? value : parsedValue;
};

export const getDayFromString = (value) => {
  const date = new Date(value);
  const day = date.toLocaleDateString("en-US", { weekday: "long" });
  return day;
};
