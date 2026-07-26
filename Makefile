.PHONY: setup pipeline dashboard

setup:
	python -m pip install .

pipeline:
	python load_data.py

dashboard:
	@echo "Dashboard not implemented"
