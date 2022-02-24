variable FRONTEND_S3_BUCKET_NAME {
  type = string
}

resource "aws_s3_bucket" "frontend" {
  bucket = var.FRONTEND_S3_BUCKET_NAME
}

resource "aws_s3_bucket_acl" "frontend" {
  bucket = aws_s3_bucket.frontend.id
}
