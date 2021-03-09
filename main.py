from os import system, popen
from kubernetes import client, config
import json
import yaml
import pprint
from models import Deployment

NAMESPACE = 'up9'

if __name__ == '__main__':

    # Create confimap

    system(f'kubectl delete configmap -n {NAMESPACE} up9-mockintosh --ignore-not-found')

    system(f'kubectl delete configmap -n {NAMESPACE} up9-mock-data  --ignore-not-found')

    system(f'kubectl create configmap -n {NAMESPACE} up9-mockintosh \
        --from-file=mockintosh.yml')

    system(f'kubectl create configmap -n {NAMESPACE} up9-mock-data \
        --from-file=mock-data/')

    # Create a single POD mockintosh

    system(f"kubectl apply -f models/mockintosh.yml")
    
    
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
        
