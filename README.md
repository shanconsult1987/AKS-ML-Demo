# AKS + AZD + ML Demo

Simple workshop demonstrating:

- Azure Developer CLI (azd)
- Bicep infrastructure
- Azure Container Registry
- Azure Kubernetes Service
- Kubernetes Deployment / ReplicaSet / Pods
- ConfigMap
- Secret
- PVC / Azure Disk
- LoadBalancer Service
- Internal ClusterIP ML service
- Random Forest ML inference API
- Scaling and monitoring

## Prerequisites

- Azure CLI
- Azure Developer CLI (azd)
- kubectl
- Python 3.12+
- Azure subscription

## Before azd up

1. Replace `REPLACE_WITH_UNIQUE_ACR_NAME` in `infra/main.parameters.json`.
2. Train the ML model:

```powershell
cd ml-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python train_model.py
cd ..
```

## Login

```powershell
az login
azd auth login
```

## Create environment

```powershell
azd env new aksdemo
azd env set AZURE_LOCATION centralindia
```

Set the unique ACR name through the Bicep parameter file or adapt the infra parameterization for your environment.

## Deploy everything

```powershell
azd up
```

The postprovision hook:
1. Gets AKS credentials
2. Builds the application image in ACR
3. Builds the ML image in ACR
4. Applies Kubernetes manifests
5. Creates the PVC and services

## Verify

```powershell
kubectl get nodes
kubectl get pods -n aks-demo
kubectl get deployment -n aks-demo
kubectl get rs -n aks-demo
kubectl get pvc -n aks-demo
kubectl get svc -n aks-demo
```

## Test ML API

```powershell
kubectl port-forward service/ml-api-service 8080:80 -n aks-demo
```

In another PowerShell window:

```powershell
$body = @{
    features = @(5.1, 3.5, 1.4, 0.2)
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8080/predict `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

## Scaling

```powershell
kubectl scale deployment ml-api --replicas=5 -n aks-demo
kubectl get pods -n aks-demo
```

## Monitoring

```powershell
kubectl top nodes
kubectl top pods -n aks-demo
kubectl logs deployment/ml-api -n aks-demo
```

## Cleanup

```powershell
azd down
```
