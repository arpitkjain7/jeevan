import React, { useState } from "react";
import { ReactMediaRecorder } from "react-media-recorder";
import { useDispatch } from "react-redux";

const RecorderComponent = () => {
  const [mediaUrl, setMediaUrl] = useState(null);
  const dispatch = useDispatch();

  const handleStopRecording = async (mediaBlobUrl) => {
    setMediaUrl(mediaBlobUrl);

    const payload = {
      pmr_id: "C360-PMR-754158906400214266",
      patient_id: "C360-PID-319053493794171106",
      translate: "true",

      mediaUrl: mediaBlobUrl, // Add mediaUrl to the payload
    };

    dispatch({ type: "RECORDING_STOPPED", payload }).then((res) => {
      console.log(res?.payload);
    });
  };

  return (
    <div>
      <ReactMediaRecorder
        audio
        render={({
          status,
          startRecording,
          stopRecording,
          mediaBlobUrl,
          clearBlobUrl,
        }) => (
          <div>
            <p>{status}</p>
            <button onClick={startRecording}>Start Recording</button>
            <button onClick={stopRecording}>Stop Recording</button>
            <audio src={mediaBlobUrl} controls autoPlay />
            <a href={mediaUrl} download="myFile">
              Download file
            </a>
          </div>
        )}
        onStop={handleStopRecording}
      />
    </div>
  );
};

export default RecorderComponent;
