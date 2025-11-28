import datetime
import time
import random
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Movie:
    id: int
    title: str
    genre: str
    duration: int
    rating: float

@dataclass
class Screening:
    id: int
    movie_id: int
    screening_time: datetime.datetime
    hall_number: int
    price: float
    available_seats: int

@dataclass
class Ticket:
    id: int
    screening_id: int
    customer_name: str
    customer_email: str
    seat_number: int
    purchase_time: datetime.datetime
    total_price: float

class CinemaTicketSystemExperiment:
    def __init__(self):
        self.movies: List[Movie] = []
        self.screenings: List[Screening] = []
        self.tickets: List[Ticket] = []
        self.next_movie_id = 1
        self.next_screening_id = 1
        self.next_ticket_id = 1
        self.init_sample_data()
    
    def init_sample_data(self):
        """Инициализация тестовых данных"""
        # Создание фильмов
        movies_data = [
            ('Аватар: Путь воды', 'Фантастика', 192, 8.1),
            ('Оппенгеймер', 'Драма', 180, 8.8),
            ('Барби', 'Комедия', 114, 7.5),
            ('Джон Уик 4', 'Боевик', 169, 8.2),
            ('Человек-паук: Паутина вселенных', 'Мультфильм', 140, 9.0)
        ]
        
        for title, genre, duration, rating in movies_data:
            self.movies.append(Movie(self.next_movie_id, title, genre, duration, rating))
            self.next_movie_id += 1
        
        # Создание сеансов
        base_time = datetime.datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        for movie in self.movies:
            for day in range(7):  # На 7 дней вперед
                for time_slot in range(4):  # 4 сеанса в день
                    screening_time = base_time + datetime.timedelta(days=day, hours=time_slot*3)
                    self.screenings.append(Screening(
                        self.next_screening_id,
                        movie.id,
                        screening_time,
                        (movie.id % 3) + 1,
                        350 + (movie.id * 50),
                        100
                    ))
                    self.next_screening_id += 1
    
    def get_available_movies(self) -> List[Movie]:
        """Получить список доступных фильмов"""
        current_time = datetime.datetime.now()
        available_movie_ids = set()
        
        for screening in self.screenings:
            if screening.screening_time > current_time and screening.available_seats > 0:
                available_movie_ids.add(screening.movie_id)
        
        return [movie for movie in self.movies if movie.id in available_movie_ids]
    
    def get_screenings_by_movie(self, movie_id: int) -> List[Screening]:
        """Получить сеансы для конкретного фильма"""
        current_time = datetime.datetime.now()
        return [
            screening for screening in self.screenings 
            if screening.movie_id == movie_id 
            and screening.screening_time > current_time
            and screening.available_seats > 0
        ]
    
    def purchase_ticket(self, screening_id: int, customer_name: str, customer_email: str, seat_count: int = 1) -> bool:
        """Покупка билетов"""
        # Находим сеанс
        screening = None
        for s in self.screenings:
            if s.id == screening_id:
                screening = s
                break
        
        if not screening or screening.available_seats < seat_count:
            return False
        
        # Покупка билетов
        for i in range(seat_count):
            ticket = Ticket(
                self.next_ticket_id,
                screening_id,
                customer_name,
                customer_email,
                screening.available_seats - i,
                datetime.datetime.now(),
                screening.price
            )
            self.tickets.append(ticket)
            self.next_ticket_id += 1
        
        # Обновление доступных мест
        screening.available_seats -= seat_count
        return True
    
    def get_ticket_history(self, customer_email: str) -> List[Dict]:
        """Получить историю покупок"""
        customer_tickets = []
        
        for ticket in self.tickets:
            if ticket.customer_email == customer_email:
                # Находим информацию о сеансе и фильме
                screening = next((s for s in self.screenings if s.id == ticket.screening_id), None)
                if screening:
                    movie = next((m for m in self.movies if m.id == screening.movie_id), None)
                    if movie:
                        customer_tickets.append({
                            'ticket_id': ticket.id,
                            'movie_title': movie.title,
                            'screening_time': screening.screening_time,
                            'hall_number': screening.hall_number,
                            'seat_number': ticket.seat_number,
                            'total_price': ticket.total_price,
                            'purchase_time': ticket.purchase_time
                        })
        
        return customer_tickets

def performance_experiment():
    """Вычислительный эксперимент для сравнения производительности"""
    print("=== ВЫЧИСЛИТЕЛЬНЫЙ ЭКСПЕРИМЕНТ ===")
    
    # Создаем систему
    system = CinemaTicketSystemExperiment()
    
    # Тест 1: Поиск доступных фильмов
    print("\n1. Тест поиска доступных фильмов:")
    start_time = time.time()
    for _ in range(1000):
        available_movies = system.get_available_movies()
    end_time = time.time()
    print(f"Время выполнения 1000 поисков: {(end_time - start_time)*1000:.2f} мс")
    
    # Тест 2: Покупка билетов
    print("\n2. Тест покупки билетов:")
    start_time = time.time()
    successful_purchases = 0
    for i in range(100):
        screening_id = random.randint(1, min(50, len(system.screenings)))
        if system.purchase_ticket(screening_id, f"Customer{i}", f"customer{i}@test.com", 1):
            successful_purchases += 1
    end_time = time.time()
    print(f"Успешных покупок: {successful_purchases}/100")
    print(f"Время выполнения 100 покупок: {(end_time - start_time)*1000:.2f} мс")
    
    # Тест 3: Поиск истории покупок
    print("\n3. Тест поиска истории покупок:")
    start_time = time.time()
    for i in range(100):
        history = system.get_ticket_history(f"customer{i}@test.com")
    end_time = time.time()
    print(f"Время выполнения 100 поисков истории: {(end_time - start_time)*1000:.2f} мс")
    
    # Тест 4: Нагрузочное тестирование
    print("\n4. Нагрузочное тестирование (параллельные операции):")
    operations = []
    start_time = time.time()
    
    # Смешанные операции
    for i in range(500):
        # 40% - поиск фильмов, 40% - покупка билетов, 20% - поиск истории
        op_type = random.random()
        if op_type < 0.4:
            system.get_available_movies()
        elif op_type < 0.8:
            screening_id = random.randint(1, min(20, len(system.screenings)))
            system.purchase_ticket(screening_id, f"LoadCustomer{i}", f"load{i}@test.com", 1)
        else:
            system.get_ticket_history(f"customer{random.randint(1, 50)}@test.com")
    
    end_time = time.time()
    print(f"Время выполнения 500 смешанных операций: {(end_time - start_time)*1000:.2f} мс")
    
    # Статистика
    print("\n=== СТАТИСТИКА СИСТЕМЫ ===")
    print(f"Всего фильмов: {len(system.movies)}")
    print(f"Всего сеансов: {len(system.screenings)}")
    print(f"Всего проданных билетов: {len(system.tickets)}")
    
    # Анализ загрузки залов
    hall_utilization = {}
    for screening in system.screenings:
        hall = screening.hall_number
        if hall not in hall_utilization:
            hall_utilization[hall] = {'total_seats': 0, 'sold_seats': 0}
        hall_utilization[hall]['total_seats'] += 100
        hall_utilization[hall]['sold_seats'] += (100 - screening.available_seats)
    
    print("\nЗагрузка залов:")
    for hall, stats in hall_utilization.items():
        utilization = (stats['sold_seats'] / stats['total_seats']) * 100
        print(f"Зал {hall}: {utilization:.1f}%")

def main_experiment():
    """Основная функция для экспериментальной версии"""
    system = CinemaTicketSystemExperiment()
    
    while True:
        print("\n=== ЭКСПЕРИМЕНТАЛЬНАЯ СИСТЕМА ПОКУПКИ БИЛЕТОВ ===")
        print("1. Просмотреть доступные фильмы")
        print("2. Купить билет")
        print("3. История покупок")
        print("4. Запустить вычислительный эксперимент")
        print("5. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            movies = system.get_available_movies()
            print("\nДоступные фильмы:")
            for movie in movies:
                print(f"{movie.id}. {movie.title} ({movie.genre}) - {movie.duration} мин. Рейтинг: {movie.rating}")
                
        elif choice == '2':
            movies = system.get_available_movies()
            if not movies:
                print("Нет доступных фильмов")
                continue
                
            print("\nДоступные фильмы:")
            for movie in movies:
                print(f"{movie.id}. {movie.title}")
            
            try:
                movie_id = int(input("Выберите ID фильма: "))
                screenings = system.get_screenings_by_movie(movie_id)
                
                if not screenings:
                    print("Нет доступных сеансов для этого фильма")
                    continue
                    
                print("\nДоступные сеансы:")
                for screening in screenings:
                    print(f"{screening.id}. {screening.screening_time} - Зал {screening.hall_number} - {screening.price} руб. ({screening.available_seats} мест)")
                
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
            performance_experiment()
            
        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main_experiment()