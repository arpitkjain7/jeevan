import React, { useState } from "react";
import { ReactMediaRecorder } from "react-media-recorder";
import { useDispatch } from "react-redux";
import { recorderAnalysis } from "../../pages/DoctorPage/EMRPage/EMRPage.slice";
import {
  Button,
  Card,
  Grid,
  IconButton,
  Stack,
  Typography,
} from "@mui/material";
import CustomizedSummaryDialog from "../RecordedPatientDataDialog";
import { styled } from "@mui/material/styles";
import MicIcon from "@mui/icons-material/Mic";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import StopIcon from "@mui/icons-material/Stop";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import PauseIcon from "@mui/icons-material/Pause";
import content from "./content.json";
import cliniq360Logo from "../../assets/icons/clinic360Logo.png";

const NumBars = window.innerWidth < 768 ? 20 : 30;

const RecordedSummaryContainer = styled(Card)(({ theme }) => ({
  display: "flex",
  flexDirection: "row",
  alignItems: "center",
  justifyContent: "space-between",
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
  border: "5px solid ",
  borderRadius: "50px",
  width: "35%",
  animation: "borderAnimation 3s infinite",

  [theme.breakpoints.down("md")]: {
    width: "100%",
    margin: theme.spacing(1),
  },

  "@keyframes borderAnimation": {
    "0%": {
      borderColor: "#000000",
    },
    "25%": {
      borderColor: "#333333",
    },
    "50%": {
      borderColor: "#666666",
    },
    "75%": {
      borderColor: "#999999",
    },
    "100%": {
      borderColor: "#CCCCCC",
    },
  },
}));

const shadesOfGray = ["#000000", "#333333", "#666666", "#999999", "#CCCCCC"];

const generateBarStyles = () => {
  const styles = {};
  for (let i = 0; i < NumBars; i++) {
    styles[`&:nth-of-type(${i + 1})`] = {
      animationDelay: `${(i % 10) * 0.1}s`,
      backgroundColor: shadesOfGray[i % 5],
    };
  }
  return styles;
};

const Bar = styled("div")(({ theme }) => ({
  width: "4px",
  height: "100%",
  margin: "0 2px",
  backgroundColor: theme.palette.primary.main,
  animation: "wave 2s infinite",
  animationTimingFunction: "linear",
  ...generateBarStyles(),
  "@keyframes wave": {
    "0%": { height: "20%" },
    "50%": { height: "100%" },
    "100%": { height: "20%" },
  },
}));

const WaveAnimationContainer = styled("div")({
  display: "flex",
  alignItems: "center",
  height: "50px",
  width: "100%", // Adjust the width of the container if needed
  justifyContent: "center",
});

const WaveAnimation = () => (
  <WaveAnimationContainer>
    {[...Array(NumBars)].map((_, i) => (
      <Bar key={i} />
    ))}
  </WaveAnimationContainer>
);

const RecorderComponent = () => {
  const [openSummary, setOpenSummary] = useState(false);
  const [summaryContent, setSummaryContent] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [translatedContent, setTranslatedContent] = useState({});
  const dispatch = useDispatch();

  const handleStopRecording = async (mediaBlobUrl) => {
    try {
      setIsRecording(false);
      const response = await fetch(mediaBlobUrl);
      const audio_file = await response.blob();
      const formData = new FormData();
      formData.append("audio_file", audio_file, "recording.mp3");

      const payload = {
        pmr_id: "C360-PMR-754158906400214266",
        patient_id: "C360-PID-319053493794171106",
        audio_file: formData,
      };

      dispatch(recorderAnalysis(payload)).then((res) => {
        const data = res?.payload?.data;
        setSummaryContent(Object.entries(data));
        setTranslatedContent(res?.payload?.data);
        console.log("res", summaryContent);
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
          <>
            <AudioControlPanel>
              <IconButton
                disabled={isRecording}
                onClick={() => {
                  startRecording();
                  setIsRecording(true);
                }}
              >
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

              {isRecording ? (
                <WaveAnimation>
                  {Array.from({ length: NumBars }).map((_, index) => (
                    <Bar key={index} />
                  ))}
                </WaveAnimation>
              ) : (
                <audio src={mediaBlobUrl} controls muted autoPlay={false} />
              )}
            </AudioControlPanel>
          </>
        )}
        onStop={handleStopRecording}
      />
      {summaryContent.length > 0 && summaryContent[0][1]?.summary && (
        <RecordedSummaryContainer>
          <Stack direction={"row"} alignItems={"center"} gap={2}>
            <IconButton sx={{ backgroundColor: "#89f2ff61" }}>
              <img style={{ height: "20px" }} src={cliniq360Logo} />
            </IconButton>
            <Typography variant="h6">
              {summaryContent[0][1]?.summary}
            </Typography>
          </Stack>
          <Stack>
            <CustomizedSummaryDialog
              open={openSummary}
              setOpen={setOpenSummary}
              summaryContent={summaryContent}
              setSummaryContent={setSummaryContent}
              translatedContent={translatedContent}
              setTranslatedContent={setTranslatedContent}
            />
          </Stack>
        </RecordedSummaryContainer>
      )}
    </>
  );
};

export default RecorderComponent;
