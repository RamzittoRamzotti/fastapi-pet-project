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
            const response = await fetch('http://localhost:5000/login/auth/', {
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
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token)
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
    let navigate = useNavigate();
    const access_token = localStorage.getItem('access_token');  // Get the token from storage
    const refresh_token = localStorage.getItem('refresh_token');  // Get the token from storage

    const [error, setError] = useState("");

    const oauth = async () => {
        try {
            const response = await fetch('http://localhost:5000/login/users/me/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${access_token}`,
                    'accept': 'application/json',
                }
            });

            const data = await response.json();
            let detail = data['detail']
            if (detail === "invalid token error: Signature has expired") {
                RefreshToken(children)
            } else {
                console.log("auth success: ", data);
            }
        } catch (error) {
            console.error('auth error:', error);
            setError(error.message);
        }
    };

    return <>{children}</>;
}

function RefreshToken(props) {
    let navigate = useNavigate();
    const [error, setError] = useState("");
    const refresh_token = localStorage.getItem('refresh_token');
    const oauth = async () => {
        try {
            const response = await fetch('http://localhost:5000/login/refresh/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${refresh_token}`,
                    'accept': 'application/json',
                }
            });
            const token = await response.json()
            if (token.detail) {
                console.log('session expired');
                localStorage.clear();
                navigate('/auth');
            } else {
                localStorage.setItem('access_token', token['access_token']);
                RequireAuth(props.children);
            }
        } catch (error) {
            console.error('auth error:', error);
            setError(error.message);
        }
    }
    useEffect(() => {
            oauth();
        },
        []);
}