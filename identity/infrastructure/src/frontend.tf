variable FRONTEND_S3_BUCKET_NAME {
  type = string
}

resource "aws_s3_bucket" "frontend" {
  bucket = var.FRONTEND_S3_BUCKET_NAME
}

resource "aws_s3_bucket_acl" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  acl    = "public-read"
}
resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Statement = [
      {
        Sid       = "PublicRead"
        Action    = "s3:GetObject"
        Effect    = "Allow"
        Principal = "*"
        Resource  = "${aws_s3_bucket.frontend.arn}/*"
      },
    ]
    Version   = "2012-10-17"
  })
}
