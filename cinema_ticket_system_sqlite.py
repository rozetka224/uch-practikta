import sqlite3
import datetime
from typing import List, Dict, Optional

class CinemaTicketSystemSQLite:
    def __init__(self, db_name: str = "cinema.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Создание таблиц
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                duration INTEGER NOT NULL,
                rating REAL NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS screenings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL,
                screening_time DATETIME NOT NULL,
                hall_number INTEGER NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                available_seats INTEGER NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                screening_id INTEGER NOT NULL,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                seat_number INTEGER NOT NULL,
                purchase_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_price DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (screening_id) REFERENCES screenings (id)
            )
        ''')
        
        # Добавление тестовых данных
        self.add_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def add_sample_data(self, cursor):
        """Добавление тестовых данных"""
        # Фильмы
        movies = [
            ('Аватар: Путь воды', 'Фантастика', 192, 8.1),
            ('Оппенгеймер', 'Драма', 180, 8.8),
            ('Барби', 'Комедия', 114, 7.5),
            ('Джон Уик 4', 'Боевик', 169, 8.2),
            ('Человек-паук: Паутина вселенных', 'Мультфильм', 140, 9.0)
        ]
        
        cursor.executemany(
            'INSERT OR IGNORE INTO movies (title, genre, duration, rating) VALUES (?, ?, ?, ?)',
            movies
        )
        
        # Сеансы
        screening_times = []
        base_time = datetime.datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        for movie_id in range(1, 6):
            for day in range(7):  # На 7 дней вперед
                for time_slot in range(4):  # 4 сеанса в день
                    screening_time = base_time + datetime.timedelta(days=day, hours=time_slot*3)
                    screening_times.append((
                        movie_id,
                        screening_time,
                        (movie_id % 3) + 1,  # Залы 1-3
                        350 + (movie_id * 50),  # Цена
                        100  # Доступные места
                    ))
        
        cursor.executemany(
            'INSERT OR IGNORE INTO screenings (movie_id, screening_time, hall_number, price, available_seats) VALUES (?, ?, ?, ?, ?)',
            screening_times
        )
    
    def get_available_movies(self) -> List[Dict]:
        """Получить список доступных фильмов"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT m.id, m.title, m.genre, m.duration, m.rating 
            FROM movies m 
            JOIN screenings s ON m.id = s.movie_id 
            WHERE s.screening_time > datetime('now')
            ORDER BY m.rating DESC
        ''')
        
        movies = []
        for row in cursor.fetchall():
            movies.append({
                'id': row[0],
                'title': row[1],
                'genre': row[2],
                'duration': row[3],
                'rating': row[4]
            })
        
        conn.close()
        return movies
    
    def get_screenings_by_movie(self, movie_id: int) -> List[Dict]:
        """Получить сеансы для конкретного фильма"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.screening_time, s.hall_number, s.price, s.available_seats
            FROM screenings s
            WHERE s.movie_id = ? AND s.screening_time > datetime('now')
            ORDER BY s.screening_time
        ''', (movie_id,))
        
        screenings = []
        for row in cursor.fetchall():
            screenings.append({
                'id': row[0],
                'screening_time': row[1],
                'hall_number': row[2],
                'price': row[3],
                'available_seats': row[4]
            })
        
        conn.close()
        return screenings
    
    def purchase_ticket(self, screening_id: int, customer_name: str, customer_email: str, seat_count: int = 1) -> bool:
        """Покупка билетов"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Проверка доступности мест
            cursor.execute('SELECT available_seats, price FROM screenings WHERE id = ?', (screening_id,))
            result = cursor.fetchone()
            
            if not result or result[0] < seat_count:
                return False
            
            available_seats, price = result
            
            # Покупка билетов
            for seat in range(1, seat_count + 1):
                cursor.execute('''
                    INSERT INTO tickets (screening_id, customer_name, customer_email, seat_number, total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (screening_id, customer_name, customer_email, available_seats - seat + 1, price))
            
            # Обновление доступных мест
            cursor.execute('''
                UPDATE screenings 
                SET available_seats = available_seats - ? 
                WHERE id = ?
            ''', (seat_count, screening_id))
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при покупке билета: {e}")
            return False
        finally:
            conn.close()
    
    def get_ticket_history(self, customer_email: str) -> List[Dict]:
        """Получить историю покупок"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, m.title, s.screening_time, s.hall_number, t.seat_number, t.total_price, t.purchase_time
            FROM tickets t
            JOIN screenings s ON t.screening_id = s.id
            JOIN movies m ON s.movie_id = m.id
            WHERE t.customer_email = ?
            ORDER BY t.purchase_time DESC
        ''', (customer_email,))
        
        tickets = []
        for row in cursor.fetchall():
            tickets.append({
                'ticket_id': row[0],
                'movie_title': row[1],
                'screening_time': row[2],
                'hall_number': row[3],
                'seat_number': row[4],
                'total_price': row[5],
                'purchase_time': row[6]
            })
        
        conn.close()
        return tickets

def main_sqlite():
    """Основная функция для SQLite версии"""
    system = CinemaTicketSystemSQLite()
    
    while True:
        print("\n=== СИСТЕМА ПОКУПКИ БИЛЕТОВ В КИНО ===")
        print("1. Просмотреть доступные фильмы")
        print("2. Купить билет")
        print("3. История покупок")
        print("4. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            movies = system.get_available_movies()
            print("\nДоступные фильмы:")
            for movie in movies:
                print(f"{movie['id']}. {movie['title']} ({movie['genre']}) - {movie['duration']} мин. Рейтинг: {movie['rating']}")
                
        elif choice == '2':
            movies = system.get_available_movies()
            if not movies:
                print("Нет доступных фильмов")
                continue
                
            print("\nДоступные фильмы:")
            for movie in movies:
                print(f"{movie['id']}. {movie['title']}")
            
            try:
                movie_id = int(input("Выберите ID фильма: "))
                screenings = system.get_screenings_by_movie(movie_id)
                
                if not screenings:
                    print("Нет доступных сеансов для этого фильма")
                    continue
                    
                print("\nДоступные сеансы:")
                for screening in screenings:
                    print(f"{screening['id']}. {screening['screening_time']} - Зал {screening['hall_number']} - {screening['price']} руб. ({screening['available_seats']} мест)")
                
                screening_id = int(input("Выберите ID сеанса: "))
                customer_name = input("Ваше имя: ")
                customer_email = input("Ваш email: ")
                seat_count = int(input("Количество билетов: "))
                
                if system.purchase_ticket(screening_id, customer_name, customer_email, seat_count):
                    print("Билеты успешно куплены!")
                else:
                    print("Ошибка при покупке билетов. Возможно, недостаточно мест.")
                    
            except ValueError:
                print("Ошибка ввода данных")
                
        elif choice == '3':
            email = input("Введите email для поиска истории: ")
            tickets = system.get_ticket_history(email)
            
            if not tickets:
                print("История покупок не найдена")
            else:
                print("\nИстория покупок:")
                for ticket in tickets:
                    print(f"Билет {ticket['ticket_id']}: {ticket['movie_title']} - {ticket['screening_time']} - Место {ticket['seat_number']} - {ticket['total_price']} руб.")
                    
        elif choice == '4':
            print("До свидания!")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main_sqlite()