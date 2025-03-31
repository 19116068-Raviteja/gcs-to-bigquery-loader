variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Cloud Storage Bucket Name"
  type        = string
}
