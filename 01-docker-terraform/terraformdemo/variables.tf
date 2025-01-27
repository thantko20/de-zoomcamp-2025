variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "unique-sentinel-447714-e0"
}

variable "region" {
  description = "Project Region"
  default     = "asia-southeast1"
}

variable "location" {
  description = "Project Location"
  default     = "ASIA-SOUTHEAST1"
}

variable "bq_dataset_name" {
  description = "My bigquery dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "unique-sentinel-447714-e0-demo-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}
