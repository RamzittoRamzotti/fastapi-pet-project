import {useEffect, useState} from "react";
import "./Home.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import {useNavigate} from "react-router-dom";

function Home() {
    const access_token = localStorage.getItem('access_token');  // Get the token from storage
    let navigate = useNavigate();
    const [mess, setMess] = useState({});

    useEffect(() => {
        if (!access_token) {
            return navigate('/auth');

        }
        fetch('http://localhost:5000/api', {
            method: 'GET'

        })
            .then(res => res.json())
            .then(mess => {
                setMess(mess);
                console.log(mess);
            });
    }, []);

    return (
        <main>

            {
                (typeof mess.Hello == 'undefined') ?
                    (<div className="main-div">Loading...</div>) :
                    (
                        <div className="main-div text-success">{mess.Hello}</div>

                    )
            }

        </main>

    );


}

export default Home;