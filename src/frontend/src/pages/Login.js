import React, {useEffect, useState} from "react";
import {Navigate, useLocation, useNavigate} from "react-router-dom";
import "./common.css";

export function LoginForm({onLogin}) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    let navigate = useNavigate();
    const handleSubmit = async (event) => {
        event.preventDefault();
        onLogin(username, password);
    };
    const registerClick = async (event) => {
        event.preventDefault();
        navigate('/register');
    }
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
                    <button onClick={registerClick} className="btn btn-light">Sign up</button>
                    <button type="submit" className="btn btn-success">Login</button>

                </div>
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
            navigate('/');
        } catch (error) {
            console.error('Login error:', error);
            setError(error.message);
        }
    };

    return (
        <div className="loginPage">
            <h2>Authentication page</h2>
            {error && <p className="error">{error}</p>}
            <LoginForm onLogin={handleLogin}/>
        </div>
    );
}

async function RefreshToken(navigate, setError, setAccessToken) {
    const refresh_token = localStorage.getItem('refresh_token');
    try {
        const response = await fetch('http://localhost:5000/login/refresh/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${refresh_token}`,
                'Accept': 'application/json',
            },
        });
        const token = await response.json();
        if (token.detail) {
            console.log('session expired');
            localStorage.clear();
            navigate('/auth')
        } else {
            localStorage.setItem('access_token', token.access_token);
            setAccessToken(token.access_token);
        }
    } catch (error) {
        console.error('auth error:', error);
        setError(error.message);
    }
}

export function RequireAuth({children}) {
    let navigate = useNavigate();
    const [access_token, setAccessToken] = useState(localStorage.getItem('access_token'));
    const [error, setError] = useState("");

    useEffect(() => {
        if (localStorage.length === 0) {
            return navigate('/auth')
        }
        const authenticate = async () => {
            try {
                const response = await fetch('http://localhost:5000/login/users/me/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${access_token}`,
                        'Accept': 'application/json',
                    }
                });

                const data = await response.json();
                if (data.detail) {
                    console.log("Session needs refresh");
                    await RefreshToken(navigate, setError, setAccessToken);
                } else {
                    console.log("Auth success: ", data);
                }
            } catch (error) {
                console.error('Auth error:', error);
                setError(error.message);
            }
        };
        authenticate();
    }, [access_token, navigate]);

    if (error) {
        return <p className="error">{error}</p>;
    }
    return <>{children}</>;
}
