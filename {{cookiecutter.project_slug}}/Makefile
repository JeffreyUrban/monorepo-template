.PHONY: help install test lint format build run dev clean
.DEFAULT_GOAL := help

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	./pants export ::

test: ## Run all tests
	./pants test ::

lint: ## Run linting
	./pants lint ::
	./pants check ::

format: ## Format code
	./pants fmt ::

build: ## Build all packages
	./pants package ::

run: ## Run main service
	./pants run services/main:main

dev: ## Start development environment
	docker-compose up -d

clean: ## Clean build artifacts
	./pants clean-all
	docker-compose down

{% if cookiecutter.ml_framework != "none" -%}
train: ## Train ML models
	./pants run models/main-model:train

serve-model: ## Serve ML models
	./pants run models/main-model:serve
{% endif -%}

deploy: ## Deploy application
	./scripts/deploy.py
