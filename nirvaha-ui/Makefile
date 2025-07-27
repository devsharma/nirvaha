# CRM Application Makefile

.PHONY: help build run dev stop clean logs setup

# Default target
help:
	@echo "Available commands:"
	@echo "  setup     - Setup project files and dependencies"
	@echo "  build     - Build Docker image"
	@echo "  run       - Run production application"
	@echo "  dev       - Run development application with hot reload"
	@echo "  stop      - Stop all containers"
	@echo "  clean     - Remove containers and images"
	@echo "  logs      - View application logs"
	@echo "  test      - Run tests (if available)"

# Setup project
setup:
	@echo "Setting up CRM application..."
	npm install
	@echo "Setup complete!"

# Build Docker image
build:
	@echo "Building Docker image..."
	docker-compose build
	@echo "Build complete!"

# Run production application
run:
	@echo "Starting CRM application in production mode..."
	docker-compose up -d
	@echo "Application started at http://localhost:3000"
	@echo "Login with: admin@crm.com / password123"

# Run development application
dev:
	@echo "Starting CRM application in development mode..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Development server started at http://localhost:5173"
	@echo "Login with: admin@crm.com / password123"

# Stop all containers
stop:
	@echo "Stopping all containers..."
	docker-compose down
	docker-compose -f docker-compose.dev.yml down
	@echo "All containers stopped!"

# Clean up containers and images
clean:
	@echo "Cleaning up containers and images..."
	docker-compose down --rmi all --volumes --remove-orphans
	docker-compose -f docker-compose.dev.yml down --rmi all --volumes --remove-orphans
	docker system prune -f
	@echo "Cleanup complete!"

# View logs
logs:
	@echo "Viewing application logs..."
	docker-compose logs -f

# View development logs
logs-dev:
	@echo "Viewing development logs..."
	docker-compose -f docker-compose.dev.yml logs -f

# Health check
health:
	@echo "Checking application health..."
	@curl -f http://localhost:3000 > /dev/null 2>&1 && echo "✅ Application is healthy" || echo "❌ Application is not responding"

# Quick restart
restart: stop run

# Quick development restart
restart-dev: stop dev
