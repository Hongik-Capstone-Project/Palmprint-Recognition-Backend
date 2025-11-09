# FastAPI server run
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker build & run
up:
	docker-compose up --build

# Install dependencies
install:
	pip install -r requirements.txt

uninstall:
	pip uninstall -r requirements.txt -y

# Test
test:
	pytest
