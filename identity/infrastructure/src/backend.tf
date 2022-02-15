terraform {
  backend "s3" {
    bucket = "devdiary.link-terraform"
    key    = "prod/identity.tfstate"
    region = "ap-southeast-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "workshop"
  region  = "ap-southeast-1"
}
