dev:
	uvicorn server:app --reload --workers 1

test:
	pytest -q
