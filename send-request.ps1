# send-request.ps1

# Définir les en-têtes
$headers = @{
    "Content-Type" = "application/json"
}

# Définir les données
$data = @{
    username = "johnarmstrong"
    password = "737ae5a9-d78"
} | ConvertTo-Json

# Envoyer la requête
$response = Invoke-WebRequest -Uri http://localhost:8080/login -Headers $headers -Method POST -Body $data

# Afficher la réponse
$response.Content
