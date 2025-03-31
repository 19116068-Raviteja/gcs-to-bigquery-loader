terraform {
  backend "gcs" {
    bucket  = "cloud-infra-hub-dev-tf-state"
    prefix  = "gcs-to-bigquery-loader"
  }
}
