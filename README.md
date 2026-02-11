# Практическая работа: Backend + Postgres + Redis + Nginx (Docker)

Твоя задача — развернуть простой сервис регистрации и входа в систему, используя контейнеры Docker и связку сервисов:

- Backend (Python / Flask)
- PostgreSQL (основная база данных)
- Redis (хранение сессий / кеш)
- Nginx (reverse proxy)

Проект уже содержит исходный код backend и конфигурацию nginx. 
В конфигурация возможны ошибки так как в сервисе не было девопса и писал джун разраб. 
Твоя задача — правильно собрать инфраструктуру и окружение.

---

## Требования

1. Поднять все сервисы через `docker-compose`:
   - backend
   - postgres
   - redis
   - nginx

2. Backend должен:
   - подключаться к PostgreSQL
   - подключаться к Redis
   - принимать запросы через nginx

3. PostgreSQL должен:
   - использовать volume для хранения данных
   - сохранять данные при перезапуске контейнеров

4. Redis должен быть доступен backend по сети Docker

5. Все секреты и настройки должны передаваться в backend через **переменные окружения (env)**:
   - `POSTGRES_HOST`
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `REDIS_HOST`
   - `REDIS_PORT`

6. Проект должен запускаться одной командой:

```bash
docker-compose up -d