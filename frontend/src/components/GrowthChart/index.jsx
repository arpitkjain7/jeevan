import * as React from 'react';
import { LineChart, LinePlot, MarkPlot } from '@mui/x-charts/LineChart';
import { ChartsReferenceLine, ChartsXAxis, ChartsYAxis } from '@mui/x-charts';
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { fetchVitalDetails } from '../VitalsDetails/vitalsDetails.slice';
import { useState } from 'react';
import CustomSnackbar from '../CustomSnackbar';
import { Grid } from '@mui/material';

const boyAge = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0];
const boyHeightPercentile = [3, 10, 25, 50, 75, 90, 97];
const boyHeight3Percentile = [99.0, 101.6, 104.2, 106.8, 109.3, 111.8, 114.3, 116.7, 119.0, 121.3, 123.6, 125.9, 128.2, 130.7, 133.2, 135.7, 138.3, 140.9, 143.4, 145.8, 148.0, 150.0, 151.8, 153.4, 155.0, 156.6, 158.1]
const boyHeight10Percentile = [102.3, 105.0, 107.7, 110.4, 113.0, 115.7, 118.2, 120.8, 123.2, 125.6, 128.1, 130.5, 133.0, 135.6, 138.3, 141.0, 143.7, 146.4, 149.0, 151.5, 153.7, 155.7, 157.4, 159.1, 160.6, 162.1, 163.6];
const boyHeight25Percentile = [105.6, 108.4, 111.2, 114.0, 116.8, 119.6, 122.3, 124.9, 127.5, 130.0, 132.6, 135.2, 137.8, 140.6, 143.3, 146.2, 149.0, 151.8, 154.5, 157.0, 159.2, 161.2, 162.9, 164.5, 165.9, 167.3, 168.7];
const boyHeight50Percentile = [108.9, 111.9, 114.8, 117.8, 120.7, 123.5, 126.4, 129.1, 131.8, 134.5, 137.2, 139.9, 142.7, 145.5, 148.4, 151.4, 154.3, 157.2, 159.9, 162.3, 164.5, 166.5, 168.1, 169.6, 171.0, 172.3, 173.6];
const boyHeight75Percentile = [112.4, 115.4, 118.5, 121.6, 124.6, 127.6, 130.5, 133.4, 136.3, 139.1, 141.9, 144.7, 147.6, 150.5, 153.5, 156.5, 159.5, 162.4, 165.1, 167.6, 169.7, 171.6, 173.1, 174.5, 175.8, 177.0, 178.2];
const boyHeight90Percentile = [115.9, 119.0, 122.2, 125.4, 128.6, 131.7, 134.8, 137.8, 140.7, 143.7, 146.6, 149.5, 152.5, 155.6, 158.6, 161.7, 164.7, 167.6, 170.3, 172.7, 174.8, 176.5, 178.0, 179.3, 180.4, 181.5, 182.5];
const boyHeight97Percentile = [119.4, 122.7, 126.0, 129.3, 132.6, 135.9, 139.1, 142.2, 145.3, 148.3, 151.4, 154.4, 157.5, 160.6, 163.7, 166.8, 169.9, 172.7, 175.4, 177.7, 179.7, 181.4, 182.7, 183.8, 184.8, 185.8, 186.7];
const boySD = [5.7, 5.3, 5.6, 5.5, 5.9, 5.7, 6.3, 6.1, 6.4, 6.4, 6.8, 6.5, 7.6, 7.3, 8.1, 7.9, 9.0, 8.4, 9.0, 7.8, 7.9, 6.6, 7.2, 6.7, 6.9, 6.1, 6.9];

const boyWeight3Percentile = [13.2, 13.8, 14.5, 15.3, 16.0, 16.7, 17.5, 18.3, 19.1, 19.9, 20.7, 21.6, 22.6, 23.8, 24.9, 26.1, 27.5, 29.0, 30.7, 32.6, 34.5, 36.1, 37.5, 38.7, 39.8, 40.8, 41.8]
const boyWeight10Percentile = [14.3, 15.0, 15.8, 16.8, 17.6, 18.5, 19.5, 20.5, 21.5, 22.4, 23.5, 24.6, 25.9, 27.3, 28.7, 30.2, 31.8, 33.6, 35.5, 37.7, 39.8, 41.6, 43.1, 44.4, 45.6, 46.7, 47.7];
const boyWeight25Percentile = [15.6, 16.5, 17.4, 18.6, 19.6, 20.7, 21.9, 23.2, 24.3, 25.6, 26.9, 28.3, 29.8, 31.6, 33.3, 35.1, 37.0, 39.1, 41.3, 43.7, 45.9, 47.9, 49.5, 50.9, 52.1, 53.2, 54.3];
const boyWeight50Percentile = [17.1, 18.2, 19.3, 20.7, 21.9, 23.3, 24.8, 26.4, 27.9, 29.4, 31.1, 32.8, 34.7, 36.9, 39.0, 41.2, 43.3, 45.7, 48.2, 50.8, 53.1, 55.2, 56.8, 58.2, 59.5, 60.6, 61.6];
const boyWeight75Percentile = [19.0, 20.3, 21.7, 23.3, 24.9, 26.6, 28.5, 30.5, 32.3, 34.3, 36.3, 38.5, 40.9, 43.5, 46.0, 48.6, 51.1, 53.8, 56.4, 59.1, 61.6, 63.6, 65.2, 66.6, 67.8, 68.7, 69.7];
const boyWeight90Percentile = [21.3, 22.9, 24.6, 26.6, 28.6, 30.8, 33.2, 35.7, 38.0, 40.5, 43.0, 45.8, 48.7, 51.8, 54.8, 57.8, 60.7, 63.6, 66.3, 69.1, 71.5, 73.4, 74.8, 76.1, 77.1, 77.8, 78.6];
const boyWeight97Percentile = [24.2, 26.1, 28.3, 30.8, 33.4, 36.2, 39.4, 42.6, 45.5, 48.6, 51.8, 55.2, 58.7, 62.5, 66.1, 69.5, 72.6, 75.6, 78.3, 80.9, 83.1, 84.7, 85.8, 86.8, 87.5, 88.0, 88.4];

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
    const yAxis = [{label: 'Weight in KG'}];

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
        console.log(res);
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
    }, []);
  
  return (
    <>
     <CustomSnackbar
        message="Something went wrong"
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
      
        <Grid container spacing={2}>
        
          {/* <Grid item xs={12} md={12}>
             <LineChart
                xAxis={[
                  {
                    id: 'Age',
                    data: boyAge,
                    // scaleType: 'point',
                  },
                ]}
                series={[
                  {
                    id: '3 Percentile',
                    label: '3 Percentile',
                    data: boyHeight3Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    scaleType: "point",
                    color: "red"
                  },
                  {
                    id: '10 Percentile',
                    label: '10 Percentile',
                    data: boyHeight10Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                  },
                  {
                    id: '25 Percentile',
                    label: '25 Percentile',
                    data: boyHeight25Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                  },
                  {
                    id: '50 Percentile',
                    label: '50 Percentile',
                    data: boyHeight50Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                  },
                  {
                    id: '75 Percentile',
                    label: '75 Percentile',
                    data: boyHeight75Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                  },
                  {
                    id: '90 Percentile',
                    label: '90 Percentile',
                    data: boyHeight90Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                  }, 
                  {
                    id: '97 Percentile',
                    label: '97 Percentile',
                    data: boyHeight97Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    color: "red"
                  },
                ]}
                width={900}
                height={500}
                margin={{ left: 70 }}
              />
          </Grid> */}
          <Grid item xs={12} md={12}>
             <LineChart
                xAxis={[
                  {
                    id: 'Age',
                    data: boyAge,
                    label: "Age in Years",
                    scaleType: 'point',
                  },
                  { data: [5, 6, 7, 8, 9] }
                ]}
                yAxis={yAxis}
                series={[
                  {
                    id: '3 Percentile',
                    label: '3 Percentile',
                    data: boyWeight3Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    scaleType: "point",
                    color: "#fc2c2c"
                  },
                  {
                    id: '10 Percentile',
                    label: '10 Percentile',
                    data: boyWeight10Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    color: "#3c3c3c"
                  },
                  {
                    id: '25 Percentile',
                    label: '25 Percentile',
                    data: boyWeight25Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    color: "#3c3c3c"
                  },
                  {
                    id: '50 Percentile',
                    label: '50 Percentile',
                    data: boyWeight50Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    color: "#3c3c3c"
                  },
                  {
                    id: '75 Percentile',
                    label: '75 Percentile',
                    data: boyWeight75Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    color: "#3c3c3c"
                  },
                  {
                    id: '90 Percentile',
                    label: '90 Percentile',
                    data: boyWeight90Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    color: "#3c3c3c"
                  }, 
                  {
                    id: '97 Percentile',
                    label: '97 Percentile',
                    data: boyWeight97Percentile,
                    // stack: 'total',
                    area: false,
                    showMark: false,
                    color: "#fc2c2c"
                  },
                  {
                    data: [15, 18, 20, 25, 28],
                    showMark: true,
                    label: "Patient Weight",
                    color: "black",
                  },
                ]}
                // sx={{ width: "80% !important", fontSize: "18px" }}
                width={900}
                height={500}
                margin={{ left: 70 }}
              >
                <LinePlot />
                <MarkPlot />
                {/* <ChartsReferenceLine
                  x={10}
                  label="Current Age"
                  lineStyle={{ stroke: 'black' }}
                />
                <ChartsReferenceLine y={25} label="Current Weight" lineStyle={{ stroke: 'black' }} /> */}
                <ChartsXAxis />
                <ChartsYAxis />
              </LineChart>
          </Grid>
        </Grid>
    </>
  );
}

export default GrowthChart;