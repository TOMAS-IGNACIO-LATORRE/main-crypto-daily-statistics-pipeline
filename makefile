# Makefile

# Variables
AIRFLOW_UID = $(shell id -u)
IMAGE_AIRFLOW = my-airflow-image

# Create necessary folders and .env file if they do not exist
create_dirs_and_env:
	@if [ ! -d ./dags ] || [ ! -d ./logs ] || [ ! -d ./plugins ] || [ ! -d ./config ]; then \
		echo "Creating necessary folders..."; \
		mkdir -p ./dags ./logs ./plugins ./config; \
	else \
		echo "Folders already exist. Skipping creation."; \
	fi
	@if [ ! -f .env ]; then \
		echo -e "AIRFLOW_UID=$(AIRFLOW_UID)" > .env; \
		echo ".env file created with AIRFLOW_UID=$(AIRFLOW_UID)"; \
	else \
		echo ".env file already exists. Skipping creation."; \
	fi

# Build Airflow image if it doesn't exist
build_airflow_image:
	@if [ -z "$$(docker images -q $(IMAGE_AIRFLOW))" ]; then \
		echo "Building the Airflow image..."; \
		docker build -t $(IMAGE_AIRFLOW) -f Dockerfile .; \
	else \
		echo "Airflow image already exists. Skipping build."; \
	fi

# Bring up services with Docker Compose
docker_up:
	docker compose up

# Main command that runs everything
all: build_airflow_image create_dirs_and_env docker_up