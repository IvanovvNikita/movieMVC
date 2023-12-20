Usage
=====

Movie
-----------------------
Представляет информацию о фильме.

.. automodule:: movies

.. autoclass:: movies.Movie 

MovieList
-----------------------
Представляет список фильмов.

.. autoclass:: movies.MovieList 

Application
-----------------------
Управляет графическим интерфейсом curses и создает экземпляры других классов.

.. automodule:: main

.. autoclass:: main.Application

MovieListModel
-----------------------
Хранит список фильмов и выбранный фильм. Предоставляет методы для получения списка фильмов, удаления фильма и переключения на следующий/предыдущий фильм.

.. autoclass:: main.MovieListModel 
   :members:

MovieListView
-----------------------
Отображает список фильмов в окне.

.. autoclass:: main.MovieListView
   :members:

HeaderView
-----------------------
Отображает заголовок приложения в окне.

.. autoclass:: main.HeaderView
   :members:

Controller
-----------------------
Обрабатывает пользовательский ввод и управляет моделью и представлением.

.. autoclass:: main.Controller
   :members:

MovieView
-----------------------
Отображает информацию о выбранном фильме в окне.

.. autoclass:: main.MovieView
   :members: