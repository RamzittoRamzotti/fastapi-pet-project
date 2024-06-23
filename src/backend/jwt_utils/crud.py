import asyncio
import sys

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.backend.schemas import UserSchema
from src.backend.jwt_utils import utils as auth_utils
from src.backend.config import settings
from src.backend.models import User, Book
from sqlalchemy import select, insert

sys.path.append('C:\\Users\\1\\PycharmProjects\\blog_platform\\src\\backend')

engine = create_async_engine(url=settings.db.DB_url, echo=True)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
john = User(
    username='john',
    password=auth_utils.hash_password('qwerty'),
    email='john@mail.ru',
)
sam = User(
    username='sam',
    password=auth_utils.hash_password('password'),
)


async def initial_inserts_users():
    async with async_session() as session:
        async with session.begin():
            session.add_all([john, sam])
            await session.commit()


async def get_user_from_db_by_username(username: str):
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.username == username)
            username_ = await session.execute(query)
            result = username_.scalar_one_or_none()
            return result


async def get_user_from_db_by_email(email: str):
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.email == email)
            email_ = await session.execute(query)
            result = email_.scalar_one_or_none()
            return result


async def insert_new_user(user: User):
    async with async_session() as session:
        async with session.begin():
            query = insert(User).values(username=user.username, email=user.email, password=user.password)
            await session.execute(query)
            await session.commit()


# asyncio.run(initial_inserts())
async def get_admin(user: UserSchema):
    async with async_session() as session:
        async with session.begin():
            query = select(User).where(User.username == user.username)
            await session.execute(query)
            result = await session.scalar_one_or_none()
            if result.is_admin:
                return result


books = [
    Book
        (
        author="Ф. Фитзджерльд Скотт",
        title="Великий Гэтсби",
        title_picture="./pictures/gatsby.jpg",
        description="""Роман американского писателя Фрэнсиса Скотта Фицджеральда; самое знаменитое литературное произведение «века джаза». Роман был начат Фицджеральдом в Нью-Йорке, а закончен в Париже, где он тогда проживал во время своего путешествия по Европе[1]. Опубликован издательством Scribner’s 10 апреля 1925 года.
В центре сюжета — любовная история с детективной и трагической развязкой. Действие развивается недалеко от Нью-Йорка, на «золотом побережье» Лонг-Айленда, среди вилл богачей. В 1920-е годы вслед за хаосом Первой мировой начался экономический бум и американское общество вступило в беспрецедентную полосу процветания. В то же время «сухой закон» сделал многих бутлегеров миллионерами и дал значительный толчок развитию организованной преступности.""",
        user_id=1
    ),
    Book
        (
        author="Джэк Лондон",
        title="Мартин Иден",
        title_picture="./pictures/martin_eden.jpg",
        description="""Роман Джека Лондона. Впервые был напечатан в журнале «The Pacific Monthly[англ.]» в 1908—1909 годах и уже в 1909 году вышел отдельной книгой в издательстве «Макмиллан компани». Действие романа происходит в начале XX века в Окленде (Калифорния, США). Мартин Иден — рабочий парень, моряк, выходец из низов, примерно 21 года от роду, 
        случайно знакомится с Руфью Морз — девушкой из состоятельной буржуазной семьи. Влюбившись в неё с первого взгляда и попав под впечатление от высшего общества, Мартин, желая стать достойным Руфи, активно берётся за самообразование. Руфь, видя в Мартине «дикаря», берёт покровительство над его начинаниями. Мартин узнаёт, что журналы платят приличные гонорары авторам, которые в них печатаются, и твёрдо решает сделать карьеру писателя. К тому же он уверен, что может писать гораздо лучше, чем те, чьи произведения публикуют литературные журналы."""
    ),
    Book
        (
        author="Эрих Мария Ремарк",
        title="На западном фронте без перемен",
        title_picture="./pictures/remark.jpg",
        description="""Hоман Эриха Марии Ремарка, опубликованный в газетном варианте в 1928 году, а отдельной книгой в 1929 году. В предисловии автор говорит: «Эта книга не является ни обвинением, ни исповедью. Это только попытка рассказать о поколении, которое погубила война, о тех, кто стал её жертвой, даже если спасся от снарядов». Название романа — несколько изменённая формулировка из немецких сводок о ходе военных действий на Западном фронте[1].
Ремарк описывает события войны от лица простого солдата. Пауль Боймер, протагонист романа, появляется в самом начале повествования — именно его рассказ вводит читателя в обстоятельства действия. Ремарк делает похожими характеристики Боймера и других персонажей, отмечая их одинаковый возраст, взгляды и т. п. По его собственному выражению, «таким образом он говорил от лица целого поколения».
Описывая ужасы войны, роман Ремарка стоит в остром противоречии с превалировавшей в эпоху Веймарской республики правоконсервативной военной литературой, которая, как правило, старалась оправдать проигранную Германией войну и героизировать её солдат.""",
    ),
]


async def initial_inserts_books():
    async with async_session() as session:
        async with session.begin():
            session.add_all(books)
            await session.commit()


asyncio.run(initial_inserts_books())
