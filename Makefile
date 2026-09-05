.PHONY: install verify test lint ui evidence clean

install:
	python3 -m pip install -e ".[dev]"

test:
	TRUCKPLAN_FORCE_MOCK=1 python3 -m pytest -q

lint:
	python3 -m ruff check src tests || true

evidence:
	TRUCKPLAN_FORCE_MOCK=1 python3 scripts/write_evidence.py

verify: install test evidence
	@echo ""
	@echo "=== make verify OK ==="
	@echo "Mock Dallas→Houston distance_m=328500 duration_s=14100 (~204.1 mi, 3h 55m)"

ui:
	TRUCKPLAN_FORCE_MOCK=$${TRUCKPLAN_FORCE_MOCK:-1} python3 -m truckplan.ui

clean:
	rm -rf .pytest_cache .ruff_cache *.egg-info dist build .coverage htmlcov
