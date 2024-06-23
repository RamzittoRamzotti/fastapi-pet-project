import {useEffect} from "react";
import {useNavigate} from "react-router-dom";

export default function Logout() {
    let navigate = useNavigate();
    useEffect(function logout() {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        navigate("/auth");
    }, [])
}