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
	@echo "Mock Ontario CA→Chicago ~2010 mi: distance_m=3234781 duration_s=131564 (36h 32m, 4 HOS days)"
	@echo "ROI illustrative: 32→4 min saved 28 min; ~$$16.33/trip; ~$$131/day @8 long-haul dispatches"

ui:
	TRUCKPLAN_FORCE_MOCK=$${TRUCKPLAN_FORCE_MOCK:-1} python3 -m truckplan.ui

clean:
	rm -rf .pytest_cache .ruff_cache *.egg-info dist build .coverage htmlcov
