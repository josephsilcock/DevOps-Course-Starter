# Kubernetes

We have files to set up the app on a local minikube cluster. You will need to have installed 
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Docker desktop](https://docs.docker.com/desktop/install/windows-install/)

First, with docker desktop running, run `minikube start` in an elevated rights terminal.

Next create a docker image and load it into minikube:
```bash
docker build --target production --tag todo-app:prod . && minikube image load todo-app:prod
```

[Create a secret](https://kubernetes.io/docs/concepts/configuration/secret/#creating-a-secret) called `todo-app` with 
the following values:
- flask_secret_key
- mongodb_name
- mongodb_connection_string
- github_client_secret
- github_client_id
- loggly_token

Finally, navigate to the `kubernetes/` folder and run:
```bash
kubectl apply -f deployment.yaml && kubectl apply -f service.yaml &&  kubectl port-forward service/module-14 7080:80
```

The app should now be running at http://localhost:7080.