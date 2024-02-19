import { 
    Grid,
    styled, 
    FormLabel,
    TextField,
    Button,
} from "@mui/material";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { genearteOTPPassword, resetPassword } from "./forgotPassword.slice";
import CustomSnackbar from "../../components/CustomSnackbar";

const ModalContainer = styled("div")(({ theme }) => ({
    "&": {
        backgroundColor: "white",
        padding: "20px",
        borderRadius: "8px",
        outline: "none",        
        fontFamily: "sans-serif",
        [theme.breakpoints.up("sm")]: {
            marginTop: "50px",
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "40%",
        },
    },
    "& .title": { 
        textAlign: "center",
        [theme.breakpoints.up("sm")]: {
            paddingTop: "15px",
            fontSize: "25px",
            margin: "0 0 26px 0",
            
        }
    },
    hr: {
        background: "#0089e9",
        height: "1px",
        border: 0,
        width: "90%",
    },
    span: {
        color: "red",
    },
    label: {
        fontWeight: "bold",
    },
    input: {
        color: "#8a97a0",
        boxShadow: "0 1px 0 rgba(0, 0, 0, 0.03)",
    },
    "& .form-input": {
        marginTop: "9px",
        marginBottom: "10px",
    },
    "& .btn-wrapper": {
        display: "flex",
        justifyContent: "center",
    },
    "& .link-text": {
        marginTop: "10px",
    }
}));

  const CustomButton = styled("button")(({ theme }) => ({
    "&": theme.typography.primaryButton,
  }));

//   const Form = styled("form")({
//     margin: "0 auto",
//   });
const ForgotPasswordPage = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const [isForgotPassword, setIsForgotPassword] = useState(false);
    const [stepOne, setStepOne] = useState(true);
    const [stepTwo, setStepTwo] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");
    const [showSnackbar, setShowSnackbar] = useState(false);
    const [snackbarStatus, setSnackbarStatus] = useState("");
    const [formData, setFormData] = useState({
        mobileNumber: "",
        oldPassword: "",
        newPassword: "",
        otp: ""
    });
    const isAuthenticated = sessionStorage.getItem("accesstoken");
    const resetEMRForm = () => {
        setFormData({
            mobileNumber: "",
            oldPassword: "",
            newPassword: "",
            otp: ""
        });
        setStepOne(true);
        setStepTwo(false);
    }
    const handlePasswordChange = (e) => {
        resetEMRForm();
        setIsForgotPassword(false);
    }
    const handleResetChange = (e) => {
        resetEMRForm();
        setIsForgotPassword(true);
    }
    
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleChangePasswordSubmit = (event) => {
        event.preventDefault();
        const payload = {
            mobile_number: formData.mobileNumber,
            old_password: formData.oldPassword,
            new_password: formData.newPassword,
        }
        dispatch(resetPassword(payload)).then((res) => {
            if (res?.error) {
                setSnackbarStatus("error");
                setSnackbarMessage("Something went wrong");
                setShowSnackbar(true);
                return;
            } else {
                setSnackbarStatus("success");
                setSnackbarMessage("Password changed successfully");
                setShowSnackbar(true);
                if(isAuthenticated){
                    sessionStorage.clear();
                }
                setTimeout(() => navigate("/login"), 2000);
            }
          });
    }

    const handleGenerateOtp = (event) => {
        event.preventDefault();
        const payload = {
            mobile_number: formData.mobileNumber
        }
        dispatch(genearteOTPPassword(payload)).then((res) => {
            if (res?.error) {
                setSnackbarStatus("error");
                setSnackbarMessage("Something went wrong");
                setShowSnackbar(true);
              return;
            } else {
                setSnackbarStatus("success");
                setSnackbarMessage("OTP sent successfully");
                setShowSnackbar(true);
                setStepOne(false);
                setStepTwo(true);
            }
          });
    }

    const handleForgotPasswordSubmit = (event) => {
        event.preventDefault();
        const payload = {
            mobile_number: formData.mobileNumber,
            new_password: formData.newPassword,
            otp: formData.otp
        }
        dispatch(resetPassword(payload)).then((res) => {
            if (res?.error) {
                setSnackbarStatus("error");
                setSnackbarMessage("Something went wrong");
                setShowSnackbar(true);
                return;
            } else {
                setSnackbarStatus("success");
                setSnackbarMessage("Password reset successfully");
                setShowSnackbar(true);
                if(isAuthenticated){
                    sessionStorage.clear();
                }
                setTimeout(() => navigate("/login"), 2000);
            }
          });
    }
    const onSnackbarClose = () => {
        setShowSnackbar(false);
    };

    return(
        <ModalContainer>
            <CustomSnackbar
                message={snackbarMessage}
                open={showSnackbar}
                status={snackbarStatus}
                onClose={onSnackbarClose}
            />
            {isForgotPassword ? (
                <>
                    <h3 className="title">Forgot your password?</h3>
                    <hr></hr>
                    <div style={{ padding: "24px" }}>
                        <Grid container spacing={4} sx={{ marginBottom: "32px" }}>
                            <Grid item xs={12}>
                                <FormLabel>Mobile Number</FormLabel>
                                <TextField
                                    className="form-input"
                                    fullWidth
                                    name="mobileNumber"
                                    value={formData.mobileNumber}
                                    onChange={handleChange}
                                />
                            </Grid>
                            {stepTwo && 
                                <>
                                    <Grid item xs={12}>
                                        <FormLabel>New Password</FormLabel>
                                        <TextField
                                            className="form-input"
                                            fullWidth
                                            name="newPassword"
                                            value={formData.newPassword}
                                            onChange={handleChange}
                                        />
                                    </Grid>
                                    <Grid item xs={12}>
                                        <FormLabel>OTP</FormLabel>
                                        <TextField
                                            className="form-input"
                                            fullWidth
                                            name="otp"
                                            value={formData.otp}
                                            onChange={handleChange}
                                        />
                                    </Grid>
                                </>
                            }
                        </Grid>
                        {stepOne && 
                            <div className="btn-wrapper">
                                <CustomButton onClick={handleGenerateOtp} type="submit">Get OTP</CustomButton>
                            </div>
                        }
                        {stepTwo && 
                            <div className="btn-wrapper">
                                <CustomButton onClick={handleForgotPasswordSubmit} type="submit">Submit</CustomButton>
                            </div>
                        }
                        <div className="btn-wrapper">
                            <Button className="link-text" onClick={handlePasswordChange}>
                                Change Password?
                            </Button>
                        </div>
                        {!isAuthenticated &&
                            <div className="btn-wrapper">
                                <Button onClick={() => navigate("/login")}>
                                    Login
                                </Button>
                            </div>
                        }
                    </div>
                </>
                ) : (
                <>
                    <h3 className="title">Change your password</h3>
                    <hr></hr>
                    <div style={{ padding: "24px" }}>
                        <Grid container spacing={4} sx={{ marginBottom: "32px" }}>
                            <Grid item xs={12}>
                                <FormLabel>Mobile Number</FormLabel>
                                <TextField
                                    className="form-input"
                                    fullWidth
                                    name="mobileNumber"
                                    value={formData.mobileNumber}
                                    onChange={handleChange}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <FormLabel>Old Password</FormLabel>
                                <TextField
                                    className="form-input"
                                    fullWidth
                                    name="oldPassword"
                                    value={formData.oldPassword}
                                    onChange={handleChange}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <FormLabel>New Password</FormLabel>
                                <TextField
                                    className="form-input"
                                    fullWidth
                                    name="newPassword"
                                    value={formData.newPassword}
                                    onChange={handleChange}
                                />
                            </Grid>
                        </Grid>
                        <div className="btn-wrapper">
                            <CustomButton onClick={handleChangePasswordSubmit} type="submit">Submit</CustomButton>
                        </div>
                        <div className="btn-wrapper">
                        <Button className="link-text" onClick={handleResetChange}>
                            Forgot Password?
                        </Button>
                        </div>
                        {!isAuthenticated &&
                            <div className="btn-wrapper">
                                <Button onClick={() => navigate("/login")}>
                                    Login
                                </Button>
                            </div>
                        }
                    </div>
                </>
            )}
        </ModalContainer>
    )
};

export default ForgotPasswordPage;