import React from "react";
import Box from "@mui/material/Box";
import { Button, Grid, Link, Typography } from "@mui/material";
import LocalPhoneIcon from "@mui/icons-material/LocalPhone";
import InfoIcon from "@mui/icons-material/Info";
import EmailIcon from "@mui/icons-material/Email";
import WorkIcon from "@mui/icons-material/Work";
import LanguageIcon from "@mui/icons-material/Language";
import vCardJs from "vcards-js";
const VirtualCard = () => {
  const sampleData = {
    name: "Dr. Prasad Gurjar",
    userImg:
      "https://imagesx.practo.com/providers/dr-dr-prasad-gurjar-nephrologist-renal-specialist-nagpur-3802c799-847c-4414-a643-1af247e417d1.jpg?i_type=t_70x70",
    designation: "Nephrologist",
    about:
      "Dr. Prasad Gurjar is a respected kidney specialist at Aaradhya Balaji Kidney Care, committed to improving patient health through expert opinion kidney to kidney patient about their disease , treatment option and management strategies.He is expert in hemodialysis, Kidney biopsy and Kidney transplant services. He's known for his skill in preparing patients for dialysis and supporting them through the process, ensuring they receive the best possible treatment with compassion and care. He is also expert in hemodialysis catheter insertion both temporary permanent (perm cath). Aaradhya Balaji Kidney Care also provide services for AV fistula creation which are crucial for hemodialysis. He is specialize in providing comprehensive care for kidney transplant patients, ensuring they receive the necessary medical attention and support throughout their transplant journey.",
    mobile_number: "8275330450",
    email: "aaradhyabalaji99@gmail.com",
    workPlace: "Aaradhya Balaji Kidney Care",
    website: "https://doc.cliniq360.com/view-profile/dr-prasad",
  };

  const handleVcardFunc = () => {
    const vCard = vCardJs();

    // Set vCard properties
    vCard.firstName = sampleData.name;
    vCard.organization = sampleData.workPlace;
    vCard.photo.attachFromUrl(sampleData.userImg, "JPEG");
    vCard.workPhone = sampleData.mobile_number;
    vCard.title = sampleData.designation;
    vCard.url = sampleData.website;
    const vCardString = vCard.getFormattedString();

    const blob = new Blob([vCardString], { type: "text/vcard" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${sampleData.name}.vcf`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    console.log(vCardString);
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Box
          sx={{
            backgroundColor: "White",
            width: "400px",
            height: "655px",
            boxShadow: "20px",
            borderRadius: "5px",
            margin: "10px 10px",
          }}
        >
          <Box
            sx={{
              backgroundColor: "#1976d2",
              width: "auto",
              height: "200px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Box
              sx={{
                height: "100px",
                width: "100px",
                backgroundColor: "white",
                borderRadius: "50%",
                backgroundImage: `url(${sampleData.userImg})`,
                backgroundSize: "cover",
                marginBottom: "10px",
              }}
            ></Box>
            <Typography variant="h3" color={"white"}>
              {sampleData.name}
            </Typography>
            <Typography variant="h3" component="h4" color={"white"}>
              {sampleData.designation}
            </Typography>
          </Box>
          <Box
            sx={{
              height: "100px",
              display: "flex",
              margin: "10px",
              padding: "5px",
            }}
          >
            <Box
              sx={{
                backgroundColor: "white",
                width: "70px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <InfoIcon sx={{ fontSize: "2rem" }} />{" "}
            </Box>
            <Box>
              <Typography sx={{ fontSize: "0.8rem", marginLeft: "10px" }}>
                {sampleData.about.slice(0, 250)}...
              </Typography>
            </Box>
          </Box>
          <Box
            sx={{
              height: "40px",
              display: "flex",
              margin: "10px",
              padding: "5px",
            }}
          >
            <Box
              sx={{
                width: "32px",
                backgroundColor: "white",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <LocalPhoneIcon sx={{ fontSize: "2rem" }} />{" "}
            </Box>
            <Box>
              <Typography
                sx={{ fontSize: "1rem", marginLeft: "10px", cursor: "pointer" }}
              >
                {sampleData.mobile_number}
              </Typography>
              <Typography sx={{ fontSize: "0.7rem", marginLeft: "10px" }}>
                Mobile Number
              </Typography>
            </Box>
          </Box>
          <Box
            sx={{
              height: "40px",
              display: "flex",
              margin: "10px",
              padding: "5px",
            }}
          >
            <Box
              sx={{
                width: "32px",
                backgroundColor: "white",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <EmailIcon sx={{ fontSize: "2rem" }} />{" "}
            </Box>
            <Box>
              <Typography
                sx={{ fontSize: "1rem", marginLeft: "10px", cursor: "pointer" }}
              >
                {sampleData.email}
              </Typography>
              <Typography sx={{ fontSize: "0.7rem", marginLeft: "10px" }}>
                Email
              </Typography>
            </Box>
          </Box>
          <Box
            sx={{
              height: "40px",
              display: "flex",
              margin: "10px",
              padding: "5px",
            }}
          >
            <Box
              sx={{
                width: "32px",
                backgroundColor: "white",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <WorkIcon sx={{ fontSize: "2rem" }} />{" "}
            </Box>
            <Box>
              <Typography
                sx={{ fontSize: "1rem", marginLeft: "10px", cursor: "pointer" }}
              >
                {sampleData.workPlace}
              </Typography>
              <Typography sx={{ fontSize: "0.7rem", marginLeft: "10px" }}>
                {sampleData.designation}
              </Typography>
            </Box>
          </Box>
          <Box
            sx={{
              height: "40px",
              display: "flex",
              margin: "10px",
              padding: "5px",
            }}
          >
            <Box
              sx={{
                width: "32px",
                backgroundColor: "white",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <LanguageIcon sx={{ fontSize: "2rem" }} />{" "}
            </Box>
            <Box>
              <Typography
                sx={{ fontSize: "1rem", marginLeft: "10px", cursor: "pointer" }}
              >
                <Link>{sampleData.website}</Link>
              </Typography>
              <Typography sx={{ fontSize: "0.7rem", marginLeft: "10px" }}>
                Website
              </Typography>
            </Box>
          </Box>
          <Grid
            container
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginTop: "25px",
            }}
          >
            <Grid
              xs={12}
              md={12}
              item
              sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
              marginTop={"20px"}
            >
              <Button
                onClick={handleVcardFunc}
                sx={{ width: "90%" }}
                variant="contained"
              >
                Save
              </Button>
            </Grid>

            <Typography sx={{ marginTop: "5px" }}>©2023 cliniQ360</Typography>
          </Grid>
        </Box>
      </Box>
    </>
  );
};

export default VirtualCard;
