terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.17.0"
    }
  }
}

provider "google" {
  project = "unique-sentinel-447714-e0"
  region  = "asia-southeast1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "unique-sentinel-447714-e0-demo-bucket"
  location      = "ASIA-SOUTHEAST1"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }

    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}