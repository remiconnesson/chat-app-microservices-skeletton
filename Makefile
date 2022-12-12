build-frontend:
	@cd spa/www && npm run build
	docker compose build frontend

npm-install-spa:
	@cd spa/www && npm install

npm-install-auth:
	@cd auth && npm install

