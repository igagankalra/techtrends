## Kubernetes Declarative Manifests 

Place the Kubernetes declarative manifests in this directory.
## Command to remove a Namespace -- 
    ```shell
        kubectl get ns argocd  -o json | jq '.spec.finalizers = []' | kubectl replace --raw "/api/v1/namespaces/argocd/finalize" -f -
    ```