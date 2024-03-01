import * as React from 'react';
import { LineChart, LinePlot, MarkPlot } from '@mui/x-charts/LineChart';
import { ChartsReferenceLine, ChartsXAxis, ChartsYAxis } from '@mui/x-charts';
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { fetchVitalDetails } from '../VitalsDetails/vitalsDetails.slice';
import { useState } from 'react';
import CustomSnackbar from '../CustomSnackbar';
import { Grid } from '@mui/material';

const uData = [120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170];
const pData = [30, 32, 35, 40, 45, 50, 55, 60, 65, 70, 75];
const xLabels = [
  '26/02/2024',
  'Page B',
  'Page C',
  'Page D',
  'Page E',
  'Page F',
  'Page G',
];

const GrowthChart = () => {
    const dispatch = useDispatch();
    const [height, setHeight] = useState([]);
    const [weight, setWeight] = useState([]);
    const [date, setDate] = useState([]);
    const [age, setAge] = useState("");
    const [gender, setGender] = useState("");
    const [isChart, setIsChart] = useState(false);
    const [showSnackbar, setShowSnackbar] = useState(false);
    const currentPatient = JSON.parse(sessionStorage?.getItem("selectedPatient"));

    const onSnackbarClose = () => {
        setShowSnackbar(false);
    };

    useEffect(() => {
        setAge((age) => [
            ...age,
            currentPatient?.age
        ]);
        setGender(currentPatient?.gender);
        const heightPayload = {
            patient_id: currentPatient?.patientId || currentPatient?.id,
            vital_type: "HT",
          };
        dispatch(fetchVitalDetails(heightPayload)).then((res) => {
          if (res?.error && Object.keys(res?.error)?.length > 0) {
              setShowSnackbar(true);
              return;
            } else {
              // setHeight.push(res?.payload?.value);
              res.payload.reverse().map((item) => {
                const createdDate = (item.created_date).split(" ");
                setDate((date) => [
                  ...date,
                  createdDate[0].toString()
                ])
                setHeight((height) => [
                  ...height,
                  parseInt(item.value),
                ]);
              })
            }
        });
        const weightPayload = {
            patient_id: currentPatient?.patientId || currentPatient?.id,
            vital_type: "WT",
          };
        dispatch(fetchVitalDetails(weightPayload)).then((res) => {
            if (res?.error && Object.keys(res?.error)?.length > 0) {
                setShowSnackbar(true);
                return;
              } else {
                res.payload.reverse().map((item) => {
                  setWeight((weight) => [
                      ...weight,
                      parseInt(item?.value)
                  ]);
                })
              }
        });
        console.log(height, weight, date, gender);
        setIsChart(true);
    }, [])
  return (
    <>
     <CustomSnackbar
        message="Something went wrong"
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
      {isChart && weight.length > 0 && date.length > 0 &&
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <LineChart
              width={450}
              height={400}
              series={[
                  { data: weight, label: 'KG', yAxisKey: 'leftAxisId'}
              ]}
              xAxis={[{ scaleType: 'point', data: date, label: "Age in Years" }]}
              yAxis={[{ id: 'leftAxisId', label: "weight in KG" }]}
              // rightAxis="rightAxisId"
            >
              {/* <LinePlot />
              <MarkPlot />
              <ChartsReferenceLine y={[{pData}, {uData}]} label="Max" lineStyle={{ stroke: 'red' }} />
              <ChartsXAxis />
              <ChartsYAxis /> */}
            </LineChart>
          </Grid>
          <Grid item xs={12} md={6}>
            <LineChart
              width={450}
              height={400}
              series={[
                { data: height, label: 'CM', yAxisKey: 'leftAxisId'}
              ]}
              xAxis={[{ scaleType: 'point', data: date, label: "Age in Years" }]}
              yAxis={[{ id: 'leftAxisId', label: "Height in CM" }]}
              // rightAxis="rightAxisId"
            >
              {/* <LinePlot />
              <MarkPlot />
              <ChartsReferenceLine y={[{pData}, {uData}]} label="Max" lineStyle={{ stroke: 'red' }} />
              <ChartsXAxis />
              <ChartsYAxis /> */}
            </LineChart>
          </Grid>
          <Grid item xs={12} md={6}>
            <LineChart
              width={450}
              height={400}
              series={[
                  { data: height, label: 'CM', yAxisKey: 'leftAxisId'}
              ]}
              xAxis={[{ scaleType: 'point', data: weight, label: "Weight in KG" }]}
              yAxis={[{ id: 'leftAxisId', label: "Height in CM" }]}
              // rightAxis="rightAxisId"
            >
              {/* <LinePlot />
              <MarkPlot />
              <ChartsReferenceLine y={[{pData}, {uData}]} label="Max" lineStyle={{ stroke: 'red' }} />
              <ChartsXAxis />
              <ChartsYAxis /> */}
            </LineChart>
          </Grid>
        </Grid>
      }
    </>
  );
}

export default GrowthChart;