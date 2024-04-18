kubectl delete -f ../k8s/kube2iam.yaml
kubectl delete -f ../k8s/fastapi-deployment.yaml
kubectl delete -f ../k8s/fastapi-service.yaml
kubectl delete hpa fastapi-deployment

kubectl delete -f ../k8s/components.yaml

