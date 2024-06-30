import {useEffect, useState} from "react";
import "./Home.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import {useNavigate} from "react-router-dom";

function Home() {
    let navigate = useNavigate();
    const [mess, setMess] = useState({});
    const access_token = localStorage.getItem('access_token');

    useEffect(() => {
        if (!access_token) {
            return navigate('/auth');
        }
        const hello = async () =>
            fetch('http://backend:5000/api', {
                method: 'GET'

            })
                .then(res => res.json())
                .then(mess => {
                    setMess(mess);
                    console.log(mess);
                });
        hello();
    }, []);


    return (
        <main className="fixed-container">

            {
                (typeof mess.Hello == 'undefined') ?
                    (<div className="main-div">Loading...</div>) :
                    (
                        <div className="main-div text-success ">{mess.Hello}</div>

                    )
            }

        </main>

    );


}

export default Home;