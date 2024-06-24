import React, {useState} from 'react';
import ReactDOM from 'react-dom/client';
import {createBrowserRouter, RouterProvider} from 'react-router-dom';
import Home from './pages/Home'
import './index.css';
import reportWebVitals from './reportWebVitals';
import {Header, Footer} from "./pages/common/HeaderAndFooter";
import {LoginPage, RequireAuth, RefreshToken} from "./pages/Login";
import Logout from "./pages/Logout";
import {RegisterPage} from "./pages/Register";
import {Library} from "./pages/secondary/Library";
import {Order} from "./pages/secondary/Order";


const router = createBrowserRouter(
    [
        {
            path: "/",
            element: (
                <>
                    <header><Header/></header>

                    <RequireAuth><Home/></RequireAuth>
                    <footer><Footer/></footer>
                </>
            )
        },
        {
            path: "/auth",
            element: (
                <>
                    <LoginPage/>
                    <footer><Footer/></footer>
                </>
            )
        },
        {
            path: "/logout",
            element: (
                <>
                    <Logout/>
                </>
            )
        },
        {
            path: "/register",
            element: (
                <>
                    <RegisterPage/>
                    <footer><Footer/></footer>
                </>
            )
        },
        {
            path: "/library",
            element: (
                <>
                    <header><Header/></header>
                    <RequireAuth><Library/></RequireAuth>
                    <footer><Footer/></footer>
                </>
            )
        },
        {
            path: "/order",
            element: (
                <>
                    <header><Header/></header>
                    <RequireAuth><Order/></RequireAuth>
                    <footer><Footer/></footer>
                </>
            )
        }
    ]
)

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <RouterProvider router={router}/>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
