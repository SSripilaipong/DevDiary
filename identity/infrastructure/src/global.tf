variable GLOBAL_PREFIX {
  type = string
}

variable APP_NAME {
  type = string
}

variable AWS_ACCOUNT_ID {
  type = string
}

data "aws_apigatewayv2_apis" "core" {
  name          = var.GLOBAL_PREFIX
}

data "aws_apigatewayv2_api" "core" {
  api_id = one(data.aws_apigatewayv2_apis.core.ids)
}

resource "aws_s3_bucket" "identity" {
  bucket = "${var.APP_NAME}-${var.GLOBAL_PREFIX}-identity"
  force_destroy = true
}

resource "aws_s3_bucket_acl" "resource-sharing" {
  bucket = aws_s3_bucket.identity.id
  acl = "private"
}
