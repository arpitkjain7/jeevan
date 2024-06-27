import { Box, FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import axios from "axios";
import React, { useEffect, useState } from "react";

const Translate = ({ translateContent, setSummaryContent }) => {
  const [language, setLanguage] = useState("");
  const [translation, setTranslation] = useState(null);
  const maxRetries = 4; // Maximum number of retries

  const generateAnswers = async (selectedLanguage, retryCount = 0) => {
    try {
      const response = await axios({
        url: "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyDKjKvLVUdMMzXNguUsdbkPNBLc--94lHE",
        method: "POST",
        data: {
          contents: [
            {
              parts: [
                {
                  text: `Translate the data object's values into ${selectedLanguage}. Also make SURE to generate the response in the exact format as per the input JSON REQUEST. For example, ${JSON.stringify(
                    translateContent
                  )}`,
                },
              ],
            },
          ],
        },
      });

      const responseData =
        response?.data?.candidates[0]?.content?.parts[0]?.text;
      if (
        response?.data?.candidates[0]?.finishReason === "OTHER" &&
        retryCount < maxRetries
      ) {
        setTimeout(() => {
          generateAnswers(selectedLanguage, retryCount + 1);
        }, 4000);
      } else {
        setTranslation(responseData);
        setSummaryContent(responseData);
        console.log(responseData);
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

  useEffect(() => {
    if (language) {
      console.log(`Selected language: ${language}`);
    }
  }, [language]);

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
