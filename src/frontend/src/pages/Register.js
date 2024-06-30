import React, {useState} from "react";
import {Navigate, useLocation, useNavigate} from "react-router-dom";

export function RegisterForm({onRegister}) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    let navigate = useNavigate();
    const handleSubmit = async (event) => {
        event.preventDefault();
        onRegister(username, email, password);
    };
    const handleReset = async (event) => {
        event.preventDefault();
        navigate(-1);
    };
    return (
        <div className="loginBlock">
            <form onSubmit={handleSubmit} className="loginForm">
                <div className="input-div">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="input-div">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="input-div">
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <div className="input-div">
                    <button onClick={handleReset} className="btn btn-light">Back to login</button>

                    <button type="submit" className="btn btn-success ">Submit</button>
                </div>
            </form>
        </div>
    );
}

export function RegisterPage() {
    let navigate = useNavigate();
    const [error, setError] = useState("");
    let data;
    const handleRegister = async (username, email, password) => {
        try {
            const response = await fetch('http://backend:5000/login/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({username, email, password, active: true}),
            });

            data = await response.json();
            console.log(data);
            if (!response.ok) {
                throw new Error();
            }
            alert("Registered successfully!");
            navigate('/auth');
        } catch (error) {
            console.error('Register error:', error);
            alert(data.detail[0]['msg'])
            setError(error.message);
        }
    };

    return (
        <div className="loginPage">
            <h2>Registration page</h2>
            {error && <p className="error">{error}</p>}
            <RegisterForm onRegister={handleRegister}/>
        </div>
    );
}