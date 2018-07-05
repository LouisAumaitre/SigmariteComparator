
requirements.txt:
	@pip-compile --no-index --output-file requirements.txt requirements.in

clean:
	rm .coverage junit.xml