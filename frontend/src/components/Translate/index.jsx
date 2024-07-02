import { Box, FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import axios from "axios";
import React, { useEffect, useState } from "react";

const Translate = ({ translatedContent, setTranslatedContent, setOpen }) => {
  const [language, setLanguage] = useState("");

  const generateAnswers = async (selectedLanguage, retryCount = 0) => {
    if (retryCount >= 4) {
      alert("Unable to Translate.");
      return;
    }
    try {
      const payload = {
        contents: [
          {
            parts: [
              {
                text: `Translate the data object's values into ${selectedLanguage}.  ${JSON.stringify(
                  translatedContent
                )}`,
              },
            ],
          },
        ],
      };
      const response = await axios({
        url: "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyDKjKvLVUdMMzXNguUsdbkPNBLc--94lHE",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        data: JSON.stringify(payload),
      });

      const responseData =
        response?.data?.candidates[0]?.content?.parts[0]?.text;
      if (response?.data?.candidates[0]?.finishReason === "OTHER") {
        setTimeout(() => {
          generateAnswers(selectedLanguage, retryCount + 1);
        }, 4000);
      } else {
        const correctedResponseData = responseData
          .replace(/^```json\n/, "")
          .replace(/\n```$/, "");

        setTranslatedContent(Object.entries(JSON.parse(correctedResponseData)));
        setOpen(false);
        console.log(
          "Translated Content:",
          Object.entries(JSON.parse(correctedResponseData))
        );
      }
    } catch (error) {
      console.error("Error generating translation:", error);
    }
  };

  const handleChange = (event) => {
    const selectedLanguage = event.target.value;
    setLanguage(selectedLanguage);
    generateAnswers(selectedLanguage);
  };

  return (
    <>
      <Box sx={{ minWidth: 120 }}>
        <FormControl fullWidth>
          <InputLabel id="demo-simple-select-label">Language</InputLabel>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={language}
            label="Language"
            onChange={handleChange}
          >
            <MenuItem value={"English"}>English</MenuItem>
            <MenuItem value={"Hindi"}>Hindi</MenuItem>
            <MenuItem value={"Marathi"}>Marathi</MenuItem>
            {/* Add more languages as needed */}
          </Select>
        </FormControl>
      </Box>
    </>
  );
};

export default Translate;
