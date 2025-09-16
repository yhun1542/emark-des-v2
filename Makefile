.PHONY: install build run clean docker-build docker-run

# Install dependencies
install:
	cd app && npm install
	cd server && pip install -r requirements.txt

# Build frontend
build:
	cd app && npm run build
	mkdir -p server/static
	cp -r app/dist/* server/static/

# Run locally
run: build
	cd server && python app.py

# Clean build files
clean:
	rm -rf app/dist
	rm -rf server/static

# Docker commands
docker-build:
	docker build -t emark-des .

docker-run:
	docker run -p 8000:8000 -e ENABLE_REAL_CALLS=false emark-des

