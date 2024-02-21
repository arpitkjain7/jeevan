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
  '0',
  '1',
  '2',
  '3',
  '4',
  '5',
  '6',
//   '7',
//   '8',
//   '9',
//   '10'
];

const GrowthChart = () => {
    const dispatch = useDispatch();
    const [height, setHeight] = useState([]);
    const [weight, setWeight] = useState([]);
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
                setHeight((height) => [
                    ...height,
                    res?.payload?.value,
                ]);
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
                setWeight((weight) => [
                    ...weight,
                    res?.payload?.value,
                ]);
              }
        });
        console.log(height, weight, gender)
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
            { data: uData, label: 'cms', yAxisKey: 'leftAxisId' },
            { data: pData, label: 'kgs', yAxisKey: 'rightAxisId' },
        ]}
        xAxis={[{ scaleType: 'point', data: xLabels }]}
        yAxis={[{ id: 'leftAxisId' }, { id: 'rightAxisId' }]}
        rightAxis="rightAxisId"
        />
    </>
  );
}

export default GrowthChart;