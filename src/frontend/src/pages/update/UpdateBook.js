import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import "./update-book.css"

export default function UpdateBookPage() {
    const access_token = localStorage.getItem('access_token');

    let navigate = useNavigate()
    const {book_id} = useParams()
    if (!access_token) {
        navigate('/auth')
    }
    return (
        <main className="main-update">
            <div className="main-div-form">
                <h2>Изменение книги</h2>
                <UpdateBookPageForm book_id={book_id}/>
            </div>
        </main>
    )

}

function UpdateBookPageForm({book_id}) {
    const [title, setTitle] = useState('');
    const [author, setAuthor] = useState('');
    const [desc, setDesc] = useState('');
    const [img, setImg] = useState(null);
    let navigate = useNavigate();

    const access_token = localStorage.getItem('access_token');
    const handleSubmit = async (event) => {
        event.preventDefault()
        const formData = new FormData();
        formData.append('title', title);
        formData.append('author', author);
        formData.append('desc', desc);
        if (img) {
            formData.append('img', img); // Убедитесь, что img действительно является объектом File
        } else {
            console.log("No file selected");
        }
        const update = async (formData) => {
            try {
                console.log(formData.get('title'))

                const response = await fetch(`http://backend:5000/books/update_book/${book_id}`, {
                    method: "PATCH",
                    headers: {
                        'Authorization': `Bearer ${access_token}`,
                    },
                    body: formData
                });
                let data = await response.json();
                console.log(data);
                if (data['detail']) {
                    throw new Error(data);
                }
                alert("Книга успешно изменена!");
                return navigate("/admin");
            } catch (error) {
                alert(error);
                return navigate("/admin");
            }
        }
        await update(formData);


    }
    return (
        <form className="loginForm" onSubmit={handleSubmit}>

            <div className="input-div">
                <label htmlFor="title">Название книги:</label>
                <input
                    type="text"
                    id="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
            </div>
            <div className="input-div">
                <label htmlFor="author">Автор:</label>
                <input
                    type="text"
                    id="author"
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                />
            </div>
            <div className="input-div">
                <label htmlFor="desc">Описание:</label>
                <textarea
                    id="desc"
                    value={desc}
                    onChange={(e) => setDesc(e.target.value)}
                />
            </div>
            <div className="input-div">
                <label htmlFor="img">Изображение:</label>
                <input
                    type="file"
                    id="img"
                    onChange={(e) => setImg(e.target.files[0])}
                />
            </div>
            <div className="input-div">
                <p onClick={handleSubmit} className="btn btn-success btns">Submit</p>
            </div>
        </form>
    )
}