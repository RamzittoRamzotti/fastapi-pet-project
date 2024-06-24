import {Link, useLocation} from "react-router-dom";
import "./HeaderAndFooter.css"
import "../common.css"
import {useRef} from "react";

export function Header() {
    let location = useLocation();
    console.log(location.pathname);
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