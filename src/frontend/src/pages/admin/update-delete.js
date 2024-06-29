import React, {useState, useEffect} from "react";
import "../secondary/books.css";
import "./add-book.css";
import {useNavigate} from "react-router-dom";

export function UpdateDeletePage() {
    let navigate = useNavigate();
    const [books, setBooks] = useState([]);
    const [text, setText] = useState("");
    const [access_token, setAccessToken] = useState(localStorage.getItem('access_token'));
    const handleDelete = async (book_id) => {
        try {
            const response = await fetch(`http://localhost:5000/api/books/${book_id}`, {
                method: "DELETE"
            });
            if (response.ok) {
                setBooks(prevBooks => prevBooks.filter(book => book.id !== book_id));
                alert("Книга успешно удалена!");

                navigate('/update-delete');
            } else {
                throw new Error("Failed to delete the book.");
            }
        } catch (error) {
            alert(error.message);
        }
    };

    const handleUpdate = (book_id) => {
        navigate(`/update-book/${book_id}`);
    };

    const handleSearch = async (event) => {
        event.preventDefault();
        if (text) {
            console.log(text);
            try {
                const response = await fetch(`http://localhost:5000/api/books/search/?text=${text}`, {
                    method: "GET",
                    headers: {
                        'Authorization': `Bearer ${access_token}`
                    }
                });
                const data = await response.json();
                if (!data['detail']) {
                    setBooks(data['books']);
                } else {
                    throw new Error(data['detail'] || "Failed to fetch books.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert(error.message);
            }
        }
    };

    return (
        <main className="main-update-delete">
            <form className="loginForm" onSubmit={handleSearch}>
                <label htmlFor="text">Поиск книги:</label>
                <input
                    type="text"
                    id="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    required
                />
                <button className="btn btn-success" type="submit">Поиск</button>
            </form>
            <div className="book-div">
                {books.length > 0 ? books.map(book => (
                    <ul key={book.id} className="ul-align">
                        <img src={`http://localhost:5000/images/${book.title_picture}`} alt={book.title}
                             className="book-image"/>
                        <li>Название книги: {book.title}</li>
                        <li>Автор: {book.author}</li>
                        <li>{book.description}</li>
                        <li>
                            <button className="btn btn-dark" onClick={() => handleUpdate(book.id)}
                                    id="button-shift">Изменить
                            </button>
                            <button className="btn btn-danger" onClick={() => handleDelete(book.id)}>Удалить</button>
                        </li>
                    </ul>
                )) : <p>No books found or loading...</p>}
            </div>
        </main>
    );
}
