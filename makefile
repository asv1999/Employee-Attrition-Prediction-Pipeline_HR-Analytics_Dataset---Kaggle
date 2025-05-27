SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

py = $$(if [ -d $(PWD)/.venv ]; then echo $(PWD)/.venv/bin/python3; else echo python3; fi)
pip = $(py) -m pip

.PHONY: install
install:
	$(pip) install -r requirements.txt

.PHONY: data
data:
	$(py) src/data/processing.py

.PHONY: train
train:
	$(py) src/models/pipeline.py

.PHONY: notebook
notebook:
	jupyter notebook --ip=0.0.0.0 --port=8888
