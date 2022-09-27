build:
	python3 setup.py sdist

install:
	python3 setup.py install

remove:
	python3 -m pip uninstall -y cjutils

upload:
	twine upload dist/*	

clean:
	rm -rf build cjutools.egg-info dist

all: clean build remove install
