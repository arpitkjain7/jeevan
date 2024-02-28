import * as React from 'react';
import { LineChart, LinePlot, MarkPlot } from '@mui/x-charts/LineChart';
import { ChartsReferenceLine, ChartsXAxis, ChartsYAxis } from '@mui/x-charts';
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { fetchVitalDetails } from '../VitalsDetails/vitalsDetails.slice';
import { useState } from 'react';
import CustomSnackbar from '../CustomSnackbar';

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
                console.log(item);
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
        console.log(height, weight, date, gender)
    }, [])
  return (
    <>
     <CustomSnackbar
        message="Something went wrong"
        open={showSnackbar}
        status={"error"}
        onClose={onSnackbarClose}
      />
        <LineChart
        width={800}
        height={500}
        series={[
            { data: weight, label: 'kgs', yAxisKey: 'leftAxisId'},
            { data: height, label: 'cms', yAxisKey: 'rightAxisId', color: "#e15759" },
        ]}
        xAxis={[{ scaleType: 'point', data: date, label: "Age in Years" }]}
        yAxis={[{ id: 'leftAxisId', label: "weight in KG" }, { id: 'rightAxisId', label: "Height in CM" }]}
        rightAxis="rightAxisId"
        >
         <LinePlot />
        <MarkPlot />
          {/* <ChartsReferenceLine
            x={uData}
            label="Max PV PAGE"
            lineStyle={{ stroke: 'red' }}
          /> */}
          <ChartsReferenceLine y={[{pData}, {uData}]} label="Max" lineStyle={{ stroke: 'red' }} />
          <ChartsXAxis />
        <ChartsYAxis />
      </LineChart>
    </>
  );
}

export default GrowthChart;