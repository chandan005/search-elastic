.PHONY: install run-dev docker-build docker-run-dev docker-run-prod clean docker-compose-up docker-compose-down

install:
	pipenv install --dev

# Dev
run-dev:
	ENV=dev pipenv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t abn_search .

docker-run-dev:
	docker run -d --name abn_search -p 8000:8000 -e ENV=dev abn_search

docker-run-prod:
	docker run -d --name abn_search -p 8000:8000 -e ENV=prod abn_search

clean:
	docker rm -f abn_search || true
	docker rmi -f abn_search || true

docker-compose-up:
	docker-compose up --build -d

docker-compose-down:
	docker-compose down
