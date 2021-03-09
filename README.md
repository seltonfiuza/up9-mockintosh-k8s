# up9-mockintosh-k8s

## Usage

#### First make sure to copy mockintosh.yml and mock-data folder given by `Export Spec in Contract tab` of up9


Run python3 main.py will create:
  - Configmaps for mockintosh.yml and mock-data folder;
  - PVC on GCP to make possible edit all mockintosh files (On minikube this may not working, maybe remove the PVC on links on models/mockintosh.yml;
  - A single POD with all services mapped Mockintosh (On minikube this may not working, maybe remove the PVC on links on models/mockintosh.yml;
  - A POD per service Mockintosh;
  
Run  python3 services_related.py will show All services that up9 is monitoring
