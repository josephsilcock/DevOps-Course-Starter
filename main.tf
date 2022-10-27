terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "Softwire21_JosephSilcock_ProjectExercise"
    storage_account_name = "tfstatejjs"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "Softwire21_JosephSilcock_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}todo-app-jjs"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id
  site_config {
    application_stack {
      docker_image     = "josephsilcock1/todo-app"
      docker_image_tag = "latest"
    }
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGODB_CONNECTION_STRING"  = azurerm_cosmosdb_account.main.connection_strings[0]
    "DB_NAME"                    = azurerm_cosmosdb_mongo_database.main.name
    "GITHUB_CLIENT_ID"           = var.github_client_id
    "GITHUB_CLIENT_SECRET"       = var.github_client_secret
    "SECRET_KEY"                 = var.secret_key
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                 = "${var.prefix}jjs-todo-cosmos"
  location             = data.azurerm_resource_group.main.location
  resource_group_name  = data.azurerm_resource_group.main.name
  offer_type           = "Standard"
  kind                 = "MongoDB"
  mongo_server_version = "3.6"
  capabilities {
    name = "EnableServerless"
  }
  capabilities {
    name = "EnableMongo"
  }
  consistency_policy {
    consistency_level = "Session"
  }
  geo_location {
    location          = "uksouth"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}jjs-todo-mongodb"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}
