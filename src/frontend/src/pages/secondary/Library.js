import {useNavigate} from "react-router-dom";
import {useEffect, useState} from "react";
import "./books.css"

export function Library() {
    const access_token = localStorage.getItem('access_token');
    let navigate = useNavigate();
    const [totalCount, setCount] = useState(0);
    const [skip, setSkip] = useState(0);
    const [limit, setLimit] = useState(2);
    const [books, setBooks] = useState([]);


    useEffect(() => {
        if (!access_token) {
            return navigate('/auth');
        }
        const getBooks = async (skip, limit) => {
            try {
                let response = await fetch(`http://localhost:5000/books?skip=${skip}&limit=${limit}`, {
                    method: 'GET'
                })
                let res = await response.json()
                if (res.detail) {
                    throw new Error(res.detail);
                } else {
                    setBooks(res['books']);
                    setCount(res['count']);
                }
            } catch (error) {
                console.error(error)
            }
        }
        getBooks(skip, limit);
    }, [skip])
    const handlePrevious = () => {
        setSkip(Math.max(0, skip - limit))
    }
    const handleNext = () => {
        setSkip(skip + limit)
    }
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
                                        <button className="btn btn-dark">Забронировать</button>
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