user:
	python ./flarchive/__init__.py -v -a ${APIKEY} -n ${NSID} -d ./data

list-commons:
	python ./flarchive/__init__.py -v -a ${APIKEY} --commons -l

commons:
	python ./flarchive/__init__.py -v -a ${APIKEY} --commons -d ./data
