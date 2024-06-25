import React, { useState } from "react";
import { ReactMediaRecorder } from "react-media-recorder";
import { useDispatch } from "react-redux";
import { recorderAnalysis } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import { Button, Card, Grid, IconButton, Typography } from "@mui/material";
import CustomizedSummaryDialog from "../RecordedPatientDataDialog";
import { styled } from "@mui/material/styles";
import MicIcon from "@mui/icons-material/Mic";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import StopIcon from "@mui/icons-material/Stop";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import PauseIcon from "@mui/icons-material/Pause";
import content from "./content.json";

const RecordedSummaryContainer = styled(Card)(({ theme }) => ({
  padding: theme.spacing(2),
  margin: theme.spacing(2),
  border: "1px solid #ccc",
  borderRadius: "5px",
}));

const AudioControlPanel = styled(Card)(({ theme }) => ({
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  justifyContent: "center",
  padding: theme.spacing(2),
  margin: theme.spacing(2),
  border: "1px solid #ccc",
  borderRadius: "50px",
  width: "50%",
}));

const RecorderComponent = () => {
  const [openSummary, setOpenSummary] = useState(false);
  const [summaryContent, setSummaryContent] = useState({});
  console.log(summaryContent);
  const dispatch = useDispatch();

  const handleStopRecording = async (mediaBlobUrl) => {
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
        // setSummaryContent(content);
        setSummaryContent(res.payload);
      });
    } catch (error) {
      console.error("Error handling mediaBlobUrl:", error);
    }
  };

  return (
    <>
      <ReactMediaRecorder
        audio
        render={({
          status,
          startRecording,
          stopRecording,
          pauseRecording,
          resumeRecording,
          mediaBlobUrl,
          clearBlobUrl,
        }) => (
          <AudioControlPanel>
            <IconButton onClick={startRecording}>
              <MicIcon
                sx={{ color: status === "recording" ? "Red" : "default" }}
              />
            </IconButton>
            <IconButton onClick={stopRecording}>
              <StopIcon />
            </IconButton>
            <IconButton onClick={pauseRecording}>
              <PauseIcon />
            </IconButton>
            <IconButton onClick={resumeRecording}>
              <PlayArrowIcon />
            </IconButton>
            <IconButton onClick={clearBlobUrl}>
              <RestartAltIcon />
            </IconButton>
            <audio src={mediaBlobUrl} controls autoPlay />
            {/* <a href={mediaUrl} download="myFile">
              Download file
            </a> */}
          </AudioControlPanel>
        )}
        onStop={handleStopRecording}
      />
      {summaryContent?.data?.consultation_summary?.summary && (
        <RecordedSummaryContainer>
          <Grid container xs={12}>
            <Grid item xs={10.5}>
              <Typography variant="h6">
                {summaryContent?.data?.consultation_summary?.summary}
              </Typography>
            </Grid>
            <Grid item xs={1.5}>
              <CustomizedSummaryDialog
                open={openSummary}
                setOpen={setOpenSummary}
                summaryContent={summaryContent}
                setSummaryContent={setSummaryContent}
              />
            </Grid>
          </Grid>
        </RecordedSummaryContainer>
      )}
    </>
  );
};

export default RecorderComponent;
