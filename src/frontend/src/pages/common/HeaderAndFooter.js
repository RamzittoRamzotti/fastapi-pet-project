import {Link} from "react-router-dom";
import "./HeaderAndFooter.css"
import "../common.css"

export function Header() {
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