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
import {AdminPage, AddBookPage} from './pages/admin/admin';
import {UpdateDeletePage} from './pages/admin/update-delete';
import UpdateBookPage from "./pages/update/UpdateBook";

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
        },
        {
            path: "/admin",
            element: (
                <>
                    <header><Header/></header>
                    <RequireAuth><AdminPage/></RequireAuth>
                    <footer><Footer/></footer>
                </>
            )
        },
        {
            path: "/add-book",
            element: (
                <>
                    <header><Header/></header>
                    <RequireAuth><AddBookPage/></RequireAuth>
                    <footer><Footer/></footer>
                </>
            )
        }, {
        path: "/update-delete",
        element: (
            <>
                <header><Header/></header>
                <RequireAuth><UpdateDeletePage/></RequireAuth>
                <footer><Footer/></footer>
            </>
        )
    },
        {
            path: "/update-book/:book_id",
            element: (
                <>
                    <header><Header/></header>
                    <RequireAuth><UpdateBookPage/></RequireAuth>
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
