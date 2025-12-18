clientsphere-crm/
├── 📁 src/ # Исходный код приложения
│ ├── 📁 frontend/ # Клиентская часть
│ │ ├── 📁 public/ # Статические файлы
│ │ │ ├── index.html # Главная HTML страница
│ │ │ ├── favicon.ico # Иконка сайта
│ │ │ └── robots.txt # Файл для поисковых систем
│ │ │
│ │ ├── 📁 src/ # Исходный код React приложения
│ │ │ ├── 📁 components/ # React компоненты
│ │ │ │ ├── 📁 common/ # Общие компоненты
│ │ │ │ │ ├── Header/
│ │ │ │ │ ├── Sidebar/
│ │ │ │ │ ├── Footer/
│ │ │ │ │ └── Modal/
│ │ │ │ │
│ │ │ │ ├── 📁 clients/ # Компоненты модуля клиентов
│ │ │ │ │ ├── ClientList/
│ │ │ │ │ ├── ClientForm/
│ │ │ │ │ └── ClientCard/
│ │ │ │ │
│ │ │ │ ├── 📁 deals/ # Компоненты модуля сделок
│ │ │ │ ├── 📁 tasks/ # Компоненты модуля задач
│ │ │ │ ├── 📁 analytics/ # Компоненты аналитики
│ │ │ │ └── 📁 calendar/ # Компоненты календаря
│ │ │ │
│ │ │ ├── 📁 pages/ # Страницы приложения
│ │ │ │ ├── Dashboard.jsx # Главная панель
│ │ │ │ ├── Clients.jsx # Страница клиентов
│ │ │ │ ├── Deals.jsx # Страница сделок
│ │ │ │ ├── Tasks.jsx # Страница задач
│ │ │ │ ├── Analytics.jsx # Страница аналитики
│ │ │ │ └── Settings.jsx # Настройки системы
│ │ │ │
│ │ │ ├── 📁 services/ # Сервисы и API вызовы
│ │ │ │ ├── api.js # Конфигурация API
│ │ │ │ ├── clientsService.js # Сервис клиентов
│ │ │ │ └── authService.js # Сервис аутентификации
│ │ │ │
│ │ │ ├── 📁 store/ # Управление состоянием (Redux)
│ │ │ │ ├── index.js # Настройка store
│ │ │ │ ├── 📁 slices/ # Redux slices
│ │ │ │ └── 📁 actions/ # Redux actions
│ │ │ │
│ │ │ ├── 📁 utils/ # Вспомогательные функции
│ │ │ │ ├── helpers.js # Общие функции
│ │ │ │ ├── validators.js # Валидаторы форм
│ │ │ │ └── constants.js # Константы приложения
│ │ │ │
│ │ │ ├── 📁 styles/ # Стили приложения
│ │ │ │ ├── main.css # Основные стили
│ │ │ │ ├── variables.css # CSS переменные
│ │ │ │ └── components/ # Стили компонентов
│ │ │ │
│ │ │ ├── App.jsx # Главный компонент
│ │ │ ├── App.css # Стили главного компонента
│ │ │ ├── index.js # Точка входа
│ │ │ └── index.css # Глобальные стили
│ │ │
│ │ ├── package.json # Зависимости фронтенда
│ │ └── README.md # Документация фронтенда
│ │
│ ├── 📁 backend/ # Серверная часть
│ │ ├── 📁 src/ # Исходный код сервера
│ │ │ ├── 📁 controllers/ # Контроллеры
│ │ │ │ ├── authController.js
│ │ │ │ ├── clientController.js
│ │ │ │ ├── dealController.js
│ │ │ │ └── analyticsController.js
│ │ │ │
│ │ │ ├── 📁 models/ # Модели данных
│ │ │ │ ├── User.js
│ │ │ │ ├── Client.js
│ │ │ │ ├── Deal.js
│ │ │ │ └── Task.js
│ │ │ │
│ │ │ ├── 📁 routes/ # Маршруты API
│ │ │ │ ├── authRoutes.js
│ │ │ │ ├── clientRoutes.js
│ │ │ │ ├── dealRoutes.js
│ │ │ │ └── index.js
│ │ │ │
│ │ │ ├── 📁 middleware/ # Промежуточное ПО
│ │ │ │ ├── auth.js # Аутентификация
│ │ │ │ ├── validation.js # Валидация данных
│ │ │ │ └── errorHandler.js # Обработка ошибок
│ │ │ │
│ │ │ ├── 📁 config/ # Конфигурационные файлы
│ │ │ │ ├── database.js # Настройка БД
│ │ │ │ ├── jwt.js # Настройка JWT
│ │ │ │ └── server.js # Настройка сервера
│ │ │ │
│ │ │ ├── 📁 utils/ # Вспомогательные функции
│ │ │ │ ├── logger.js # Логирование
│ │ │ │ ├── emailService.js # Сервис отправки email
│ │ │ │ └── exportUtils.js # Экспорт данных
│ │ │ │
│ │ │ ├── app.js # Приложение Express
│ │ │ ├── server.js # Запуск сервера
│ │ │ └── .env.example # Пример переменных окружения
│ │ │
│ │ ├── package.json # Зависимости бэкенда
│ │ └── README.md # Документация бэкенда
│ │
│ ├── 📁 database/ # Скрипты и миграции БД
│ │ ├── 📁 migrations/ # Миграции базы данных
│ │ ├── 📁 seeds/ # Начальные данные
│ │ ├── schema.sql # Схема базы данных
│ │ └── init.sql # Инициализация БД
│ │
│ └── 📁 docker/ # Docker конфигурации
│ ├── docker-compose.yml # Docker Compose конфигурация
│ ├── Dockerfile.frontend # Dockerfile для фронтенда
│ └── Dockerfile.backend # Dockerfile для бэкенда
│
├── 📁 docs/ # Документация проекта
│ ├── 📁 api/ # Документация API
│ │ ├── endpoints.md # Описание эндпоинтов
│ │ └── examples/ # Примеры запросов
│ │
│ ├── 📁 architecture/ # Архитектурная документация
│ │ ├── system-design.md # Дизайн системы
│ │ ├── database-schema.md # Схема базы данных
│ │ └── api-specification.md # Спецификация API
│ │
│ ├── 📁 user-guide/ # Руководство пользователя
│ │ ├── getting-started.md # Начало работы
│ │ ├── clients-management.md # Управление клиентами
│ │ ├── deals-management.md # Управление сделками
│ │ └── reports-guide.md # Работа с отчетами
│ │
│ ├── 📁 developer-guide/ # Руководство разработчика
│ │ ├── setup-development.md # Настройка среды разработки
│ │ ├── coding-standards.md # Стандарты кодирования
│ │ └── deployment-guide.md # Руководство по развертыванию
│ │
│ └── practice-report.md # Отчет по производственной практике
│
├── 📁 tests/ # Тесты проекта
│ ├── 📁 frontend/ # Тесты фронтенда
│ │ ├── unit/ # Юнит-тесты
│ │ └── integration/ # Интеграционные тесты
│ │
│ ├── 📁 backend/ # Тесты бэкенда
│ │ ├── unit/ # Юнит-тесты
│ │ ├── integration/ # Интеграционные тесты
│ │ └── api/ # API тесты
│ │
│ └── 📁 e2e/ # End-to-end тесты
│
├── 📁 scripts/ # Вспомогательные скрипты
│ ├── setup.sh # Скрипт настройки проекта
│ ├── deploy.sh # Скрипт деплоя
│ ├── backup-db.sh # Скрипт резервного копирования БД
│ └── generate-docs.sh # Генерация документации
│
├── 📁 assets/ # Графические ресурсы
│ ├── 📁 images/ # Изображения
│ │ ├── logo.png # Логотип проекта
│ │ ├── screenshots/ # Скриншоты приложения
│ │ └── diagrams/ # Диаграммы и схемы
│ │
│ ├── 📁 icons/ # Иконки
│ └── 📁 fonts/ # Шрифты
│
├── .gitignore # Исключения для Git
├── .env.example # Пример переменных окружения
├── package.json # Корневые зависимости
├── README.md # Этот файл
├── LICENSE # Лицензия проекта
├── CHANGELOG.md # История изменений
├── CONTRIBUTING.md # Руководство по внесению вклада
└── CODE_OF_CONDUCT.md # Кодекс поведения
