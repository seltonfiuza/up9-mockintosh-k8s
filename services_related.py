from kubernetes import client, config
import yaml
import pprint

config.load_kube_config()

api_instance = client.CoreV1Api()


def get_services_by_namespace(data):
    services_related = []
    for namespace in data:
        services = api_instance.list_namespaced_service(namespace).to_dict()
        for service in services['items']:
            for port in service['spec']['ports']:
                full_address = f"{service['metadata']['name']}.{namespace}:{port['port']}"
                services_related.append(full_address)
    return services_related


def get_services_by_services(data):
    services_related = []
    for service in data:
        service_details = api_instance.read_namespaced_service(
            service['name'], service['namespace']).to_dict()
        for port in service_details['spec']['ports']:
            full_address = f"{service['name']}.{service['namespace']}:{port['port']}"
            services_related.append(full_address)
    return services_related


def get_related_services(api_instance, namespace, configmap):
    api_response = api_instance.read_namespaced_config_map(
        configmap, namespace)

    data = api_response.to_dict()['data']

    data_loaded = yaml.load(
        data['up9-injector-config'], Loader=yaml.FullLoader)

    if len(data_loaded['includedNamespaces']) > 0:
        services_related = get_services_by_namespace(
            data_loaded['includedNamespaces'])

    if len(data_loaded['services']) > 0:
        services_related = get_services_by_services(data_loaded['services'])

    return services_related


print(get_related_services(api_instance, 'up9', 'up9-injector-config'))
