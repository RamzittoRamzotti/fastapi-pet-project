from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.sql.functions import count, func

from src.backend.database import engine
from src.backend.models import Book
from src.backend.schemas import BookSchema

async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

books = [
    Book
        (
        author="Ф. Фитзджерльд Скотт",
        title="Великий Гэтсби",
        title_picture="gatsby.jpg",
        description="""Роман американского писателя Фрэнсиса Скотта Фицджеральда; самое знаменитое литературное произведение «века джаза». Роман был начат Фицджеральдом в Нью-Йорке, а закончен в Париже, где он тогда проживал во время своего путешествия по Европе[1]. Опубликован издательством Scribner’s 10 апреля 1925 года.
В центре сюжета — любовная история с детективной и трагической развязкой. Действие развивается недалеко от Нью-Йорка, на «золотом побережье» Лонг-Айленда, среди вилл богачей. В 1920-е годы вслед за хаосом Первой мировой начался экономический бум и американское общество вступило в беспрецедентную полосу процветания. В то же время «сухой закон» сделал многих бутлегеров миллионерами и дал значительный толчок развитию организованной преступности.""",
        user_id=1
    ),
    Book
        (
        author="Джэк Лондон",
        title="Мартин Иден",
        title_picture="martin_eden.jpg",
        description="""Роман Джека Лондона. Впервые был напечатан в журнале «The Pacific Monthly[англ.]» в 1908—1909 годах и уже в 1909 году вышел отдельной книгой в издательстве «Макмиллан компани». Действие романа происходит в начале XX века в Окленде (Калифорния, США). Мартин Иден — рабочий парень, моряк, выходец из низов, примерно 21 года от роду, 
        случайно знакомится с Руфью Морз — девушкой из состоятельной буржуазной семьи. Влюбившись в неё с первого взгляда и попав под впечатление от высшего общества, Мартин, желая стать достойным Руфи, активно берётся за самообразование. Руфь, видя в Мартине «дикаря», берёт покровительство над его начинаниями. Мартин узнаёт, что журналы платят приличные гонорары авторам, которые в них печатаются, и твёрдо решает сделать карьеру писателя. К тому же он уверен, что может писать гораздо лучше, чем те, чьи произведения публикуют литературные журналы."""
    ),
    Book
        (
        author="Эрих Мария Ремарк",
        title="На западном фронте без перемен",
        title_picture="remark.jpg",
        description="""Роман Эриха Марии Ремарка, опубликованный в газетном варианте в 1928 году, а отдельной книгой в 1929 году. В предисловии автор говорит: «Эта книга не является ни обвинением, ни исповедью. Это только попытка рассказать о поколении, которое погубила война, о тех, кто стал её жертвой, даже если спасся от снарядов». Название романа — несколько изменённая формулировка из немецких сводок о ходе военных действий на Западном фронте[1].
Ремарк описывает события войны от лица простого солдата. Пауль Боймер, протагонист романа, появляется в самом начале повествования — именно его рассказ вводит читателя в обстоятельства действия. Ремарк делает похожими характеристики Боймера и других персонажей, отмечая их одинаковый возраст, взгляды и т. п. По его собственному выражению, «таким образом он говорил от лица целого поколения».
Описывая ужасы войны, роман Ремарка стоит в остром противоречии с превалировавшей в эпоху Веймарской республики правоконсервативной военной литературой, которая, как правило, старалась оправдать проигранную Германией войну и героизировать её солдат.""",
    ),
]


async def initial_inserts_books():
    async with async_session() as session:
        async with session.begin():
            session.add_all(books)
            await session.commit()


async def count_books():
    async with async_session() as session:
        async with session.begin():
            query = select(func.count(Book.id))
            result = await session.execute(query)
            return result.scalar_one_or_none()


async def get_all_books(skip: int, limit: int):
    async with async_session() as session:
        async with session.begin():
            query = select(Book).offset(skip).limit(limit)
            result = await session.execute(query)
            books = result.scalars().all()
            count = await count_books()
            return {
                "books": books,
                "count": count,
            }


async def add_book_db(book: BookSchema):
    async with async_session() as session:
        async with session.begin():
            books = Book(**book.dict())
            session.add(books)
            await session.commit()
            return True


async def delete_book_db(book_id: int):
    async with async_session() as session:
        async with session.begin():
            query = select(Book).where(Book.id == book_id)
            result = await session.execute(query)
            book = result.scalar_one_or_none()
            if book:
                await session.delete(book)
                await session.commit()
                return True
            else:
                return False


async def get_book_by_id(book_id: int):
    async with async_session() as session:
        async with session.begin():
            query = select(Book).where(Book.id == book_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()


async def update_book_db(book: Book):
    async with async_session() as session:
        async with session.begin():
            query = update(Book).where(Book.id == book.id).values(**book.as_dict())
            result = await session.execute(query)
            await session.commit()
            return True


async def search_book_db(text: str):
    async with async_session() as session:
        async with session.begin():
            query = select(Book).where(Book.title.ilike("%" + text + "%") | Book.author.ilike("%" + text + "%"))
            result = await session.execute(query)
            return result.scalars().all()
