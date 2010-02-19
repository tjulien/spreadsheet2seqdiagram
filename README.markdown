spreadsheet2seqdiagram
=====================

Grabs system calls from a google spreadsheet and generates sequence diagrams using http://www.websequencediagrams.com

The format of the spreadsheet is one call per row, using the following columns:
Description, Type, Input, Caller, Callee, Result

Installation
============

	git clone git@github.com:tjulien/spreadsheet2seqdiagram.git
	cd spreadsheet2seqdiagram
	wget http://gdata-python-client.googlecode.com/files/gdata-2.0.7.zip
	unzip gdata-2.0.7.zip
	cd gdata-2.0.7
	./setup.py install
