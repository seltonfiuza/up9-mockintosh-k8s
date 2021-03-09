import json
import yaml
import kubernetes


UP9_CONFIGMAP_MOCKINTOSH = 'up9-mockintosh'
UP9_CONFIGMAP_MOCK_DATA = 'up9-mock-data'


class Deployment():

    name = ''
    containers = []
    yaml = ''

    def __init__(self, deploy_from_compose, namespace):
        self.namespace = namespace
        self.name = deploy_from_compose['hostname']
        self.deploy_from_compose = deploy_from_compose
        self.create_deployment_object()


    def create_deployment_object(self):
        name = f"up9-mockintosh-{self.name}"
        client = kubernetes.client
        spec = client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(
                match_labels={"name": name}
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={"name": name}
                ),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        command=['/bin/sh', '-c'],
                        args=[f"mockintosh {self.deploy_from_compose['command']}"],
                        image=self.deploy_from_compose['image'],
                        name=self.name,
                        ports=[client.V1ContainerPort(
                            container_port=self.deploy_from_compose['ports'][0]
                        )],
                        env=[client.V1EnvVar(
                            name=self.deploy_from_compose['environment'][0].split('=')[
                                0],
                            value=self.deploy_from_compose['environment'][0].split('=')[
                                1]
                        )],
                        volume_mounts=[client.V1VolumeMount(
                            mount_path='/config',
                            name=UP9_CONFIGMAP_MOCKINTOSH
                        ), client.V1VolumeMount(
                            mount_path='/config/mock-data',
                            name=UP9_CONFIGMAP_MOCK_DATA
                        )],
                    )],
                    volumes=[client.V1Volume(
                        name=UP9_CONFIGMAP_MOCKINTOSH,
                        config_map={"name": UP9_CONFIGMAP_MOCKINTOSH}
                    ), client.V1Volume(
                        name=UP9_CONFIGMAP_MOCK_DATA,
                        config_map={"name": UP9_CONFIGMAP_MOCK_DATA}
                    )]
                )

            ))
        body = client.V1Deployment(
            metadata={"name": name, "namespace": self.namespace},
            spec=spec
        )
        self.body = body
