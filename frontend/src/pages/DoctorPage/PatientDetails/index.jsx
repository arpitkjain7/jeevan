import React from "react";
import AutoSearch from "../../../components/AutoSearch";
import PatientDetailsHeader from "../../../components/PatientDetailsHeader";


const data = [
    { name: 'Apple', value: 'A' },
    { name: 'Banana', value: 'B' },
    { name: 'Cherry', value: 'C' },
    {name: 'App', value: 'SD'}
    // Add more objects to the array as needed
  ];

function PatientDetails() {
   return (
    <div>
      <PatientDetailsHeader />
    </div>
  )
}

export default PatientDetails;
