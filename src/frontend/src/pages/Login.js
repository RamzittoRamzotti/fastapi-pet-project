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
    let navigate = useNavigate()
    const handleLogin = async (username, password) => {
        try {
            const response = await fetch('http://localhost:5001/auth/jwt/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({username, password}),
            }).then(data => data.json())
                .then(
                    data => {
                        console.log("success: %s", data)
                        localStorage.setItem('username', data.token)
                        return navigate('/');
                    }
                )


        } catch (error) {
            console.error('Login error:', error);
        }

    };
    return (
        <div>
            <h2>Login</h2>
            <LoginForm onLogin={handleLogin}/>
        </div>
    );

}

export function RequireAuth({children}) {
    const [token, setToken] = useState("");
    const [isLoading, setIsLoading] = useState(true);
    const location = useLocation();

    const fetchToken = async (email) => {
        try {
            const response = await fetch('http://localhost:5001/auth/request-verigy-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    email
                }),
            });
            const data = await response.json();
            if (response.ok) {
                setToken(data); // Assuming 'username' is part of the response
            } else {
                throw new Error('Failed to fetch user');
            }
        } catch (error) {
            console.error('Login error:', error);
        }
        setIsLoading(false);

    }
    fetchToken();
    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (!user) {
        return <Navigate to="/auth" state={{from: location}} replace/>;
    }

    return children;
}