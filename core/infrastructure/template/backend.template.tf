terraform {
  backend "s3" {
    bucket = "TF_BACKEND_BUCKET_NAME"
    key    = "TF_BACKEND_BUCKET_PATH"
    region = "AWS_REGION"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.0.0"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  region  = "AWS_REGION"
}
