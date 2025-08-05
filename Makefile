test:
	uv run pytest tests

test-cov:
	uv run coverage run -m pytest tests

cov-report:
	uv run coverage combine && uv run coverage report

cov: test-cov cov-report

typing:
	uv run mypy --install-types --non-interactive src/pyshelf tests

style:
	uv run ruff . && uv run black --check --diff .

fmt:
	uv run black . && uv run ruff --fix . && make style

lint: style typing

compile: 
	cd src/frontend && sh compile.sh && cd ../..

install:
	cd src/frontend && npm install
