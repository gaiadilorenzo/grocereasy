resource "google_compute_instance" "orchestrator" {
  boot_disk {
    auto_delete = true
    device_name = "orchestrator"

    initialize_params {
      image = "https://www.googleapis.com/compute/beta/projects/cos-cloud/global/images/cos-stable-101-17162-127-8"
      size  = 10
      type  = "pd-standard"
    }

    mode   = "READ_WRITE"
    source = "https://www.googleapis.com/compute/v1/projects/${var.gcp_project_id}/zones/us-central1-c/disks/orchestrator"
  }

  confidential_instance_config {
    enable_confidential_compute = false
  }

  labels = {
    container-vm = "cos-stable-101-17162-127-8"
  }

  machine_type = "e2-micro"

  metadata = {
    ssh-keys                  = "gaiadilorenzo01:ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBEklJy4IXU8I/H3ZnGZLXbNyKMrt8YhMlAxF3N8GwKpMKYzgl9R9WKtgEgx4Bfbh7ah5Z6x/7KKJH04w74yCnY8= google-ssh {\"userName\":\"gaiadilorenzo01@gmail.com\",\"expireOn\":\"2023-04-15T20:48:02+0000\"}\ngaiadilorenzo01:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCv6jm1WP3CB11MNJ8o10fdZVHGwcbQkiXoyXxUFTn2rv+9yayPCXtY2YIj5FJnmEtb7b4mEZu7cUJoMHtrJdY+z18qm9rExuLTqR0YKOBF5KEqy1fJ2Q3/NWXIIYrJKACN9y9PL+41k9MUpP5cYjYeBRG9IgUIIPH807fbk2ImpyOTbMe9O3jMWIcJHcv9c7J27EtwsA9UAbtfyt+ePl+u9AVM6TSB4SStM4zZR4KE5bzRfKjqccVSoM963Cq2qLHJ6C10NCNcrAh6u9XR4Hm2qYntfwPt3Bd3XUajGfpPYElzlyyIsjXi+UAHiKabWNtnfzHWPsHONO2I9Q1v6otp google-ssh {\"userName\":\"gaiadilorenzo01@gmail.com\",\"expireOn\":\"2023-04-15T20:48:19+0000\"}\ngaiadilorenzo01:ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBKo9JwzHs4NpBqKS0e0u/r1Y7ZrPsmT4/AZtBCrEBaYt2urXO/Rl273gYvgQ8sv+vnhaTZq5FnDgPEpn0JNTfbI= google-ssh {\"userName\":\"gaiadilorenzo01@gmail.com\",\"expireOn\":\"2023-04-15T20:50:06+0000\"}\ngaiadilorenzo01:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCYG1Jnw+091gKDu6DBL+Obh/tMv+xy8lkRb8liSOoDE83N76JMbWjkRNl6YMW0p7bsvf/pzhc4p9l6CAPsmo5xlnnoJwt4XZuqLF3pVRtdF8A/6GxGneZRS5CF+92SvH0iaT5PzF6iCVnqnacDh8XeOKIvSh1SvAYEUmTbsdbL35xhgG24QpmPr/AzLicbrjzudkfMh2fCR7sIRjTziGG9RkaRdTxrkRihFGQbPMfBipeVpz99Tuaru6m4XrNoDON2KwJhU/6pj1fpbcCvKBkHPB+yvSQPrZHSQ4GGHOzX9O2bsFKZRvmzpdoc5lszF4Wyg+O/A2EPtNye9/LNUQFT google-ssh {\"userName\":\"gaiadilorenzo01@gmail.com\",\"expireOn\":\"2023-04-15T20:50:23+0000\"}\ngaiadilorenzo01:ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAMfPEo9UxFAqcgXdDkP+wAo/GEWm5utcMMVlEgI6Ggp9fwvV5XVsnpJNGLnjvTxy9yp6PVUd9JeDw3Ponz7O40= google-ssh {\"userName\":\"gaiadilorenzo01@gmail.com\",\"expireOn\":\"2023-04-15T20:50:31+0000\"}\ngaiadilorenzo01:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCgKWQHNjks4dJmHat50iCSOpGzIH3Trpje9EsU58zvxLxQUgSK20WsfdVIcPURpn+RpZPUrUexDmzBBDqj6lmU1tAaFYM9yMOL8GaLRNEgnDE14CEQ2g5Mhb+Hz7vTnfE0C8MXiatyDIyumC0BMtJxTOIvpzrLyOOBALFCA+DNkAZPq7EKK+kHdyhnTviwR98E12QxfgO9VbjTyk6mDNKi2rMM/LVQiBvRwHL63PH6juozJGkZKhNN56ucKElkyJ/RmaSiILI9UHoRGoNiEW1C9e7p9TCQ0Z8sRd4/cWEplAITXJ1X6fNYO2aUmhpDJWwXDxMA1PkU4IdQbhYf9Bfh google-ssh {\"userName\":\"gaiadilorenzo01@gmail.com\",\"expireOn\":\"2023-04-15T20:50:47+0000\"}"
    gce-container-declaration = "# DISCLAIMER:\n# This container declaration format is not a public API and may change without\n# notice. Please use gcloud command-line tool or Google Cloud Console to run\n# Containers on Google Compute Engine.\n\nspec:\n  containers:\n  - image: gcr.io/${var.gcp_project_id}/orchestrator:265dcf05d97a35e26a26c3d350dc9d30709c3bde\n    name: orchestrator\n    stdin: false\n    tty: false\n    volumeMounts: []\n  restartPolicy: Always\n  volumes: []\n"
    startup-script            = "#! /bin/bash\n    docker image prune -af"
  }

  name = "orchestrator"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    network            = "https://www.googleapis.com/compute/v1/projects/${var.gcp_project_id}/global/networks/default"
    network_ip         = "10.128.0.2"
    stack_type         = "IPV4_ONLY"
    subnetwork         = "https://www.googleapis.com/compute/v1/projects/${var.gcp_project_id}/regions/us-central1/subnetworks/default"
    subnetwork_project = var.gcp_project_id
  }

  project = var.gcp_project_id

  reservation_affinity {
    type = "ANY_RESERVATION"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "deploy@${var.gcp_project_id}.iam.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_vtpm                 = true
  }

  tags = ["http-server", "https-server"]
  zone = var.gcp_zone
}
# terraform import google_compute_instance.orchestrator projects/${var.gcp_project_id}/zones/us-central1-c/instances/orchestrator
