import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";

export function Library() {
    const access_token = localStorage.getItem('access_token');
    let navigate = useNavigate();
    const [mess, setMess] = useState({});

    useEffect(() => {
        if (!access_token) {
            return navigate('/auth');

        }
        fetch('http://localhost:5000/books/', {
            method: 'GET'

        })
            .then(res => res.json())
            .then(mess => {
                setMess(mess);
                console.log(mess);
            });
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