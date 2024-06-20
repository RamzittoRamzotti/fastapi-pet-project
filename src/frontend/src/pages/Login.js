import {useEffect, useState} from "react";
import React from 'react';
import {Navigate, useLocation, useNavigate} from 'react-router-dom';
import "./common.css"

export function LoginForm({onLogin}) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        onLogin(username, password);
    };

    return (
        <div className="loginBlock">
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}


export function LoginPage() {
    let navigate = useNavigate();
    const [error, setError] = useState("");

    const handleLogin = async (username, password) => {
        try {
            const response = await fetch('http://localhost:5005/login/auth', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({username, password}),
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'Login failed');
            }
            console.log("Login success: ", data);
            localStorage.setItem('token', data.token);
            navigate('/');  // Navigate to the home page or dashboard
        } catch (error) {
            console.error('Login error:', error);
            setError(error.message);
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <p className="error">{error}</p>}
            <LoginForm onLogin={handleLogin}/>
        </div>
    );
}

export function RequireAuth({children}) {
    const location = useLocation();
    const token = localStorage.getItem('token');  // Get the token from storage
    const [error, setError] = useState("");

    const oauth = async () => {
        try {
            const response = await fetch('http://localhost:5005/users/me', {
                method: 'GET',
                headers: 'Authorization Bearer ' + token,
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || 'auth failed');
            }
            console.log("auth success: ", data);
        } catch (error) {
            console.error('auth error:', error);
            setError(error.message);
        }
    };
    if (!token) {
        // Redirect to the login page if no token is found
        return <Navigate to="/auth" state={{from: location}} replace/>;
    }

    return children;
}