# up9-mockintosh-k8s

## Usage

First make sure to copy mockintosh.yml and mock-data folder given by `Export Spec in Contract tab` of up9 to this folder. Afther that you can run python3 main.py [option]

```shell
> python3 main.py --help   
usage: main.py [-h] option

positional arguments:
  option      [single] to install a single deploment mockintosh on cluster; or; [multiple] to install one mockintosh deployment per service in docker-compose.yml

optional arguments:
  -h, --help  show this help message and exit
```

> Run  python3 services_related.py will show All services that up9 is monitoring
