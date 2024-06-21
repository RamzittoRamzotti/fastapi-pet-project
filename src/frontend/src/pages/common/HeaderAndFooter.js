import {Link} from "react-router-dom";
import "./HeaderAndFooter.css"
import "../common.css"

export function Header() {
    return (
        <>
            <div className="fixed-container">
                <div className="links">
                    <p><Link to="/library" className="linker">Библиотека</Link></p>
                    <p><Link to="/order" className="linker">Заказать книгу</Link></p>

                </div>
                <div className="auth">
                    <p><Link to="/auth" className="linker">Авторизоваться</Link></p>
                </div>
            </div>
        </>
    )
}

export function Footer() {
    return (
        <div className="fixed-container">
            <p><Link className="btn btn-success" to="https://github.com/RamzittoRamzotti/fastapi-pet-project"
                     target="_blank"
                     rel="noreferrer">fastapi-pet-project</Link> by ramzittoramzotti</p>
        </div>
    );
}