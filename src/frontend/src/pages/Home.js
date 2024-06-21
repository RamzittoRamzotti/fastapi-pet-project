import {useEffect, useState} from "react";
import "./Home.css"
import 'bootstrap/dist/css/bootstrap.min.css';

function Home() {
    const access_token = localStorage.getItem('access_token');  // Get the token from storage

    const [mess, setMess] = useState({});
    useEffect(() => {
        fetch('http://localhost:5000/api', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${access_token}`,
                'accept': 'application/json',
            }
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