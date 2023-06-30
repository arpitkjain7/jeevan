import React, { useEffect, useState } from "react";
import { Typography, styled } from "@mui/material";
import ArrowNext from "../../assets/arrows/arrow-right.svg";
import { useDispatch, useSelector } from "react-redux";
import { fetchHospital } from "./hospitalList.slice";
import { useNavigate } from "react-router-dom";

const HospitalListWrapper = styled("div")(({ theme }) => ({
  "&": {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  ".hospitalList-title": {
    "&.MuiTypography-root": {
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "32px",
      lineHeight: "150%",
      marginBottom: "4px",
    },
  },
  ".hospitalList-content": {
    textAlign: "center",
  },
  ".hospitalList-subTitle": {
    "&.MuiTypography-root": {
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      lineHeight: "16px",
      marginBottom: "54px",
    },
  },
  ".hospitalList-container": {
    alignItems: "center",
    justifyContent: "center",
    width: "500px",
    margin: "0 auto",
    marginTop: "10%",
  },
  ".hospitalList-name-wrapper": {
    border: `1px solid ${theme.tertiaryGrey}`,
    borderRadius: "3px",
    backgroundColor: theme.primaryWhite,
    padding: "16px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    width: "100%",
    cursor: "pointer",
  },

  ".hospitalList-name": {
    "&.MuiTypography-root": {
      fontFamily: "Inter",
      fontWeight: "500",
      fontSize: "16px",
      lineHeight: "16px",
    },
  },
}));

const temp = [{ hospitalName: "AIMS Bengaluru" }];

const HospitalList = () => {
  const dispatch = useDispatch();
  const dataState = useSelector((state) => state.list);
  const navigate = useNavigate();
  const [hospitalList, setHospitalList] = useState([]);
  // const hospitalList = dataState.

  useEffect(() => {
    dispatch(fetchHospital()).then((response) => {
      const resData = response.payload;
      if (resData?.length) {
        setHospitalList(resData);
        console.log(response.payload);
      }
    });
  }, []);

  const redirectToDashboard = (hospitalData) => {
    localStorage.setItem("selectedHospital",JSON.stringify(hospitalData));
    navigate("/dashboard");
  };

  return (
    <HospitalListWrapper>
      <div className="hospitalList-container">
        <div className="hospitalList-content">
          <Typography className="hospitalList-title">
            Choose your hospital
          </Typography>
          <Typography className="hospitalList-subTitle">
            Select your hospital from the below list
          </Typography>
        </div>

        {hospitalList?.map((item) => (
          <div
            className="hospitalList-name-wrapper"
            onClick={() => redirectToDashboard(item)}
          >
            <Typography className="hospitalList-name">{item?.name}</Typography>
            <img src={ArrowNext} alt="Select hospital" />
          </div>
        ))}
      </div>
    </HospitalListWrapper>
  );
};

export default HospitalList;
