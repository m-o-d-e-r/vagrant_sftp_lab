
SHELL := /bin/bash


run_cert_provider:
	python -m cert_provider

build_cert_provider:
	docker build -f Dockerfile.cert_provider -t cert_provider .

run_cert_provider_docker:
	source .env && docker run --rm -e SFTP_SERVER_LIST='192.168.33.201    192.168.33.202   192.168.33.203' --network cert_provider_net --ip 192.10.0.2 cert_provider

run_report_maker:
	python -m report_maker

build_report_maker:
	docker build -f Dockerfile.report_maker -t report_maker .

run_report_maker_docker:
	docker run --rm --network cert_provider_net --ip 192.10.0.3 report_maker

build_report_maker_go:
	docker build -f Dockerfile.report_maker_go -t report_maker_go .

run_report_maker_go_docker:
	docker run --rm --env-file .env --network host report_maker_go

create_cert_provider_net:
	docker network create --driver=bridge --subnet=192.10.0.0/16 cert_provider_net

activate_env:
	source .venv/bin/activate
