build:
	python3 setup.py sdist

install:
	python3 setup.py install

remove:
	python3 -m pip uninstall -y cjutils

upload: clean format build
	twine upload dist/*	

clean:
	rm -rf build cjutools.egg-info dist

format:
	python3 -m cjutools format -Pi

all: clean format build remove install
