build:
	poetry install

start:
	poetry run gunicorn task_manager.wsgi --log-file -