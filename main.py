from kubernetes import client, config
import yaml
import time
import subprocess
import os
import sys

NAMESPACE = 'up9'
CWD = os.getcwd()


if __name__ == '__main__':

    print("""
Creating configmap resources based on mockintosh.yml file and mock-data folder.
    """)

    config.load_kube_config()
    api_instance = client.AppsV1Api()
    core_instance = client.CoreV1Api()

    subprocess.run(['kubectl', 'apply', '-f', './models/pvc.yml'])
    try:
        with open('./models/statefulset.yml', 'r') as fp:
            yaml_as_dict = yaml.load(fp, Loader=yaml.FullLoader)
            result = api_instance.create_namespaced_stateful_set(
                namespace=NAMESPACE,
                body=yaml_as_dict,
                pretty=True,
            )
            print("Created up9-mockintosh-test statefulset")
    except Exception:
        pass

    try:
        while True:
            pod_status = core_instance.read_namespaced_pod_status(
                'up9-mockintosh-test-0', NAMESPACE)
            if pod_status.status.container_statuses[0].state.waiting.reason != 'PodInitializing':
                time.sleep(3.0)
                continue
            time.sleep(2.0)
            copy_zip_file = subprocess.run(
                ["kubectl", "cp", f"{CWD}/{sys.argv[1]}", "up9-mockintosh-test-0:/config/up9-contracts.zip", "-c", "up9-load-files"])
            print(f"Copied {sys.argv[1]} to the StatefulSet")
            break
    except Exception:
        pass
