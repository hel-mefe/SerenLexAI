# SerenLexAI Infrastructure Control

.DEFAULT_GOAL := help

PROJECT_NAME := SerenLexAI
COMPOSE := docker compose -f infrastructure/docker-compose.yml

GREEN := \033[0;32m
CYAN := \033[0;36m
YELLOW := \033[1;33m
NC := \033[0m

help:
	@echo ""
	@echo "$(CYAN)=========================================================="
	@echo " $(PROJECT_NAME) Developer Command Center"
	@echo "==========================================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Infrastructure$(NC)"
	@echo "  make up              Start all services"
	@echo "  make down            Stop all services"
	@echo "  make rebuild         Rebuild containers"
	@echo "  make logs            Tail all logs"
	@echo ""
	@echo "$(YELLOW)Database$(NC)"
	@echo "  make migrate         Run alembic migrations"
	@echo "  make seed            Seed the database"
	@echo "  make reset-db        ⚠️  Destroy & recreate database"
	@echo ""
	@echo "$(YELLOW)Worker$(NC)"
	@echo "  make worker          Run celery worker manually"
	@echo ""
	@echo "$(YELLOW)Utility$(NC)"
	@echo "  make shell           Open API container shell"
	@echo "  make clean           Remove volumes & containers"
	@echo ""
	@echo "$(CYAN)==========================================================$(NC)"
	@echo ""

up:
	@echo "$(GREEN)Starting $(PROJECT_NAME)...$(NC)"
	$(COMPOSE) up -d

down:
	@echo "$(GREEN)Stopping $(PROJECT_NAME)...$(NC)"
	$(COMPOSE) down

rebuild:
	@echo "$(GREEN)Rebuilding containers...$(NC)"
	$(COMPOSE) up --build -d

logs:
	$(COMPOSE) logs -f


migrate:
	@echo "$(GREEN)Running migrations...$(NC)"
	$(COMPOSE) exec api alembic upgrade head

seed:
	@echo "$(GREEN)Seeding database...$(NC)"
	$(COMPOSE) exec api python infrastructure/scripts/seed.py

reset-db:
	@echo "$(YELLOW)⚠️  Resetting database...$(NC)"
	$(COMPOSE) down -v
	$(COMPOSE) up -d postgres
	@sleep 5
	$(COMPOSE) up -d


worker:
	$(COMPOSE) exec worker celery -A app.core.celery_app worker --loglevel=info

shell:
	$(COMPOSE) exec api bash

clean:
	@echo "$(YELLOW)Removing containers and volumes...$(NC)"
	$(COMPOSE) down -v --remove-orphans
