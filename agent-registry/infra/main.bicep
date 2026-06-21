targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment used to derive resource names (azd).')
param environmentName string

@minLength(1)
@description('Primary location for all resources.')
param location string

@description('Auth mode for the registry API: dev or entra.')
@allowed([
  'dev'
  'entra'
])
param authMode string = 'entra'

@description('Microsoft Entra ID tenant id (required when authMode=entra).')
param entraTenantId string = ''

@description('API audience, e.g. api://<registry-app-client-id> (required when authMode=entra).')
param entraApiAudience string = ''

@description('Allowed CORS origin for the marketplace UI.')
param corsOrigins string = '*'

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = {
  'azd-env-name': environmentName
}

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

module resources './resources.bicep' = {
  name: 'resources'
  scope: rg
  params: {
    location: location
    tags: tags
    resourceToken: resourceToken
    abbrs: abbrs
    authMode: authMode
    entraTenantId: entraTenantId
    entraApiAudience: entraApiAudience
    corsOrigins: corsOrigins
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = resources.outputs.registryLoginServer
output SERVICE_API_URI string = resources.outputs.apiUri
output COSMOS_ENDPOINT string = resources.outputs.cosmosEndpoint
