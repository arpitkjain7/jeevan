import React, { useState } from "react";
import { formatDistanceToNow } from "date-fns";
import {
  Stack,
  Avatar,
  Button,
  Paper,
  styled,
  Typography,
  Card,
  CardContent,
  Rating,
  Divider,
  Box,
  CardMedia,
  Grid,
} from "@mui/material";
import CustomBackdrop from "../../components/CustomBackdrop";
import PlayCircleFilledOutlinedIcon from "@mui/icons-material/PlayCircleFilledOutlined";
import DirectionsIcon from "@mui/icons-material/Directions";
import profile from "../../assets/prasad.jpg";
// import {Link} from 'react-router-dom'

const DoctorProfile = () => {
  const ProfileContainer = styled("div")(({ theme }) => ({
    backgroundColor: "#f8f8f8",
    padding: "25px 40px",
    [theme.breakpoints.down("sm")]: {
      padding: "10px",
    },
  }));

  const IntroContainer = styled("header")(({ theme }) => ({
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    borderRadius: "10px",
    marginBottom: "10px",
    [theme.breakpoints.down("sm")]: {
      flexDirection: "column",
      alignItems: "flex-start",
    },
  }));

  const ProfileImage = styled(Avatar)(({ theme }) => ({
    borderRadius: "50%",
    overflow: "hidden",
    width: "100px",
    height: "100px",
    [theme.breakpoints.down("sm")]: {
      width: "60px",
      height: "60px",
    },
  }));

  const DoctorInfoHeader = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    [theme.breakpoints.down("sm")]: {},
  }));

  const DoctorInfo = styled("div")(({ theme }) => ({
    flex: 1,
    marginLeft: "20px",

    "&h2": {
      marginTop: "3px",
      marginBottom: "3px",
    },
    "& p": {
      color: "#5B5B5A",
      fontSize: "small",
      margin: 0,
    },
    "& span": {
      fontSize: "16px",
      color: "black",
      letterSpacing: "0.5px",
    },
  }));

  const AppointmentContainer = styled("div")(({ theme }) => ({
    textAlign: "right",
    "& button": {
      backgroundColor: "#0088E8",
      color: "white",
      padding: "10px 20px",
      fontSize: "13px",
      fontWeight: "bold",
      border: "none",
      borderRadius: "5px",
      cursor: "pointer",
      marginBottom: "10px",
      [theme.breakpoints.down("sm")]: {
        marginTop: "10px",
      },
    },
    "& p": {
      fontSize: "small",
      letterSpacing: "0.5px",
      [theme.breakpoints.down("sm")]: {
        fontSize: "12px",
        letterSpacing: "0.3px",
      },
    },
    "& span": {
      fontWeight: 600,
      letterSpacing: "0.8px",
    },
  }));

  const DetailsCard = styled(Paper)(({ theme }) => ({
    backgroundColor: "#fff",
    padding: "10px 18px",
    borderRadius: "5px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
    marginTop: "18px",
    width: "43vw",
    height: "226px",
    display: "flex",
    flexDirection: "column",
    overflowY: "auto",
    scrollbarWidth: "thin",
    [theme.breakpoints.down("sm")]: {
      width: "100%",
    },
  }));

  const Details = styled("div")(({ theme }) => ({
    "& p": {
      fontSize: "14px",
      fontWeight: "bold",
      color: "#5A5A5A",
      margin: "5px 0px",
    },
  }));

  const DetailsColumn = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "column",
    width: "100%",
    [theme.breakpoints.down("sm")]: {
      width: "100%",
    },
  }));

  const DetailsBody = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "row",
    marginTop: "15px",
    [theme.breakpoints.down("sm")]: {
      marginTop: "10px",
    },
  }));

  const DetailsRow = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "column",
    height: "80px",
  }));

  const DetailsLabel = styled("span")(({ theme }) => ({
    fontWeight: "bold",
    fontSize: "small",
    color: "#5A5A5A",
  }));

  const DetailsInfo = styled("span")(({ theme }) => ({
    marginTop: "1px",
    fontWeight: 900,
  }));

  const TreatsContainer = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    [theme.breakpoints.down("sm")]: {
      flexDirection: "column",
    },
  }));

  const Treats = styled("div")(({ theme }) => ({
    marginTop: "15px",
    display: "flex",
    flexWrap: "wrap",
    "& span": {
      border: "0.5px solid #b3aeae",
      borderRadius: "7px",
      padding: "5px 10px 5px 10px",
      margin: "13px 10px",
    },
    height: "130px",
    overflowY: "scroll",
    scrollbarWidth: "none",
    [theme.breakpoints.down("sm")]: {
      justifyContent: "center",
    },
  }));

  const AboutCard = styled(Paper)(({ theme }) => ({
    backgroundColor: "#fff",
    padding: "15px 20px",
    borderRadius: "5px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
    marginTop: "20px",
    display: "flex",
    flexDirection: "column",
    [theme.breakpoints.down("sm")]: {
      fontSize: "8px",
    },
  }));

  const AddressesContainer = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "column",
    height: "200px",
    overflowY: "auto",
    [theme.breakpoints.down("sm")]: {
      height: "150px",
      marginRight: "0",
      marginBottom: "20px",
    },
  }));

  const AddressContainer = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    border: "1px solid #b3aeae",
    borderRadius: "7px",
    padding: "15px 15px",
    width: "400px",
    marginBottom: "5px",
    [theme.breakpoints.down("sm")]: {
      width: "300px",
      text: "10px",
    },
  }));

  const DetailsAndActionButtonContainer = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    width: "700px",
    [theme.breakpoints.down("sm")]: {
      width: "100%",
    },
    "& button": {
      height: 50,
      width: 200,
      padding: "15px 5px",
      marginLeft: "100px",
      [theme.breakpoints.down("sm")]: {
        marginLeft: 0,
        width: 100,
        fontSize: "8px",
        height: 50,
      },
    },
  }));

  const DirectionContainer = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "row",
    marginTop: "15px",
    [theme.breakpoints.down("sm")]: {
      marginTop: "10px",
      display: "flex",
      flexDirection: "column-reverse",
    },
  }));

  const DetailsContainer = styled("div")(({ theme }) => ({
    display: "flex",
    flexDirection: "column",
    marginLeft: "100px",
    marginTop: "15px",
    [theme.breakpoints.down("sm")]: {
      margin: 0,
      width: "200px",
      display: "flex",
      flexDirection: "row",
      justifyContent: "space-evenly",
    },
  }));

  const [doctorDetails, setDoctorDetails] = useState({
    avatar: profile,
    name: "Dr. Prasad Gurjar",
    registrationNo: "2012020164",
    specialty: "DM Nephrology",
    consultation: "Consultant Nephrology | Transplant Physician",
    experience: "3 Years",
    age: "35 years",
    location: "Nagpur",
    languages: ["English", "Hindi", "Marathi"],
    availability: "Mon-Sat(10:30am-8:00pm)",
    about:
      "Dr. Prasad Gurjar is a respected kidney specialist at Aaradhya Balaji Kidney Care, committed to improving patient health through expert opinion  kidney to kidney patient about their disease  , treatment option and management strategies.He is expert in  hemodialysis, Kidney biopsy   and Kidney  transplant services.  He's known for his skill in preparing patients for dialysis and supporting them through the process, ensuring they receive the best possible treatment with compassion and care. He is also expert in hemodialysis catheter insertion both temporary permanent (perm cath). Aaradhya Balaji Kidney Care also provide services for AV fistula creation which are crucial for hemodialysis. He is specialize in providing comprehensive care for kidney transplant patients, ensuring they receive the necessary medical attention and support throughout their transplant journey.",
    addresses: [
      {
        text: "A-wing, 2 Floor, Neeti Gaurav Complex, Ramdaspeth, Nagpur - 440010",
        location:
          "https://www.google.com/maps/dir//21.134892,79.076768/@21.1348922,78.9943632,12z?entry=ttu",
      },
    ],
    appointmentAvailability: "Monday-Saturday",
    appointmentTime: "10:30am-8:00pm",
    education: [
      {
        year: 2020,
        degree: "DM Nephrology",
        college: "Dr. DY Patil Medical College, Pune",
      },
      {
        year: 2015,
        degree: "MD Genereal Medicine",
        college: "Jawaharlal Nehru Medical College, Wardha",
      },
      {
        year: 2010,
        degree: "MBBS",
        college: "Jawaharlal Nehru Medical College, Wardha",
      },
    ],
    awards: [
      {
        year: 2022,
        name: "Mentor Mentee Award, Argentina",
      },
    ],
    reviews: [
      {
        name: "Ravi, Nagpur",
        feedback:
          "Dr. Prasad is good at explaining things. He answers all your questions and makes sure you know what's going on. It helps a lot.",
        date: "20/03/2024",
        rating: 4,
      },
      {
        name: "Arjun, Nagpur",
        feedback:
          "When you go to see Dr. Prasad, everyone is friendly. It feels good to be there. Dr. Prasad is easy to talk to and very friendly",
        date: "25/03/2024",
        rating: 3,
      },
      {
        name: "Nirali, Amravti",
        feedback:
          "Dr. Prasad is really nice and listens to what you have to say. He makes sure you understand everything and feel okay about your care",
        date: "04/04/2024",
        rating: 4,
      },
      {
        name: "Jagmohan, Wardha",
        feedback:
          "He explains things clearly. I always know what he means because he uses simple words. It makes me feel more sure about my health",
        date: "09/04/2024",
        rating: 4,
      },
    ],
    videos: [
      {
        title: "Parenting Tips: Navigating common childhood illness",
        link: "https://www.youtube.com/watch?v=iWSewFlU6o8",
      },
      {
        title: "Nephrology Kidney",
        link: "https://www.youtube.com/watch?v=fv53QZRk4hs",
      },
      {
        title: "Nephrology - Kidney Physiology Overview",
        link: "https://www.youtube.com/watch?v=KWHasxDRf54",
      },
      {
        title: "Can I reverse kidney disease? Is there a cure?",
        link: "https://www.youtube.com/watch?v=z1nCUmWHvsU",
      },
    ],
  });
  //Treats:

  const [treats, setTreats] = useState([
    "Kidney Diseases",
    "Dialysis",
    "Kidney Transplant",
    "Diabetic Kidney Disease",
    "Hypertension and Kidney Disease",
    "Kidney Stone",
    "Urine Infection",
  ]);

  //address:
  const [selectedAddress, setSelectedAddress] = useState(
    doctorDetails.addresses[0].location
  );
  //STATE FOR BACKDROP
  const [backdrop, setBackDrop] = useState(false);
  const onAppointementSubmit = () => {
    setBackDrop(!backdrop);
  };
  const handleGetDirections = () => {
    const addressToNavigate =
      selectedAddress || doctorDetails.addresses[0].location;
    window.location.href = addressToNavigate;
  };

  //Rating:
  const [value, setValue] = useState(4);

  // const formatTimeDifference = (date) => {
  //   return formatDistanceToNow(new Date(date), { addSuffix: true });
  // };

  const getYouTubeThumbnail = (url) => {
    // Extract the video id from the url
    const videoId = url.split("v=")[1].substring(0, 11);

    // Return the url of the thumbnail
    return `https://img.youtube.com/vi/${videoId}/0.jpg`;
  };

  //click address:
  const handleAddress = (address) => {
    setSelectedAddress(address);
  };

  return (
    <ProfileContainer>
      <div>{backdrop && <CustomBackdrop />}</div>
      <IntroContainer>
        <DoctorInfoHeader>
          <ProfileImage src={doctorDetails.avatar} alt="Doctor Profile Image" />
          <DoctorInfo>
            <Typography variant="body2" color="textSecondary">
              Registration No. : {doctorDetails.registrationNo}
            </Typography>
            <Typography variant="h4">{doctorDetails.name}</Typography>

            <Stack direction="row" spacing={2} sx={{ marginTop: "7px" }}>
              <Typography variant="body1" component="span">
                {doctorDetails.specialty}{" "}
              </Typography>
              <Divider
                orientation="vertical"
                variant="middle"
                flexItem
                sx={{ borderColor: "#00000066" }}
              />{" "}
              <Typography variant="body1" component="span">
                {doctorDetails.consultation}
              </Typography>
            </Stack>
          </DoctorInfo>
        </DoctorInfoHeader>

        <AppointmentContainer>
          <Button
            variant="contained"
            onClick={onAppointementSubmit}
            color="inherit"
          >
            Book Your Appointment
          </Button>

          <Typography variant="body2" color="textSecondary">
            Available:{" "}
            <span style={{ color: "#5B5B5A" }}>
              {doctorDetails.availability}
            </span>
          </Typography>
        </AppointmentContainer>
      </IntroContainer>

      <TreatsContainer>
        <DetailsCard>
          <Details>
            <Typography variant="body1">DETAILS</Typography>
          </Details>
          <DetailsBody>
            <DetailsColumn>
              <DetailsRow>
                <DetailsLabel>Experience</DetailsLabel>
                <DetailsInfo>{doctorDetails.experience}</DetailsInfo>
              </DetailsRow>
              <DetailsRow>
                <DetailsLabel>Age</DetailsLabel>
                <DetailsInfo>{doctorDetails.age}</DetailsInfo>
              </DetailsRow>
            </DetailsColumn>
            <DetailsColumn>
              <DetailsRow>
                <DetailsLabel>Location</DetailsLabel>
                <DetailsInfo>{doctorDetails.location}</DetailsInfo>
              </DetailsRow>
              <DetailsRow>
                <DetailsLabel>Spoken Languages</DetailsLabel>
                <DetailsInfo>{doctorDetails.languages.join(", ")}</DetailsInfo>
              </DetailsRow>
            </DetailsColumn>
          </DetailsBody>
        </DetailsCard>

        <DetailsCard>
          <Details>
            <Typography variant="body1">COMMONLY TREATS</Typography>
          </Details>

          <Treats>
            {treats.map((treat, index) => (
              <span key={index}>{treat}</span>
            ))}
          </Treats>
        </DetailsCard>
      </TreatsContainer>

      <AboutCard>
        <Details>
          <Typography variant="body1">ABOUT</Typography>
        </Details>
        <Typography variant="body1" sx={{ marginBottom: "4px" }}>
          {doctorDetails.about}
        </Typography>
      </AboutCard>

      <AboutCard>
        <Details>
          <Typography variant="body1">APPOINTMENT</Typography>
        </Details>
        <DirectionContainer>
          <AddressesContainer>
            {doctorDetails.addresses.map((address, index) => (
              <AddressContainer
                key={index}
                style={{
                  border:
                    selectedAddress === address.location
                      ? "1px solid blue"
                      : "1px solid #b3aeae",
                }}
              >
                <Button onClick={() => handleAddress(address.location)}>
                  <Typography variant="body1">{address.text}</Typography>
                </Button>
              </AddressContainer>
            ))}
          </AddressesContainer>
          <DetailsAndActionButtonContainer>
            <DetailsContainer>
              <DetailsRow>
                <DetailsLabel>Availability</DetailsLabel>
                <DetailsInfo>
                  {doctorDetails.appointmentAvailability}
                </DetailsInfo>
              </DetailsRow>
              <DetailsRow>
                <DetailsLabel>Time</DetailsLabel>
                <DetailsInfo>{doctorDetails.appointmentTime}</DetailsInfo>
              </DetailsRow>
            </DetailsContainer>
            <Button variant="contained" onClick={handleGetDirections}>
              <DirectionsIcon /> Get Directions
            </Button>
          </DetailsAndActionButtonContainer>
        </DirectionContainer>
      </AboutCard>

      <TreatsContainer>
        <DetailsCard>
          <Details>
            <Typography variant="body1">EDUCATION</Typography>
          </Details>
          <DetailsBody>
            <DetailsColumn>
              {doctorDetails.education.map((edu, index) => (
                <DetailsRow key={index}>
                  <DetailsLabel>{`${edu.degree} - ${edu.year}`}</DetailsLabel>
                  <DetailsInfo style={{ width: { lg: "40vw", sm: "100%" } }}>
                    {edu.college}
                  </DetailsInfo>
                </DetailsRow>
              ))}
            </DetailsColumn>
          </DetailsBody>
        </DetailsCard>

        <DetailsCard>
          <Details>
            <Typography variant="body1">AWARDS</Typography>
          </Details>
          <DetailsBody>
            <DetailsColumn>
              {doctorDetails.awards.map((award, index) => (
                <DetailsRow key={index}>
                  <DetailsInfo style={{ width: "100%" }}>
                    {`${award.name} - ${award.year}`}
                  </DetailsInfo>
                </DetailsRow>
              ))}
            </DetailsColumn>
          </DetailsBody>
        </DetailsCard>
      </TreatsContainer>

      <AboutCard sx={{ height: 350 }}>
        <Details>
          <Typography variant="body1">
            IN THEIR OWN WORDS: PRASAD'S IMPACT
          </Typography>
        </Details>
        <Box sx={{ overflowX: "auto", width: "100%", padding: "10px" }}>
          <Grid
            container
            spacing={2}
            sx={{ display: "flex", flexDirection: "row", gap: "20px" }}
          >
            {doctorDetails.reviews.map((review, index) => (
              <Grid item key={index} sx={{ minWidth: "250px" }}>
                <Card variant="outlined" sx={{ maxWidth: 250, height: "100%" }}>
                  <CardContent sx={{ height: 180 }}>
                    <Typography variant="body1" sx={{ color: "#5B5A5B" }}>
                      {review.feedback}
                    </Typography>
                  </CardContent>
                  <Divider variant="middle" />
                  <Box
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      padding: "15px",
                    }}
                  >
                    <Stack direction="column" spacing={1}>
                      <Typography variant="body2" component="span">
                        {review.name}
                      </Typography>
                      <Typography
                        variant="body1"
                        color="textSecondary"
                        component="span"
                        fontSize={12}
                      >
                        {/* {formatTimeDifference(review.date)} */}
                        {review.date}
                      </Typography>
                    </Stack>

                    <Rating
                      name={`size-small-${index}`}
                      value={review.rating}
                      readOnly
                      size="small"
                    />
                  </Box>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      </AboutCard>

      {/* Videos */}
      <AboutCard>
        <Details>
          <Typography variant="body1">
            INFORMED PARENTING WITH NARESH
          </Typography>
        </Details>

        <Stack
          direction="row"
          spacing={5}
          sx={{ marginTop: "10px", overflowX: "auto", scrollbarWidth: "thin" }}
        >
          {doctorDetails.videos.map((video, index) => (
            <a style={{ textDecoration: "none" }} key={index} href={video.link}>
              <Card variant="outlined" sx={{ width: 280, height: 200 }}>
                <CardMedia
                  sx={{ height: 120, backgroundColor: "#D9D9D9" }}
                  image={getYouTubeThumbnail(video.link)}
                >
                  <PlayCircleFilledOutlinedIcon
                    sx={{
                      float: "inline-end",
                      marginTop: "75px",
                      marginRight: "10px",
                    }}
                    fontSize="large"
                  />
                </CardMedia>
                <CardContent>
                  <Typography variant="body2" component="div">
                    {video.title}
                  </Typography>
                </CardContent>
              </Card>
            </a>
          ))}
        </Stack>
      </AboutCard>
    </ProfileContainer>
  );
};

export default DoctorProfile;
