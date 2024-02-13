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
import { convertDateFormat, parseDateFormat } from '../../utils/utils';

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
  ".chartStyling": {
    width: "100%", 
    height: "450px"
  },
  ".chartStyling .MuiChartsAxis-tickLabel": {
    fontSize: "16px !important"
  },
}));

const chartSetting = {
  yAxis: [{
    tickNumber: 0
 }],
  // xAxis: [
  //   {
  //   }
  // ],
};

function Dashboard() {
  const hospital = sessionStorage?.getItem("selectedHospital");
  const username = sessionStorage.getItem("userName");
  const dispatch = useDispatch();
  const [appointmentList, setAppointmentList] = useState({});
  const [completedAppointment, setCompletedAppointment] = useState(0);
  const [pendingAppointment, setPendingAppointment] = useState(0);
  const [followupCases, setFollowupCases] = useState(0);
  const [newCases, setNewCases] = useState(0);
  const [chartData, setChartData] = useState([]);
  const [isChart, setIsChart] = useState(false);
  const isMobile = window.innerWidth < 600;

  useEffect(() => {
    let currentHospital = {};
    if (hospital) {
      currentHospital = JSON.parse(hospital);
      const payload = {
        hip_id: currentHospital?.hip_id,
      };
      const dates = [];
      const currentDate = new Date();
      currentDate.setDate(currentDate.getDate() - 6);
      for (let i = 0; i < 7; i++) {
        const date = currentDate.toLocaleDateString(undefined, {
          year: "numeric",
          month: "numeric",
          day: "numeric",
        })
        const day = currentDate.toLocaleDateString(undefined, {
          weekday: "long",
        })
        const day_date = currentDate.toLocaleDateString(undefined, {
          weekday: "long",
          year: "numeric",
          month: "numeric",
          day: "numeric",
        })
        dates.push({ date: parseDateFormat(date, "yyyy-MM-dd"), day: day, count: 0, day_date: day_date });
        currentDate.setDate(currentDate.getDate() + 1);
      }
      dispatch(fetchAppointmentList(payload)).then((res) => {
        const mainList = res?.payload;
        setAppointmentList(mainList);
        let appointment_days = [];
        let finalArray;
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
          dates.map((date) => {
            if(date.date === list?.slot_details?.date){
              appointment_days.push({ date: date.date, day: date.day });
            }
          });
        });

        const countsByDays = { };
        appointment_days.forEach(({ day }) => {
          countsByDays[day] = (countsByDays[day] || 0) + 1;
        });
       
        finalArray = Object.entries(countsByDays)
          .map(([day, count]) => ({ day, count }))
       
        const chart_data = dates.map((item) => {
          const matchedObject = finalArray.find((obj) => obj.day === item.day);
          return { ...item, ...matchedObject };
        });
        setChartData(chart_data);
        setIsChart(true);
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
      {isChart && isMobile && (
        <Paper className="chartStyling" elevation={3}>
          <BarChart       
            dataset={chartData}
            series={[{ dataKey: 'count', label: 'Weekly Patient Visits Overview', color: "#1976d2" }]}
            {...chartSetting}
            sx={{ width: "85% !important", fontSize: "18px" }}
            xAxis={[{
              scaleType: 'band', dataKey: 'day',
              tickLabelStyle: {
                angle: 45,
                textAnchor: 'start',
                fontSize: 12,
              },
            }]}
          />
        </Paper>
      )}
      {isChart && !isMobile && (
        <Paper className="chartStyling" elevation={3}>
          <BarChart       
            dataset={chartData}
            series={[{ dataKey: 'count', label: 'Weekly Patient Visits Overview', color: "#1976d2" }]}
            {...chartSetting}
            sx={{ width: "85% !important", fontSize: "18px" }}
            xAxis={[{ scaleType: 'band', dataKey: 'day' }]}
          />
        </Paper>
      )}
    </DashboardWrapper>
  )
}

export default Dashboard