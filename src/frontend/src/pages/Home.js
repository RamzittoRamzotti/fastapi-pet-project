import {useEffect, useState} from "react";
import "./Home.css"
import 'bootstrap/dist/css/bootstrap.min.css';

function Home() {

    const [mess, setMess] = useState({});
    useEffect(() => {
        fetch('/api', {mode: "no-cors",})
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