from datetime import date
from uuid import UUID, uuid4


class Movie:
    """
    Представляет информацию о фильме.

    Attributes:
        id (UUID): Уникальный идентификатор фильма.
        
        title (str): Название фильма.
        
        description (str): Описание фильма.
        
        genre (str): Жанр фильма.
        
        age_rating (str): Возрастной рейтинг фильма (G, PG, PG-13, R, R-17).
        
        release_date (date): Дата выпуска фильма.
    """

    def __init__(self, title, desc, genre, age, release):
        """
        Инициализирует объект Movie.

        Args:
            title (str): Название фильма.
            
            desc (str): Описание фильма.
            
            genre (str): Жанр фильма.
            
            age (str): Возрастной рейтинг фильма.
            
            release (date): Дата выпуска фильма.
        """
        self.id = uuid4()
        self.title = title
        self.description = desc
        self.genre = genre
        self.age_rating = age
        self.release_date = release


class MovieList:
    """
    Представляет список фильмов.

    Methods:
        default(): Устанавливает список фильмов по умолчанию.
        
        create(title, desc, genre, age, release) -> UUID: Создает новый фильм и добавляет его в список.
        
        delete(id: UUID): Удаляет фильм из списка по заданному идентификатору.
        
        get_all() -> list: Возвращает список всех фильмов.
        
        get_by_title(title) -> Movie: Возвращает фильм с заданным названием.
        
        recommend(age, genre=None) -> Movie: Рекомендует фильм на основе возраста и жанра.
    """

    def __init__(self):
        """
        Инициализирует объект MovieList.
        """
        self.movies = []

    def default(self):
        """
        Устанавливает список фильмов по умолчанию.

        Returns:
            MovieList: Ссылка на текущий объект MovieList.
        """
        self.movies = default_movies
        return self

    def create(self, title, desc, genre, age, release) -> UUID:
        """
        Создает новый фильм и добавляет его в список фильмов.

        Args:
            title (str): Название фильма.
            
            desc (str): Описание фильма.
            
            genre (str): Жанр фильма.
            
            age (str): Возрастной рейтинг фильма.
            
            release (date): Дата выпуска фильма.

        Returns:
            UUID: Идентификатор созданного фильма.

        Raises:
            Exception: Если фильм с таким названием и датой выпуска уже существует.
        """
        for m in self.movies:
            if m.title == title and m.release_date == release:
                raise Exception("Такой фильм уже существует!")

        movie = Movie(title, desc, genre, age, release)
        self.movies.append(movie)

        return movie.id

    def delete(self, id: UUID):
        """
        Удаляет фильм из списка по заданному идентификатору.

        Args:
            id (UUID): Идентификатор фильма.

        Raises:
            Exception: Если фильм с заданным идентификатором не существует.
        """
        idx = -1
        for i, movie in enumerate(self.movies):
            if movie.id == id:
                idx = i

        if idx == -1:
            raise Exception("Такого фильма не существует!")
        else:
            del self.movies[idx]


# Спасибо ChatGPT
default_movies = [
    Movie(
        title="Похождения Потерянного Сокровища",
        desc=
        "Группа молодых исследователей отправляется в поисках давно забытого сокровища, спрятанного глубоко в неизведанной джунгли.",
        genre="Приключения",
        age="PG",
        release=date(2022, 7, 15)),
    Movie(
        title="Загадка Кодов Энигмы",
        desc=
        "Гениальный математик присоединяется к команде кодовых разгадчиков во время Второй мировой войны, чтобы расшифровать таинственный код Энигмы, используемый вражескими силами.",
        genre="Драма",
        age="PG-13",
        release=date(2021, 11, 28)),
    Movie(
        title="Загадочный Особняк",
        desc=
        "Группа друзей проводит ночь в загадочном особняке, не подозревая о темных секретах и сверхъестественных сущностях, скрывающихся в его стенах.",
        genre="Ужасы",
        age="R",
        release=date(2023, 10, 31)),
    Movie(
        title="Дилемма Путешественника Во Времени",
        desc=
        "Гениальный ученый изобретает машину времени и вынужден разбираться с этическими и моральными последствиями изменения прошлого в попытке спасти будущее.",
        genre="Научная фантастика",
        age="PG-13",
        release=date(2024, 3, 12)),
    Movie(
        title="Тайный Агент",
        desc=
        "Шпион, работающий под прикрытием, должен предотвратить катастрофическую террористическую атаку, столкнувшись с предательством и борьбой со временем.",
        genre="Триллер",
        age="R-17",
        release=date(2022, 9, 2))
]
