import curses

from movies import MovieList


class Application:

    """
    Класс приложения, управляющий моделями, представлениями и контроллерами.

    Атрибуты:
        window (curses.window): Окно приложения.
        
        moviesModel (MovieListModel): Модель списка фильмов.
        
        header (HeaderView): Представление заголовка приложения.
        
        main_window (MovieListView): Представление списка фильмов.
        
        side_menu (MovieView): Представление выбранного фильма в боковом меню.
        
        side_menu_controller (Controller): Контроллер для бокового меню.

    Методы:
        __init__(self, window): Инициализация приложения.
        
        refresh(self): Обновление всех представлений приложения.
        
        run(self): Запуск приложения.
    """
    
    def __init__(self, window):
        screen_width = curses.COLS - 1
        screen_height = curses.LINES - 1

        self.window = window

        # Models
        movies = MovieList().default()
        self.moviesModel = MovieListModel(movies)

        # Views
        self.header = HeaderView("Movies")
        self.header.init_window(window, 1, screen_width, 0, 0)

        self.main_window = MovieListView(self.moviesModel)
        self.main_window.init_window(window, screen_height, screen_width - 40,
                                     1, 0)

        self.side_menu = MovieView(self.moviesModel)
        self.side_menu.init_window(window, screen_height, 40, 1,
                                   screen_width - 40)

        # Controller
        self.side_menu_controller = Controller(window, self.moviesModel, self)

    def refresh(self):
        """
        Обновление всех представлений приложения.
        """
        self.window.touchwin()
        self.header.refresh()
        self.side_menu.refresh()
        self.main_window.refresh()

    def run(self):
        """
        Запуск приложения.
        """
        self.side_menu_controller.run()


class MovieListModel:

    """
    Модель списка фильмов.

    Атрибуты:
        _movies (MovieList): Список фильмов.
        
        selected (int): Индекс выбранного фильма.

    Методы:
        __init__(self, movies): Инициализация модели.
        
        get_movies(self): Получение всех фильмов.
        
        delete_item(self): Удаление выбранного фильма.
        
        next_item(self): Выбор следующего фильма в списке.
        
        prev_item(self): Выбор предыдущего фильма в списке.
    """

    def __init__(self, movies: MovieList):

        self._movies = movies
        self.selected = None

    def get_movies(self):

        return self._movies.get_all()

    def delete_item(self):

        if self.selected is None:
            return

        id = self.get_movies()[self.selected].id
        self._movies.delete(id)
        self.selected = None

    def next_item(self):

        movies_len = len(self.get_movies())
        if movies_len == 0:
            return
        elif self.selected is None:
            self.selected = 0
        elif self.selected < movies_len - 1:
            self.selected += 1

    def prev_item(self):
        movies_len = len(self.get_movies())
        if movies_len == 0:
            return
        if self.selected is None:
            self.selected = 0
        elif self.selected > 0:
            self.selected -= 1


class MovieView:

    """
    Представление выбранного фильма.

    Атрибуты:
        model (MovieListModel): Модель списка фильмов.
        
        window (curses.window): Окно представления фильма.
        
        movie (Movie): Выбранный фильм для отображения.

    Методы:
        __init__(self, model): Инициализация представления фильма.
        
        refresh(self): Обновление представления фильма.
        
        movie_view(self): Отображение информации о фильме.
    """
    
    def __init__(self, model):
        self.model = model
        self.window = None
        self.movie = None

    def init_window(self, window, height, width, begin_y, begin_x):
        self.window = window.subwin(height, width, begin_y, begin_x)
        self.height = height
        self.width = width

    def refresh(self):
        self.window.clear()
        self.window.border()

        if self.model.selected != None:
            self.movie = self.model.get_movies()[self.model.selected]
            self.movie_view()

        self.window.refresh()

    def movie_view(self):
        poster_height = 10
        for i in range(1, poster_height):
            if i == int(poster_height / 2):
                s = "#" * 3 + ' POSTER ' + '#' * 3
            else:
                s = "#" * 14
            self.window.addstr(i, int(self.width / 2) - 7, s, curses.A_DIM)

        self.window.addstr(12, 2, "Title", curses.A_BOLD)
        self.window.addstr(13, 2, self.movie.title)
        self.window.addstr(14, 2, "Genre", curses.A_BOLD)
        self.window.addstr(15, 2, self.movie.genre)
        self.window.addstr(16, 2, "Release Date", curses.A_BOLD)
        self.window.addstr(17, 2, str(self.movie.release_date))
        self.window.addstr(18, 2, "Age Rating", curses.A_BOLD)
        self.window.addstr(19, 2, self.movie.age_rating)
        self.window.addstr(20, 2, "Description", curses.A_BOLD)

        # Разбиваем описание на чанки
        chunks, chunk_size = len(self.movie.description), self.width - 4
        desc_chunks = [
            self.movie.description[i:i + chunk_size]
            for i in range(0, chunks, chunk_size)
        ]
        cursor_y = 21
        for a in desc_chunks:
            self.window.addstr(cursor_y, 2, a)
            cursor_y += 1


class MovieListView:
    def __init__(self, model):
        self.model = model
        self.window = None
        self.col_widths = [50]  #[50, 20, 20]

    def init_window(self, window, height, width, begin_y, begin_x):
        self.window = window.subwin(height, width, begin_y, begin_x)
        self.height = height

    def refresh(self):
        self.window.clear()

        header = self.format_row("Title", 'Genre', 'Premier')
        self.window.addstr(1, 2, header, curses.A_BOLD)

        offset_y = 2

        for idx, movie in enumerate(self.model.get_movies()):
            if idx + offset_y >= self.height - 1:
                break

            s = self.format_row(movie.title, movie.genre, movie.release_date)
            if idx == self.model.selected:
                self.window.addstr(idx + offset_y, 2, s, curses.A_BOLD)
            else:
                self.window.addstr(idx + offset_y, 2, s)

        self.window.refresh()

    def format_row(self, *items):
        s = ''
        for idx, item in enumerate(items):
            if idx > len(self.col_widths) - 1:
                break
            whitespace = " " * (self.col_widths[idx] - len(str(item)))
            s += str(item) + whitespace
        return s + '\n'


class HeaderView:
    """
    Представление заголовка.

    Атрибуты:
        title (str): Заголовок представления.
        
        window (curses.window): Окно представления заголовка.
        
        center (int): Координата X для выравнивания заголовка по центру.

    Методы:
        __init__(self, title): Инициализация представления заголовка.
        
        init_window(self, window, height, width, begin_y, begin_x): Инициализация окна представления заголовка.
        
        refresh(self): Обновление представления заголовка.
    """
    def __init__(self, title):
        self.title = title
        self.window = None
        self.center = None

    def init_window(self, window, height, width, begin_y, begin_x):
        self.window = window.subwin(height, width, begin_y, begin_x)
        self.center = int((curses.COLS - 1) / 2 - int(len(self.title) / 2))

    def refresh(self):
        self.window.clear()
        self.window.addstr(0, self.center, self.title)
        self.window.refresh()


class Controller:
    """
    Контроллер для управления представлением и моделью.

    Атрибуты:
        window (curses.window): Окно приложения.
        
        model (MovieListModel): Модель списка фильмов.
        
        view: Представление списка фильмов.

    Методы:
        __init__(self, window, model, view): Инициализация контроллера.
        
        run(self): Запуск основного цикла контроллера.
    """
    def __init__(self, window, model, view):
        self.window = window
        self.model = model
        self.view = view

    def run(self):
        while True:
            c = self.window.getch()
            if c == ord('q'):
                break
            elif c == curses.KEY_DOWN or c == ord('j'):
                self.model.next_item()
            elif c == curses.KEY_UP or c == ord('k'):
                self.model.prev_item()
            elif c == curses.KEY_BACKSPACE or c == ord('d'):
                self.model.delete_item()

            self.view.refresh()


if __name__ == '__main__':
    window = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    window.keypad(True)

    try:
        view = Application(window)
        view.refresh()
        view.run()
    except Exception as e:
        print(e)
    finally:
        curses.endwin()
