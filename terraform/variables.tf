variable "project_id" {
  type        = string
  description = "The project ID that resource(s) is deployed to"
}

variable "region" {
  type        = string
  description = "The region to deploy to (Default: us-central1)"
  default     = "us-central1"
}

variable "zone" {
  type        = string
  description = "The zone to deploy to (Default: us-central1-a)"
  default     = "us-central1-a"
}

variable "bucket_name" {
  type        = string
  description = "The name of the bucket to create (Default: flask-crypto-bucket)"
  default     = "flask-crypto-bucket"
}

variable "bucket_location" {
  type        = string
  description = "The bucket location (Default: US)"
  default     = "US"
}

variable "instance_name" {
  type        = string
  description = "The compute engine instance name (Default: instance1)"
  default     = "instance1"
}

variable "machine_type" {
  type        = string
  description = "The machine type (Default: e2-medium)"
  default     = "e2-medium"
}

variable "tags" {
  type        = list(string)
  description = "The tags to apply to the instance (Default: http-server, https-server)"
  default     = ["http-server", "https-server"]
}

variable "image" {
  type        = string
  description = "The image to use for the instance (Default: ubuntu-os-cloud/ubuntu-2204-lts)"
  default     = "ubuntu-os-cloud/ubuntu-2204-lts"
}

variable "size" {
  type        = string
  description = "The size of the boot disk (Default: 10gb)"
  default     = "10"
}

variable "disk-type" {
  type        = string
  description = "The type of the boot disk (Default: pd-ssd)"
  default     = "pd-ssd"
}

variable "network" {
  type        = string
  description = "The network to use for the instance (Default: default)"
  default     = "default"
}

variable "ssh_key" {
  type        = string
  description = "The ssh key to use for the instance (Default: \"\")"
  default     = ""
}

variable "service_account_email" {
  type        = string
  description = "The service account email to use for the instance (Default: \"fresher-training-02@appspot.gserviceaccount.com\")"
  default     = "fresher-training-02@appspot.gserviceaccount.com"
}