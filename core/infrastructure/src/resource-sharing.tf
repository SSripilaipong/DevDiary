variable RESOURCE_SHARING_BUCKET_NAME {
  type = string
}

resource "aws_s3_bucket" "resource-sharing" {
  bucket = var.RESOURCE_SHARING_BUCKET_NAME

  acl           = "private"
  force_destroy = true
}
