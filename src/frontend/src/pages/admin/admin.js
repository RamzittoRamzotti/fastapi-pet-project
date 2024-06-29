import {useEffect, useState} from "react";
import "../secondary/books.css"
import "./add-book.css"
import {useNavigate} from "react-router-dom";

export function AdminPage() {
    let navigate = useNavigate();
    const handleDiv = (event) => {
        event.preventDefault();
        return navigate("/add-book");
    }
    const handleFoo = (event) => {
        event.preventDefault();
        return navigate('/update-delete')
    }
    return (
        <main className="main-admin">
            <div className="main-div" onClick={handleDiv}>
                <p>Добавить книгу</p>
            </div>
            <div className="main-div" onClick={handleFoo}>
                <p>Изменить/удалить книгу</p>
            </div>
        </main>
    );
}

function AddBookForm() {
    const access_token = localStorage.getItem('access_token');
    let navigate = useNavigate();
    const [title, setTitle] = useState('');
    const [author, setAuthor] = useState('');
    const [desc, setDesc] = useState('');
    const [img, setImg] = useState(null);
    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('title', title);
        formData.append('author', author);
        formData.append('desc', desc);
        formData.append('img', img);
        const handleForm = async (formData) => {
            try {
                console.log(formData['title'])

                const response = fetch("http://localhost:5000/api/books/add_book", {
                    method: "POST",
                    headers: {
                        'Authorization': `Bearer ${access_token}`,
                    },
                    body: formData
                })
                let data = (await response).status;
                console.log(data);
                if (!data.ok) {
                    throw new Error(data);
                }
                return navigate("/admin");
            } catch (error) {
                alert(error);
            }
        }
        await handleForm(formData);
    }

    return (
        <form className="loginForm" onSubmit={handleSubmit} encType="multipart/form-data">
            <div className="input-div">
                <label htmlFor="title">Название книги:</label>
                <input
                    type="text"
                    id="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                />
            </div>
            <div className="input-div">
                <label htmlFor="author">Автор:</label>
                <input
                    type="text"
                    id="author"
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                    required
                />
            </div>
            <div className="input-div">
                <label htmlFor="desc">Описание:</label>
                <textarea
                    id="desc"
                    value={desc}
                    onChange={(e) => setDesc(e.target.value)}
                    required
                />
            </div>
            <div className="input-div">
                <label htmlFor="img">Изображение:</label>
                <input
                    type="file"
                    id="img"
                    onChange={(e) => setImg(e.target.files[0])}
                    required
                />
            </div>
            <div className="input-div">
                <p onClick={handleSubmit} className="btn btn-success btns">Submit</p>
            </div>
        </form>
    );
}

export function AddBookPage() {
    const access_token = localStorage.getItem('access_token');
    let navigate = useNavigate();
    useEffect(() => {
        if (!access_token) {
            return navigate('/auth')
        }
    }, [access_token, navigate])


    return (
        <main className="main-add-book">
            <div className="main-div-form">
                <h2>Добавление книги</h2>
                <AddBookForm/>
            </div>
        </main>
    );
}