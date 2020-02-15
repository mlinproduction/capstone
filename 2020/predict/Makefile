predict-test:
	# Calling predict function from terminal
	python predict/run.py /path/to/model/artefacts/ --text="ruby on rails: how to change BG color of options in select list, ruby-on-rails"

flask-server-local:
	# starts flask server
	python predict/app.py /path/to/model/artefacts/

request:
	# make a POST request to flask server (needs to be running, for example having executed flask-server-local)
	curl -v http://0.0.0.0:5000/tag/predict/ -d text="ruby on rails: how to change BG color of options in select list, ruby-on-rails"

flask-server:
	docker run -p 5000:5000 predict

flask-server-debug:
	docker run -it -p 5000:5000 -v "$PWD":/libraries/app predict


