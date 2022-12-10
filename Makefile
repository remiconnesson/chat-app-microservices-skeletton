build-frontend:
	@cd spa/www && npm run build
	docker compose build frontend
