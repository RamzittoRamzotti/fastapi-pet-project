import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import "./books.css";
import {RefreshToken} from "../Login";

export function Library() {
    const [access_token, setAccessToken] = useState(localStorage.getItem('access_token'));
    let navigate = useNavigate();
    const [totalCount, setCount] = useState(0);
    const [skip, setSkip] = useState(0);
    const [limit, setLimit] = useState(2);
    const [books, setBooks] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!localStorage.getItem('access_token')) {
            navigate('/auth');
        } else {
            fetchBooks();
        }
    }, [skip, access_token]);

    const fetchBooks = async () => {
        try {
            const response = await fetch(`http://localhost:5000/books?skip=${skip}&limit=${limit}`, {
                headers: {'Authorization': `Bearer ${access_token}`},
                method: 'GET'
            });
            const res = await response.json();
            if (res['detail']) {
                throw new Error(res.detail || 'Error fetching books');
            }
            setBooks(res['books']);
            setCount(res['count']);
        } catch (error) {
            console.error('Fetch error:', error);
            setError(error.message);
        }
    };

    const handlePrevious = () => setSkip(Math.max(0, skip - limit));
    const handleNext = () => setSkip(skip + limit);
    const handleClick = async (book_id) => {
        const access_tokens = await Auth(access_token, setAccessToken, navigate, setError);
        setAccessToken(access_tokens)
        if (!access_token) {
            console.error('Failed to authenticate or refresh token.');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/login/users/id/', {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${access_tokens}`,
                    'Accept': 'application/json'
                }
            });
            const users = await response.json();
            if (!users['user_id']) {
                throw new Error("Failed to fetch user data.");
            }

            const user_id = users['user_id'];
            const formData = new FormData();
            formData.append("user_id", user_id);

            const response_ = await fetch(`http://localhost:5000/books/update_book/${book_id}`, {
                method: "PATCH",
                headers: {
                    'Authorization': `Bearer ${access_tokens}`,
                },
                body: formData
            });

            const data = await response_.json();
            if (!data['result']) {
                alert("Не удалось забронировать книгу!");
            } else {
                alert("Книга успешно забронирована!");
                setBooks(currentBooks => currentBooks.map(book => {
                    if (book.id === book_id) {
                        return {...book, user_id: user_id};
                    }
                    return book;
                }));
            }
            return navigate('/library')

        } catch (error) {
            console.error('Error booking the book:', error);
            alert("An error occurred while booking the book.");
        }
    };
    return (
        <main>
            <h1>Book List</h1>
            {(typeof books == 'undefined') ? <p>Loading...</p> : (
                <div className="book-div">
                    {books.map((book) => (
                            <ul className="ul-align">
                                <img src={`http://localhost:5000/images/${book.title_picture}`} alt={book['title']}
                                     className="book-image"/>
                                <li key={book['id']}>Название книги: {book['title']}</li>
                                <li>Автор: {book['author']}</li>
                                <li><p>{book['description']}</p></li>
                                {book.user_id === null ? (
                                    <li>
                                        <button className="btn btn-dark"
                                                onClick={() => handleClick(book['id'])}>Забронировать
                                        </button>
                                    </li>
                                ) : null}

                            </ul>
                        )
                    )
                    }
                </div>
            )}
            <div className="buttons-div">
                <button onClick={handlePrevious} disabled={skip === 0}>Previous</button>
                <button onClick={handleNext} disabled={skip + limit >= totalCount}>Next</button>
            </div>
        </main>
    );

}

async function Auth(access_token, setAccessToken, navigate, setError) {


    if (localStorage.length === 0) {
        return navigate('/auth')
    }

    try {
        const response = await fetch('http://localhost:5000/login/users/me/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${access_token}`,
            }
        });

        const data = await response.json();
        if (data.detail) {
            console.log("Session needs refresh");
            return await RefreshToken(navigate, setError, setAccessToken);
        } else {
            console.log("Auth success: ", data);
            return access_token;
        }
    } catch (error) {
        console.error('Auth error:', error);
        setError(error.message);
    }
}