variable "project" {
    description = "GCP Project Id"
    default     = "de-zoomcamp-capstone"
}

variable "credentials_file" {
    default = "/home/user/de-zoomcamp-capstone/config/.secret.json"
    type    = string
}

variable "region" {
    default = "asia-southeast1"
}

variable "bucket_name" {
    default = "bandcamp"
}

variable "bucket_location" {
    default = "asia-southeast1"
}

variable "bq_dataset_name" {
    default = "bandcamp"
}