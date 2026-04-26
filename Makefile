# Variables
IMAGE_NAME = app
CONTAINER_NAME = app-container
PYTHON = .venv/bin/python
UV = uv

# Default target — runs when you type just `make`
.DEFAULT_GOAL := help

.PHONY: help install run streamlit docker-build docker-run docker-stop clean

## Show this help message
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^## ' Makefile | sed 's/## /  /'
	@echo "  install        Install all dependencies via uv"
	@echo "  run            Run main.py"
	@echo "  docker-build   Build the Docker image"
	@echo "  docker-run     Build + run the Docker container"
	@echo "  docker-stop    Stop and remove the running container"
	@echo "  clean          Remove cache and build artifacts"

## Install all dependencies via uv
install:
	$(UV) sync

## Run main.py
run:
	$(UV) run python main.py

## Build the Docker image
docker-build:
	docker build -t $(IMAGE_NAME) .

## Build the image and run the container
docker-run: docker-build
	docker run --rm --name $(CONTAINER_NAME) --env-file .env $(IMAGE_NAME)

## Stop and remove the container
docker-stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

## Remove Python cache and build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .venv dist build *.egg-info
