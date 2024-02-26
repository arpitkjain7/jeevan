import * as React from 'react';
import { LineChart } from '@mui/x-charts/LineChart';
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { fetchVitalDetails } from '../VitalsDetails/vitalsDetails.slice';
import { useState } from 'react';
import CustomSnackbar from '../CustomSnackbar';

const uData = [4000, 3000, 2000, 2780, 1890, 2390, 3490];
const pData = [2400, 1398, 9800, 3908, 4800, 3800, 4300];
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
          console.log(res);
          if (res?.error && Object.keys(res?.error)?.length > 0) {
              setShowSnackbar(true);
              return;
            } else {
              // setHeight.push(res?.payload?.value);
              res.payload.map((item) => {
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
                res.payload.map((item) => {
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
        width={500}
        height={300}
        series={[
            { data: weight, label: 'kgs', yAxisKey: 'leftAxisId' },
            { data: height, label: 'cms', yAxisKey: 'rightAxisId' },
        ]}
        xAxis={[{ scaleType: 'point', data: date }]}
        yAxis={[{ id: 'leftAxisId' }, { id: 'rightAxisId' }]}
        rightAxis="rightAxisId"
        />
    </>
  );
}

export default GrowthChart;