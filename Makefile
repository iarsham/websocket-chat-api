log-back:
	 docker-compose logs -f backend

log-db:
	docker-compose logs -f postgres

build:
	docker-compose up --build -d

check-db:
	docker-compose exec backend alembic current

migrate:
	docker-compose exec backend alembic upgrade head