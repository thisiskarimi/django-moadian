CURR_DIR=$(shell pwd)
run:
	docker run -p 8000:8000 -dit -v ${CURR_DIR}/django_moadian:/home/django_moadian --name moadian_app moadian

rm:
	docker rm moadian_app

stop:
	docker stop moadian_app

bash:
	docker exec -it moadian_app bash

all:
	-make stop
	-make rm
	make run
