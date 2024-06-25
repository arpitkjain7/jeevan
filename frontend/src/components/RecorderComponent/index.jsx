import React, { useState } from "react";
import { ReactMediaRecorder } from "react-media-recorder";
import { useDispatch } from "react-redux";
import { recorderAnalysis } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";

const RecorderComponent = () => {
  const [mediaUrl, setMediaUrl] = useState(null);
  const dispatch = useDispatch();

  const handleStopRecording = async (mediaBlobUrl) => {
    setMediaUrl(mediaBlobUrl);

    try {
      const response = await fetch(mediaBlobUrl);
      const audio_file = await response.blob();
      console.log(audio_file);
      const formData = new FormData();
      formData.append("audio_file", audio_file, "recording.mp3");
      for (let [key, value] of formData.entries()) {
        console.log(key, value);
      }
      const payload = {
        pmr_id: "C360-PMR-754158906400214266",
        patient_id: "C360-PID-319053493794171106",
        audio_file: formData,
      };

      dispatch(recorderAnalysis(payload)).then((res) => {
        console.log(res);
      });
    } catch (error) {
      console.error("Error handling mediaBlobUrl:", error);
    }
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
