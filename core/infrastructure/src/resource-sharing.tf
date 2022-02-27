variable RESOURCE_SHARING_BUCKET_NAME {
  type = string
}

resource "aws_s3_bucket" "resource-sharing" {
  bucket = var.RESOURCE_SHARING_BUCKET_NAME
  force_destroy = true
}

resource "aws_s3_bucket_acl" "resource-sharing" {
  bucket = aws_s3_bucket.resource-sharing.id
  acl = "private"
}
