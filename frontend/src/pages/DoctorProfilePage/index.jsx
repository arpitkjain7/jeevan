import React, { useEffect, useRef, useState } from "react";
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
import { convertTimeSlot } from "../../utils/utils";

const ProfileContainer = styled("div")(({ theme }) => ({
  marginTop: "-67px",
  backgroundColor: "#f8f8f8",
  padding: "25px 40px",
  [theme.breakpoints.down("sm")]: {
    padding: "10px",
  },
  "& #map_attr iframe": {
    width: "100%",
    height: "300px"
  }
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
      "profile_photo": "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",
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
      "updated_at": "2024-06-28T13:11:27.505658",
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
          "name": "ABC Healthcare",
          "id": 1,
          "hip_id": "123123",
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
    
  );
  const [treats, setTreats] = useState([]);
  const [addresses, setAddresses] = useState([]);
  const [selectedAddress, setSelectedAddress] = useState({});
  //STATE FOR BACKDROP
  const [backdrop, setBackDrop] = useState(false);
  const [youtubeLinks, setYoutubeLinks] = useState([]);

  useEffect(() => {
    setAddresses([...doctorDetails?.primary_hip, ...doctorDetails?.external_hips]);
    setSelectedAddress(doctorDetails?.primary_hip[0]);

    if(doctorDetails?.commonly_treats) 
      setTreats(doctorDetails?.commonly_treats.split("||"));

    if(doctorDetails?.educational_content){
    const youtubeVideos = doctorDetails?.educational_content.split("||");
    youtubeVideos.map(url => {
      const videoId = url.split("v=")[1].substring(0, 11);
      setYoutubeLinks(links => [...links, `https://www.youtube.com/embed/${videoId}`]);
    }); 
  }
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
          <ProfileImage src={`data:image/jpeg;base64,${doctorDetails?.profile_photo}`} alt="Doctor Profile Image" />
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

          <Typography variant="body1" color="#5B5B5A" style={{ fontSize: "16px"}}>
            <span>
              {doctorDetails?.doc_working_days}
             <br/>
              {
                doctorDetails?.consultation_start_time 
                ?
                convertTimeSlot(doctorDetails?.consultation_start_time + ' - ' + doctorDetails?.consultation_end_time)
                :
                ""
              }
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
            <div id="map_attr" dangerouslySetInnerHTML={{__html: selectedAddress?.hip_location || selectedAddress?.location}} />
            {/* <iframe 
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3721.4365350743133!2d79.07462427430923!3d21.135018984122247!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bd4c09049d1c997%3A0xe2fe5c9822d82898!2sNeeti%20Gaurav%20Complex!5e0!3m2!1sen!2sin!4v1719432002570!5m2!1sen!2sin"
              width="100%"
              height="300"
              direction
              style={{ border: 0 }} 
              allowfullscreen="true" 
              loading="lazy" 
              referrerpolicy="no-referrer-when-downgrade"
            >
            </iframe> */}
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
                    convertTimeSlot(selectedAddress?.consultation_start_time + ' - ' + selectedAddress?.consultation_end_time)
                    :
                    convertTimeSlot(doctorDetails?.consultation_start_time + ' - ' + doctorDetails?.consultation_end_time)
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
              {doctorDetails?.education.map((edu, index) => (
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
              {doctorDetails?.awards && (
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

      <AboutCard>
        <Details>
          <Typography variant="body1">
            IN THEIR OWN WORDS: <span style={{ textTransform: 'capitalize'}}>{doctorDetails?.doc_name}</span> IMPACT
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
