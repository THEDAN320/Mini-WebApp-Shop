dev_up:
	docker compose up -d --build

dev_down:
	docker compose down

bot_up:
	docker compose up -d --build bot

bot_down:
	docker compose down bot

backend_up:
	docker compose up -d --build backend

backend_down:
	docker compose down backend

.PHONY: dev_up dev_down bot_up bot_down backend_up backend_down
