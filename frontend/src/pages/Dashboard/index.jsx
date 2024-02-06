import React, { useEffect, useState } from 'react'
import Sidebar from '../../components/Sidebar'
import {
  Grid,
  Typography,
  styled,
  Card,
  CardActions,
  CardContent,
  Button,
  Paper,
} from "@mui/material";
import { Box } from '@mui/system';
import { BarChart } from '@mui/x-charts/BarChart';
import { useDispatch } from 'react-redux';
import { fetchAppointmentList } from '../AppointmentPage/AppointmentPage.slice';

const DashboardWrapper = styled("div")(({ theme }) => ({
  "&": {
    padding: "25px 10px 10px",
    [theme.breakpoints.down('sm')]: {
      padding: "10px"
    }
  }, 
  ".patientList-title-wrapper": {
    marginBottom: "20px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    [theme.breakpoints.down('md')]: {
      display: "block",
    },
  },
  ".patientList-heading": {
    "&.MuiTypography-root": theme.typography.h1,
    [theme.breakpoints.down('sm')]: {
      fontSize: "30px"
    },
  },
  ".patientList-desc": theme.typography.h2,
  ".chart-wrapper": {
    backgroundColor: "#fff"
  },
}));

const bull = (
  <Box
    component="span"
    sx={{ display: 'inline-block', mx: '2px', transform: 'scale(0.8)' }}
  >
    •
  </Box>
);

const chartSetting = {
  xAxis: [
    {
      label: 'rainfall (mm)',
    },
  ],
  // width: 500,
  // height: 400,
};

const dataset = [
  {
    london: 59,
    paris: 57,
    newYork: 86,
    seoul: 21,
    month: 'Jan',
  },
  {
    london: 50,
    paris: 52,
    newYork: 78,
    seoul: 28,
    month: 'Fev',
  },
  {
    london: 47,
    paris: 53,
    newYork: 106,
    seoul: 41,
    month: 'Mar',
  },
  {
    london: 54,
    paris: 56,
    newYork: 92,
    seoul: 73,
    month: 'Apr',
  },
  {
    london: 57,
    paris: 69,
    newYork: 92,
    seoul: 99,
    month: 'May',
  },
  {
    london: 60,
    paris: 63,
    newYork: 103,
    seoul: 144,
    month: 'June',
  },
  {
    london: 59,
    paris: 60,
    newYork: 105,
    seoul: 319,
    month: 'July',
  },
  {
    london: 65,
    paris: 60,
    newYork: 106,
    seoul: 249,
    month: 'Aug',
  },
  {
    london: 51,
    paris: 51,
    newYork: 95,
    seoul: 131,
    month: 'Sept',
  },
  {
    london: 60,
    paris: 65,
    newYork: 97,
    seoul: 55,
    month: 'Oct',
  },
  {
    london: 67,
    paris: 64,
    newYork: 76,
    seoul: 48,
    month: 'Nov',
  },
  {
    london: 61,
    paris: 70,
    newYork: 103,
    seoul: 25,
    month: 'Dec',
  },
];

const valueFormatter = (value) => `${value}mm`;

function Dashboard() {
  const hospital = sessionStorage?.getItem("selectedHospital");
  const currentPatient = JSON.parse(sessionStorage.getItem("selectedPatient"));
  const username = sessionStorage.getItem("userName");
  const dispatch = useDispatch();
  const [appointmentList, setAppointmentList] = useState({});
  const [completedAppointment, setCompletedAppointment] = useState(0);
  const [pendingAppointment, setPendingAppointment] = useState(0);
  const [followupCases, setFollowupCases] = useState(0);
  const [newCases, setNewCases] = useState(0);

  useEffect(() => {
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = {
        hip_id: currentHospital?.hip_id,
      };
      // const dates = [];
      // const currentDate = new Date();

      // for (let i = 0; i < 7; i++) {
      //   const date = currentDate.toLocaleDateString(undefined, {
      //     weekday: "long",
      //     year: "numeric",
      //     month: "numeric",
      //     day: "numeric",
      //   });

      //   dates.push(date);
      //   currentDate.setDate(currentDate.getDate() + 1);
      // }
      // console.log(dates);
      // const displayArr = date?.split(" ");
      // const formatedDate = parseDateFormat(displayArr[1], "yyyy-MM-dd");
      dispatch(fetchAppointmentList(payload)).then((res) => {
        const mainList = res.payload;
        console.log(mainList);
        setAppointmentList(mainList);
        mainList.map((list) => {
          if(list?.appointment_type === "first visit"){
            setNewCases(prevCount => prevCount + 1);
          }
          else if(list?.appointment_type === "follow-up visit"){
            setFollowupCases(prevCount => prevCount + 1);
          }
          if(list?.consultation_status === "Completed"){
            setCompletedAppointment(prevCount => prevCount + 1);
          }
          else if(list?.consultation_status === "InProgress"){
            setPendingAppointment(prevCount => prevCount + 1)
          }
        })
      })
    }
  }, [])

  return (
    <DashboardWrapper>
       <div className="patientList-title-wrapper">
        <div>
          <Typography className="patientList-heading">Hello, {username}</Typography>
          <Typography className="patientList-desc">
            OneLiner
          </Typography>
        </div>
      </div>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={4}>
          <Card style={{ height: "190px"}}>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total number of appointments
              </Typography>
              <Typography variant="h5" component="div">
                <br />
              </Typography>
              <Typography variant="body2">
                <br/>
              </Typography>
              <Typography variant="h1">
                {appointmentList.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card style={{ height: "190px"}}>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Completed appointments
              </Typography>
              <Typography variant="h5" component="div">
                {completedAppointment}
              </Typography>
                <br />
              <Typography sx={{ mb: 1.5 }} color="text.secondary">
                Pending appointments
              </Typography>
              <Typography variant="h5">
                {pendingAppointment}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card style={{ height: "190px"}}>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Follow up cases
              </Typography>
              <Typography variant="h5" component="div">
                {followupCases}
              </Typography>
              <br />
              <Typography sx={{ mt: 1.5}} color="text.secondary">
                New cases
              </Typography>
              <Typography variant="h5">
                {newCases}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
     
      <br/>
      <Paper sx={{ width: '100%', height: 400 }} elevation={3}>
        <BarChart       
          dataset={dataset}
          yAxis={[{ scaleType: 'band', dataKey: 'month' }]}
          series={[{ dataKey: 'seoul', label: 'Weekly Patient Visits Overview', valueFormatter }]}
          layout="horizontal"
          {...chartSetting}
          // width='100%'
        />
      </Paper>
    </DashboardWrapper>
  )
}

export default Dashboard