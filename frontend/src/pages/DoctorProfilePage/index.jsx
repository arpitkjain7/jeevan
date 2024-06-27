import React, { useEffect, useRef, useState } from "react";
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
  IconButton,
} from "@mui/material";
import CustomBackdrop from "../../components/CustomBackdrop";
import PlayCircleFilledOutlinedIcon from "@mui/icons-material/PlayCircleFilledOutlined";
import LocationOnOutlinedIcon from '@mui/icons-material/LocationOnOutlined';
import DirectionsIcon from "@mui/icons-material/Directions";
import profile from "../../assets/prasad.jpg";
import { useParams } from "react-router-dom";
import ArrowCircleLeftOutlinedIcon from '@mui/icons-material/ArrowCircleLeftOutlined';
import ArrowCircleRightOutlinedIcon from '@mui/icons-material/ArrowCircleRightOutlined';
// import {Link} from 'react-router-dom'

const ProfileContainer = styled("div")(({ theme }) => ({
  marginTop: "-67px",
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
  width: "44vw",
  height: "auto",
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
    fontSize: "19px",
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
  height: "60px",
}));

const DetailsLabel = styled("span")(({ theme }) => ({
  fontWeight: "bold",
  fontSize: "15px",
  color: "#5A5A5A",
}));

const DetailsInfo = styled("span")(({ theme }) => ({
  marginTop: "1px",
  fontSize: "17px",
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
    margin: "7px 5px",
  },
  // height: "130px",
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
  border: "1px solid #b3aeae",
  borderRadius: "7px",
  padding: "10px 0",
  // width: "400px",
  marginBottom: "5px",
  [theme.breakpoints.down("sm")]: {
    // width: "300px",
  },
  "& .address": {
    textAlign: "left", 
    paddingLeft: "5px",
    [theme.breakpoints.down("sm")]: {
      fontSize: "14px",
    }
  }
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

const DoctorProfile = () => {
  const {doctorName} = useParams();
  const reviewNavRef = useRef();
  const videoNavRef = useRef();
  const [doctorDetails, setDoctorDetails] = useState(
    {
      "languages": "Hindi, English",
      "affiliated": true,
      "consultation_fees": 500,
      "external_hips": [
        {
          "name": "Ruby Hall Clinic",
          "mobile_number": "7171818818",
          "location": "<iframe src='https://www.google.com/maps/embed?pb=!1m19!1m8!1m3!1d15126.115498689049!2d73.7102156!3d18.5952671!3m2!1i1024!2i768!4f13.1!4m8!3e6!4m0!4m5!1s0x3bc2bbc313557353%3A0xd6e203ef53147b33!2sRuby%20Hall%20Clinic%2C%20Rajeev%20Gandhi%20Infotech%20Park%2C%20MIDC%20Phase%20No%201%2C%20Plot%20No%2C%20P-33%2C%20Hinjawadi%2C%20Pune%2C%20Maharashtra%20411057!3m2!1d18.5926118!2d73.7340624!5e0!3m2!1sen!2sin!4v1719485348714!5m2!1sen!2sin' width='600' height='450' style='border:0;' allowfullscreen='' loading='lazy' referrerpolicy='no-referrer-when-downgrade'></iframe>",
          "address": "Hinjewadi",
          "doc_working_days": "Saturday-Sunday",
          "consultation_start_time": "10:00",
          "consultation_end_time": "20:00"
        }
      ],
      "email_id": "rachit@gmail.com",
      "doc_specialization": "Ears, Nose, Tongue",
      "awards": "Mentor Mentee Award, Argentina - 2022||Mentor Mentee Award, China - 2024",
      "doc_uid": "dr-rohit-sharma-4-ent-pune",
      "mobile_number": "8458919114",
      "doc_department": "Hospital",
      "follow_up_fees": 300,
      "profile_photo": null,
      "id": 14,
      "bio": "Hi, JASJJ",
      "doc_working_days": "Monday-Friday",
      "years_of_experience": "5",
      "signature": null,
      "age": "45",
      "about": "Blah Blah Blah Blah",
      "doc_licence_no": "BAH83829-UW92B",
      "commonly_treats": "Ears||Nose||Tongue",
      "created_at": "2024-06-27T18:12:16.849051",
      "doc_name": "Dr. Rohit Sharma",
      "hip_id": "123123",
      "avg_consultation_time": "30",
      "google_reviews": [
        {
          "content": "Dr. Prasad is good at explaining things. He answers all your questions and makes sure you know what's going on. It helps a lot.",
          "name": "Ravi, Nagpur",
          "review_date": "20-03-2024",
          "rating": "4"
        },
        {
          "content": "When you go to see Dr. Prasad, everyone is friendly. It feels good to be there. Dr. Prasad is easy to talk to and very friendly",
          "name": "Arjun, Nagpur",
          "review_date": "19-03-2023",
          "rating": "2"
        }
      ],
      "updated_at": "2024-06-27T18:12:16.849090",
      "doc_degree": "MD",
      "consultation_start_time": "09:00:00",
      "educational_content": "https://www.youtube.com/watch?v=iWSewFlU6o8||https://www.youtube.com/watch?v=fv53QZRk4hs",
      "consultation_end_time": "20:00:00",
      "education": [
        {
          "college": "GMC-Nagpur",
          "degree": "MBBS",
          "year": "2015-2019"
        },
        {
          "college": "GMC-Bombay",
          "degree": "MD",
          "year": "2020-2022"
        }
      ],
      "primary_hip": [
        {
          "hip_uid": "ABC",
          "hip_id": "123123",
          "name": "ABC Healthcare",
          "id": 1,
          "hip_city": null,
          "hip_contact_number": null,
          "hfr_reg_number": null,
          "created_at": "2024-06-25T16:22:01.611048",
          "hip_address": "DUMMY",
          "hip_location": null,
          "hip_email_address": null,
          "hfr_status": null,
          "updated_at": "2024-06-25T16:22:01.611112"
        }
      ]
    }
    
  )
  //Treats:

  const [treats, setTreats] = useState([]);

  const [addresses, setAddresses] = useState([]);
  //address:
  const [selectedAddress, setSelectedAddress] = useState({});
  //STATE FOR BACKDROP
  const [backdrop, setBackDrop] = useState(false);
  const [youtubeLinks, setYoutubeLinks] = useState([]);

  useEffect(() => {
    setAddresses([...doctorDetails?.primary_hip, ...doctorDetails?.external_hips]);
    setSelectedAddress(doctorDetails?.primary_hip[0]);

    setTreats(doctorDetails?.commonly_treats.split("||"));
    const youtubeVideos = doctorDetails?.educational_content.split("||");
    youtubeVideos.map(url => {
      const videoId = url.split("v=")[1].substring(0, 11);
      setYoutubeLinks(links => [...links, `https://www.youtube.com/embed/${videoId}`]);
    }); 
  }, []);
  
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
      {backdrop && 
        <CustomBackdrop 
          doctorDetails={doctorDetails}
        />
      }
      <IntroContainer>
        <DoctorInfoHeader>
          <ProfileImage src={doctorDetails?.profile_photo} alt="Doctor Profile Image" />
          <DoctorInfo>
            <Typography variant="body2" color="textSecondary">
              Registration No. : {doctorDetails?.doc_licence_no}
            </Typography>
            <Typography variant="h4">{doctorDetails?.doc_name}</Typography>

            <Stack direction="row" spacing={2} sx={{ marginTop: "7px" }}>
              <Typography variant="body1" component="span">
                {doctorDetails?.doc_specialization}{" "}
              </Typography>
              <Divider
                orientation="vertical"
                variant="middle"
                flexItem
                sx={{ borderColor: "#00000066" }}
              />{" "}
              <Typography variant="body1" component="span">
                {doctorDetails?.doc_degree} 
                {/* consultation */}
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
              {doctorDetails?.doc_working_days}
            </span>
          </Typography>
        </AppointmentContainer>
      </IntroContainer>

      <AboutCard>
        <Typography variant="body1" sx={{ marginBottom: "4px" }}>
          {doctorDetails?.bio}
        </Typography>
      </AboutCard>
      <TreatsContainer>
        <DetailsCard>
          <Details>
            <Typography variant="body1">DETAILS</Typography>
          </Details>
          <DetailsBody>
            <DetailsColumn>
              <DetailsRow>
                <DetailsLabel>Experience</DetailsLabel>
                <DetailsInfo>{doctorDetails?.years_of_experience} Years</DetailsInfo>
              </DetailsRow>
              <DetailsRow>
                <DetailsLabel>Age</DetailsLabel>
                <DetailsInfo>{doctorDetails?.age} Years</DetailsInfo>
              </DetailsRow>
            </DetailsColumn>
            <DetailsColumn>
              <DetailsRow>
                <DetailsLabel>Location</DetailsLabel>
                <DetailsInfo>{addresses[0]?.hip_city}</DetailsInfo>
              </DetailsRow>
              <DetailsRow>
                <DetailsLabel>Spoken Languages</DetailsLabel>
                <DetailsInfo>{doctorDetails?.languages}</DetailsInfo>
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
          {doctorDetails?.about}
        </Typography>
      </AboutCard>

      <AboutCard>
        <Details>
          <Typography variant="body1">APPOINTMENT</Typography>
        </Details>
        <Grid container spacing={4} style={{ padding: "8px 0"}}>
          <Grid item sx={12} md={4}>
            {addresses.map((address, index) => (
              <AddressContainer
                key={index}
                style={{
                  border:
                    (selectedAddress?.hip_address || selectedAddress?.address) === (address?.hip_address || address?.address)
                      ? "1px solid blue"
                      : "1px solid #b3aeae",
                }}
              >
                <Button onClick={() => handleAddress(address)} style={{ justifyContent: "flex-start"}}>
                  <LocationOnOutlinedIcon fontSize="large"></LocationOnOutlinedIcon>
                  <Typography variant="body1" className="address">
                    {address?.hip_address || address?.address}
                  </Typography>
                </Button>
              </AddressContainer>
            ))}
          </Grid>
          <Grid item sx={12} md={8}>
            <iframe 
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3721.4365350743133!2d79.07462427430923!3d21.135018984122247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bd4c09049d1c997%3A0xe2fe5c9822d82898!2sNeeti%20Gaurav%20Complex!5e0!3m2!1sen!2sin!4v1719432002570!5m2!1sen!2sin"
              width="100%"
              height="300"
              direction
              style={{ border: 0 }} 
              allowfullscreen="true" 
              loading="lazy" 
              referrerpolicy="no-referrer-when-downgrade"
            >
            </iframe>
            <div style={{ display: 'flex', direction: 'row'}}>
              <DetailsRow style={{ paddingRight: "40px" }}>
                <DetailsLabel>Availability</DetailsLabel>
                <DetailsInfo>
                  {selectedAddress?.doc_working_days || doctorDetails?.doc_working_days}
                </DetailsInfo>
              </DetailsRow>
              <DetailsRow>
                <DetailsLabel>Time</DetailsLabel>
                <DetailsInfo>
                  {
                    selectedAddress?.consultation_start_time 
                    ?
                    selectedAddress?.consultation_start_time + ' - ' + selectedAddress?.consultation_end_time
                    :
                    doctorDetails?.consultation_start_time + ' - ' + doctorDetails?.consultation_end_time
                  }
                </DetailsInfo>
              </DetailsRow>
            </div>
          </Grid>
        </Grid>
        {/* <Button variant="contained" onClick={handleGetDirections}>
          <DirectionsIcon /> Get Directions
        </Button> */}
      </AboutCard>

      <TreatsContainer>
        <DetailsCard>
          <Details>
            <Typography variant="body1">EDUCATIONAL QUALIFICATIONS</Typography>
          </Details>
          <DetailsBody>
            <DetailsColumn>
              {doctorDetails.education.map((edu, index) => (
                <DetailsRow key={index}>
                  <DetailsLabel>{`${edu.degree} - ${edu.year}`}</DetailsLabel>
                  <DetailsInfo style={{ width: { lg: "1vw", sm: "100%" } }}>
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
              {doctorDetails?.awards !== "None" && (
                doctorDetails?.awards.split("||").map((award, index) => (
                  <DetailsRow>
                    <DetailsInfo style={{ width: "100%" }}>
                      {award}
                      {/* {`${award.name} - ${award.year}`} */}
                    </DetailsInfo>
                  </DetailsRow>
                ))
              )}
            </DetailsColumn>
          </DetailsBody>
        </DetailsCard>
      </TreatsContainer>

      <AboutCard sx={{ height: 360 }}>
        <Details>
          <Typography variant="body1">
            IN THEIR OWN WORDS: PRASAD'S IMPACT
              <div style={{ float: 'right', color: '#1976d2' }}>
                <ArrowCircleLeftOutlinedIcon
                  style={{ behavior: 'smooth' }}
                  onClick={() => reviewNavRef ? (reviewNavRef.current.scrollLeft -= 255) : null }
                />
                <ArrowCircleRightOutlinedIcon
                  style={{ behavior: 'smooth' }}
                  onClick={() => reviewNavRef ? (reviewNavRef.current.scrollLeft += 255) : null }
                />
              </div>
          </Typography>
        </Details>
        <Box sx={{ width: "100%", padding: "10px 10px 10px 0" }}>
          <Stack
            direction="row"
            spacing={4}
            ref={reviewNavRef}
            sx={{ display: "flex", overflowX: "hidden" }}
          >
            {doctorDetails?.google_reviews && 
              doctorDetails.google_reviews.map((review, index) => (
              <div item key={index} sx={{ width: "250px" }}>
                <Card variant="outlined" sx={{ width: 250, height: "280px" }}>
                  <CardContent sx={{ height: 180 }}>
                    <Typography variant="body1" sx={{ color: "#5B5A5B" }}>
                      {review.content}
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
              </div>
            ))}
          </Stack>
        </Box>
      </AboutCard>

      {/* Videos */}
      <AboutCard>
        <Details>
          <Typography variant="body1">
            <>
              INFORMED PARENTING WITH NARESH
        
              <div style={{ float: 'right', color: '#1976d2' }}>
                <ArrowCircleLeftOutlinedIcon
                  style={{ behavior: 'smooth' }}
                  onClick={() => videoNavRef ? (videoNavRef.current.scrollLeft -= 255) : null }
                />
                <ArrowCircleRightOutlinedIcon
                  style={{ behavior: 'smooth' }}
                  onClick={() => videoNavRef ? (videoNavRef.current.scrollLeft += 255) : null }
                />
              </div>
            </>
          </Typography>
        </Details>

        <Stack
          direction="row"
          spacing={5}
          ref={videoNavRef}
          sx={{ marginTop: "10px", overflowX: "hidden", behavior: 'smooth' }}
        >
          {youtubeLinks.length > 0 && youtubeLinks?.map((abc, i) => (
            <>
            <iframe
              src={abc}
              width="250" 
              height="200"
            >
            </iframe>
            </>
           ))}
          {/* {doctorDetails?.educational_content && doctorDetails.educational_content.map((video, index) => (
            <a style={{ textDecoration: "none" }} key={index} href={video}>
              <Card variant="outlined" sx={{ width: 250, height: 200 }}>
                <CardMedia
                  sx={{ height: 120, backgroundColor: "#D9D9D9" }}
                  image={getYouTubeThumbnail(video)}
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
                    {}
                  </Typography>
                </CardContent>
              </Card>
            </a>
          ))} */}
       
        </Stack>
      </AboutCard>
    </ProfileContainer>
  );
};

export default DoctorProfile;
