help:
	@echo "   help          display this message"
	@echo "   clean         remove emacs leftovers"
	@echo "   coverage      report test coverage"
	@echo "   TAGS          generate tags for the python code in this directory"

clean:
	@find . -name "*~" | xargs rm -fv

coverage:
	py.test --cov --cov-report term-missing --skip deployable

TAGS: test/*.py tbx/*.py
	find . -name "*.py" | egrep -v "(venv|.tox)" | xargs etags
