import React, { useState, useEffect } from 'react';

function App() {
    const [message, setMessage] = useState({});

    useEffect( () => {
            fetch('/api', {mode:"no-cors"})
            .then( res =>  res.json())
            .then(message => {
                setMessage(message);
                console.log(message);
            });
    }, []);

    return (
        <div className="App">
            {(typeof message.Hello == 'undefined') ?
                (<p>LOADING...</p>) :
                (<p>{message.Hello}</p>)}
        </div>
    );
}
export default App;