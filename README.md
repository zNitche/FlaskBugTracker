# FlaskBugTracker

---

Bug Tracker app created using Flask and MySQL, supporting:
- Accounts management.
- Accounts permissions.
- Projects management.
- Issues management.
- Assign users to issues.
- Filtering issues by status.
- Downloading project reports.

---

## Production Setup
1. Clone this repo.
2. Generate `.env` config file and change config values (`MYSQL_ROOT_PASSWORD`).
```
python3 generate_dotenv.py
```
3. Run docker container.
```
sudo docker compose -f docker-compose.yml up -d
```

## Dev Setup
1. Clone this repo.
2. Generate `.env` config file and change config values (`MYSQL_ROOT_PASSWORD`).
```
python3 generate_dotenv.py
```
3. Change `MYSQL_SERVER_HOST` in `.env` to `127.0.0.1`
4. Run DEV docker-compose.
```
sudo docker compose -f docker-compose-dev.yml up
```

## Tests
App contains some example tests for available blueprints. To run them:
```
pytest -v tests/
```
