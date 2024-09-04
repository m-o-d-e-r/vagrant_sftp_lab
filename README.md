
## Requirements
* Docker
* Vagrant
* `make` tool

## How to run


First of all, we need to launch `cert_provider`. This tool will provide VMs with needed SSH keys.

You can use `make` commands to build and run tools.
```bash
make build_cert_provider
```

Run `cert_provider`.
```bash
make run_cert_provider_docker
```

Run `Vagrantfile`.
```bash
vagrant up --provider=<your provider> --provision
```

> [!IMPORTANT]
> `generic/ubuntu1804` used as an image for all VMs, there may be no such image available for your provider, pls change images accordingly.


Build `report_maker_go`
```bash
make build_report_maker_go
```

Run `report_maker_go`
```bash
make run_report_maker_go_docker
```

Now, you can access `report_mager_go` tool in your browser by visiting `localhost:8080`.
