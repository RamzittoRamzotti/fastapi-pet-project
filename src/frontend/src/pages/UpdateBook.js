import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";

export default function UpdateBookPage() {
    const access_token = localStorage.getItem('access_token');

    let navigate = useNavigate()
    const {book_id} = useParams()
    if (!access_token) {
        navigate('/auth')
    }
    return (
        <main>
            <h2>Изменение книги</h2>
            <UpdateBookPageForm book_id={book_id}/>
        </main>
    )

}

function UpdateBookPageForm({book_id}) {
    const [title, setTitle] = useState('');
    const [author, setAuthor] = useState('');
    const [desc, setDesc] = useState('');
    const [img, setImg] = useState(null);
    let navigate = useNavigate();
    useEffect(() => {
        const zapros = async () => {
            try {
                const response = await fetch(`http://localhost:5000/${book_id}`);

                const data = response.json();
                if (data['detail']) {
                    throw new Error(data['detail'])
                }
                setTitle(data['book']['title']);
                setAuthor(data['book']['author']);
                setDesc(data['book']['desc']);


            } catch (error) {
                console.log(error)
            }
            zapros();
        }
    }, [])
    const access_token = localStorage.getItem('access_token');
    const handleSubmit = async (event) => {
        event.preventDefault()
        const formData = new FormData();
        formData.append('title', title);
        formData.append('author', author);
        formData.append('desc', desc);
        formData.append('img', img);
        const update = async (formData) => {
            try {
                const response = await fetch(`http://localhost:5000/books/update_book/${book_id}`, {
                    method: "PATCH",
                    headers: {
                        'Authorization': `Bearer ${access_token}`,
                    },
                    body: formData
                });
                let data = (await response).status;
                console.log(data);
                if (!data.ok) {
                    throw new Error(data);
                }
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
    )
}