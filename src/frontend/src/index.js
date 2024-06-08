import React from 'react';
import ReactDOM from 'react-dom/client';
import {createBrowserRouter, RouterProvider} from 'react-router-dom';
import Home from './pages/Home'
import './index.css';
import reportWebVitals from './reportWebVitals';
import {Header, Footer} from "./pages/common/HeaderAndFooter";

const router = createBrowserRouter(
    [
        {
            path: "/",
            element: (
                <>
                    <Header/>
                    <Home/>
                    <Footer/>
                </>
            )
        }
        // {
        //     path: "/about",
        //     element: (
        //         <>
        //             <Header/>
        //                 <About/>
        //             <Footer/>
        //         </>
        //     )
        // },
        // {
        //     path: "/order",
        //     element: (
        //         <>
        //             <Header/>
        //             <Order/>
        //             <Footer/>
        //         </>
        //     )
        // }
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
