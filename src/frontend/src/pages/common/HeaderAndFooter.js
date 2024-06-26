import {Link, useLocation} from "react-router-dom";
import "./HeaderAndFooter.css"
import "../common.css"
import {useEffect, useRef, useState, useSyncExternalStore} from "react";
import userEvent from "@testing-library/user-event";

export function Header() {
    let location = useLocation();
    const [admin, setAdmin] = useState(false);
    console.log(location.pathname);
    // const access_token = localStorage.getItem("access_token");
    // const isAdmin = async () => {
    //     try {
    //         const response = fetch("http://localhost:5000/login/users/me/", {
    //             method: "GET",
    //             headers: {
    //                 'Authorization': `Bearer ${access_token}`,
    //                 'Accept': 'application/json'
    //             }
    //         });
    //         let data = response.json();
    //         if (data.detail) {
    //             throw new Error(data.detail);
    //         }
    //         setAdmin(data['admin']);
    //     } catch (error) {
    //         console.log(error);
    //     }
    // }
    // useEffect(() => {
    //     isAdmin();
    // }, [])
    if (location.pathname === '/') {
        return (
            <>
                <div className="fixed-container">
                    <div className="links">
                        <p><Link to="/library" className="linkers">Библиотека</Link></p>
                        <p><Link to="/order" className="linkers">Заказать книгу</Link></p>

                    </div>
                    <div className="auth">
                        <p><Link to="/logout" className="btn btn-danger">Выйти</Link></p>
                    </div>
                </div>
            </>
        )
    } else if (location.pathname === '/library') {
        return (
            <>
                <div className="fixed-container">
                    <div className="links">
                        <p><Link to="/" className="linkers">На главную</Link></p>
                        <p><Link to="/order" className="linkers">Заказать книгу</Link></p>

                    </div>
                    <div className="auth">
                        <p><Link to="/logout" className="btn btn-danger">Выйти</Link></p>
                    </div>
                </div>
            </>
        )
    } else {
        return (
            <>
                <div className="fixed-container">
                    <div className="links">
                        <p><Link to="/" className="linkers">На главную</Link></p>
                        <p><Link to="/library" className="linkers">Библиотека</Link></p>
                    </div>
                    <div className="auth">
                        {admin && <p><Link to='/admin' className='btn btn-dark'>Админка</Link></p>}
                        <p><Link to="/logout" className="btn btn-danger">Выйти</Link></p>
                    </div>
                </div>
            </>
        )
    }

}

export function Footer() {
    return (
        <div className="fixed-container footers">
            <p><Link className="btn btn-success" to="https://github.com/RamzittoRamzotti/fastapi-pet-project"
                     target="_blank"
                     rel="noreferrer">fastapi-pet-project</Link> by ramzittoramzotti</p>
        </div>
    );
}
