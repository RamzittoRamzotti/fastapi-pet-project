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
            const response = await fetch(`http://localhost:5000/books/update_book/${book_id}`, {
                method: "PATCH",
                headers: {
                    'Authorization': `Bearer ${access_token}`,
                }
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error("Не удалось забронировать книгу!");
            }
            alert("Книга успешно забронирована!");
            navigate("/library");
        } catch (error) {
            alert(error.message);
            navigate("/library");
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://localhost:5000/books/search?text=${text}`, {
                    method: "GET"
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.detail || "Ошибка при поиске книг.");
                }
                setBooks(data.books);
            } catch (error) {
                console.error(error);
                alert(error.message);
                navigate('/error'); // Redirect to an error page or handle differently
            }
        };

        if (text) {
            fetchData();
        }
    }, [text, navigate]);

    const handleSearch = (event) => {
        event.preventDefault(); // To prevent form submission from reloading the page
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
