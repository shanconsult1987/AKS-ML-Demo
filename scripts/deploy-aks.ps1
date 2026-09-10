$ErrorActionPreference = "Stop"

$resourceGroup = azd env get-value AZURE_RESOURCE_GROUP
$acrLoginServer = azd env get-value ACR_LOGIN_SERVER
$aksName = azd env get-value AKS_NAME
$acrName = $acrLoginServer.Split('.')[0]

Write-Host "Training ML model..."
Push-Location ml-api
python train_model.py
Pop-Location

Write-Host "Getting AKS credentials..."
az aks get-credentials --resource-group $resourceGroup --name $aksName --overwrite-existing

Write-Host "Building application image..."
az acr build --registry $acrName --image aks-demo:v1 ./app

Write-Host "Building ML image..."
az acr build --registry $acrName --image ml-api:v1 ./ml-api

Write-Host "Applying Kubernetes resources..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/pvc.yaml

(Get-Content k8s/deployment.yaml) -replace '\$\{ACR_LOGIN_SERVER\}', $acrLoginServer | kubectl apply -f -
kubectl apply -f k8s/service.yaml

(Get-Content k8s/ml-deployment.yaml) -replace '\$\{ACR_LOGIN_SERVER\}', $acrLoginServer | kubectl apply -f -
kubectl apply -f k8s/ml-service.yaml

Write-Host ""
Write-Host "Deployment complete."
kubectl get pods -n aks-demo
kubectl get svc -n aks-demo
kubectl get pvc -n aks-demo
