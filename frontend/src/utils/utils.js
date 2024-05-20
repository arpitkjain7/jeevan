import { format, isValid, parse } from "date-fns";
import { enGB } from 'date-fns/locale';

export const convertDateFormat = (dateString, formatNeeded) => {
  const formattedDate = format(new Date(dateString), formatNeeded);
  return formattedDate;
};

export const parseDateFormat = (dateString, formatNeeded) => {
  if(isValid(new Date(dateString))){
    const formattedDate = format(new Date(dateString), formatNeeded);
    return formattedDate;
  } else {
    const parsedDate = parse(dateString, 'P', new Date(), { locale: enGB });
    const formattedDate = format(parsedDate, formatNeeded);
    return formattedDate;
  }
};

export const customformatDate = (dateString, formatNeeded) => {
  const parsedDate = parse(dateString, "EEEE, dd/MM/yyyy", new Date());
  const formattedDate = format(parsedDate, formatNeeded);
  return formattedDate;
};

//
export const convertToNumber = (value) => {
  const parsedValue = parseFloat(value);
  return isNaN(parsedValue) ? value : parsedValue;
};

export const getDayFromString = (value) => {
  const date = new Date(value);
  const day = date.toLocaleDateString("en-US", { weekday: "long" });
  return day;
};

export const convertTimeSlot = (timeSlot24hr) => {
  if(timeSlot24hr.length){
    let timeParts = timeSlot24hr.split("-");
    let startTime = timeParts[0].trim();
    let endTime = timeParts[1].trim();
    let startTimeParts = startTime.split(":");
    let startHours = parseInt(startTimeParts[0]);
    let startMinutes = parseInt(startTimeParts[1]);

    let endTimeParts = endTime.split(":");
    let endHours = parseInt(endTimeParts[0]);
    let endMinutes = parseInt(endTimeParts[1]);

    let startMeridiem = startHours < 12 ? "AM" : "PM";
    let endMeridiem = endHours < 12 ? "AM" : "PM";

    if (startHours === 0) {
      startHours = 12;
    } else if (startHours > 12) {
      startHours -= 12;
    }

    if (endHours === 0) {
      endHours = 12;
    } else if (endHours > 12) {
      endHours -= 12;
    }

    let convertedTimeSlot =
      startHours +
      ":" +
      (startMinutes < 10 ? "0" + startMinutes : startMinutes) +
      startMeridiem +
      " - " +
      endHours +
      ":" +
      (endMinutes < 10 ? "0" + endMinutes : endMinutes) +
      endMeridiem;

    return convertedTimeSlot;
  }
};

export const validateAbhaAddress = (address) => {
  const regex = /^[A-Za-z0-9]+([_.][A-Za-z0-9]+)*$/;
  // console.log(address);
  return (
    // /^[\w!@#$%^&*-_./?]{8,18}$/.test(address)
    /^[a-zA-Z0-9](?=.*[a-zA-Z0-9!@#$%^&*._])([a-zA-Z0-9!@#$%^&*._]{6,18}[a-zA-Z0-9])$/.test(address)
    // address.length >= 8 &&
    // address.length <= 18 &&
    // regex.test(address) &&
    // !/^[._]|[._]$/.test(address)
  );
};

export const calculateBMI = (bodyHeight, bodyWeight) => {
  // Check if bodyHeight and bodyWeight are numbers
  const height = Number(bodyHeight);
  const weight = Number(bodyWeight);
  if (
    typeof height !== "number" ||
    isNaN(height) ||
    typeof weight !== "number" ||
    isNaN(weight)
  ) {
    console.error(
      "Invalid input. Please enter valid numbers for body height and weight."
    );
    return null;
  }

  const bodyHeightM = height / 100;
  const bmi = weight / Math.pow(bodyHeightM, 2);
  return bmi;
};
