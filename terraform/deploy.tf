terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# resource "google_storage_bucket" "bucket" {
#   name     = var.bucket_name
#   location = var.bucket_location
#   project  = var.project_id
# }

resource "google_compute_instance" "default" {
  name         = var.instance_name
  project      = var.project_id
  machine_type = var.machine_type
  tags         = var.tags
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.image
      size  = var.size
      type  = var.disk-type
    }
  }

  network_interface {
    network = var.network

    access_config {
      // Ephemeral public IP
    }
  }

  metadata = {
    ssh_key = var.ssh_key
  }

  service_account {
    email  = var.service_account_email
    scopes = ["cloud-platform"]
  }

  metadata_startup_script = "apt-get update"
}
