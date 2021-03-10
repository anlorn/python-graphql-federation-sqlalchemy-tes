clean:
	docker image rm -f python-openapi-test
build:
	docker build -t python-openapi-test .
run:
	docker run -p 8080:8080 python-openapi-test:latest
