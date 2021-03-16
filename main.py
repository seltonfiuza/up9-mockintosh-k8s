from os import system, popen, path, strerror
import errno
from kubernetes import client, config
import json
import yaml
import pprint
from models import Deployment
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("option", help="""
[single] to install a single deploment mockintosh on cluster; or;
[multiple] to install one mockintosh deployment per service in docker-compose.yml
""")
args = parser.parse_args()

NAMESPACE = 'up9'

if __name__ == '__main__':

    try:
        print("""
        Creating configmap resources based on mockintosh.yml file and mock-data folder.
        """)
        if not path.isfile('mockintosh.yml'):
            raise FileNotFoundError(
                errno.ENOENT, strerror(errno.ENOENT), 'mockintosh.yml')
        if not path.isdir('mock-data'):
            raise FileNotFoundError(
                errno.ENOENT, strerror(errno.ENOENT), 'mock-data')
        system(f'kubectl delete configmap -n {NAMESPACE} up9-mockintosh --ignore-not-found')

        system(f'kubectl delete configmap -n {NAMESPACE} up9-mock-data  --ignore-not-found')

        system(f'kubectl create configmap -n {NAMESPACE} up9-mockintosh \
            --from-file=mockintosh.yml')

        system(f'kubectl create configmap -n {NAMESPACE} up9-mock-data \
            --from-file=mock-data/')
        
        if args.option == 'single':
        # Create a single POD mockintosh
            system(f"kubectl apply -f models/mockintosh.yml")

        elif args.option == 'multiples':
        # Create one mockintosh POD per service in docker-compose file
            with open('./docker-compose.yml', 'r') as f:
                docker_compose_file = f.read()

            config.load_kube_config()

            api_instance = client.AppsV1Api()

            yaml_as_dict = yaml.load(docker_compose_file, Loader=yaml.Loader)
            for service in yaml_as_dict['services']:
                deploy = Deployment(yaml_as_dict['services'][service], NAMESPACE)
                result = api_instance.create_namespaced_deployment(
                    namespace=NAMESPACE,
                    body=deploy.body,
                    pretty=True,
                    )
                print(f"Created {service} mockintosh deployment")

    except Exception as e:
        print(e)
    finally:
        print("done")