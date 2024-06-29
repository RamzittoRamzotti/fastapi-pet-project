import React, {useState, useEffect} from 'react';
import {useNavigate, useParams} from 'react-router-dom';

export function Order() {
    let navigate = useNavigate();
    const {book_id} = useParams();
    const [books, setBooks] = useState([]);
    const [text, setText] = useState('');
    const access_token = localStorage.getItem('access_token');

    const handleBook = async (book_id) => {
        try {
            const response_ = await fetch('http://localhost:5000/api/login/users/id/', {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${access_token}`,
                    'Accept': 'application/json'
                }
            });
            const users = await response_.json();
            if (!users['user_id']) {
                throw new Error("Failed to fetch user data.");
            }

            const user_id = users['user_id'];
            const email = users['email'];
            const formData = new FormData();
            formData.append("user_id", user_id);
            formData.append("email", email);
            const response = await fetch(`http://localhost:5000/api/books/reserve_book/${book_id}`, {
                method: "PATCH",
                headers: {
                    'Authorization': `Bearer ${access_token}`,
                },
                body: formData,
            });
            const data = await response.json();
            if (data['detail']) {
                throw new Error("Не удалось забронировать книгу!");
            }
            alert("Книга успешно забронирована!");
            return navigate("/library");
        } catch (error) {
            alert(error.message);
            return navigate("/library");
        }
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
        <main>
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
            {books.length > 0 ? (
                <div className="book-div">
                    {books.map((book) => (
                        <ul key={book.id} className="ul-align">
                            <img src={`http://localhost:5000/images/${book.title_picture}`} alt={book.title}
                                 className="book-image"/>
                            <li>Название книги: {book.title}</li>
                            <li>Автор: {book.author}</li>
                            <li>{book.description}</li>
                            {book.user_id ? <li>Нет в наличии =(</li> : (
                                <li>
                                    <button className="btn btn-dark" onClick={() => handleBook(book.id)}>Забронировать
                                    </button>
                                </li>
                            )}
                        </ul>
                    ))}
                </div>
            ) : (
                <p>Книги по запросу не найдены.</p>
            )}
        </main>
    );
}
