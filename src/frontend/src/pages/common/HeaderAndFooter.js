import {Link} from "react-router-dom";
import "./HeaderAndFooter.css"

export function Header() {
    return (
        <header>
            <div className="links">
                <p><Link to="/library">Библиотека</Link></p>
                <p><Link to="/order">Заказать книгу</Link></p>

            </div>
            <div className="auth">
                <p><Link to="/auth">Авторизоваться</Link></p>
            </div>
        </header>
    )
}

export function Footer() {
    return (
        <footer>
            <p><Link className="btn btn-success" to="https://github.com/RamzittoRamzotti/fastapi-pet-project"
                     target="_blank"
                     rel="noreferrer">fastapi-pet-project</Link> by ramzittoramzotti</p>
        </footer>
    );
}