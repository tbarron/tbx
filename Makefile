help:
	@echo "   help          display this message"
	@echo "   TAGS          generate tags for the python code in this directory"
	@echo "   coverage      report test coverage"

coverage:
	py.test --cov --cov-report term-missing --skip deployable

TAGS: test/*.py tbx/*.py
	find . -name "*.py" | egrep -v "(venv|.tox)" | xargs etags
