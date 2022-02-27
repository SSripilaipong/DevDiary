variable GLOBAL_PREFIX {
  type = string
}

variable RESOURCE_SHARING_BUCKET_NAME {
  type = string
}

data "aws_s3_bucket" "resource-sharing" {
  name = var.RESOURCE_SHARING_BUCKET_NAME
}
