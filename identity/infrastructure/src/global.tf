variable GLOBAL_PREFIX {
  type = string
}

variable RESOURCE_SHARING_BUCKET_NAME {
  type = string
}

data "aws_s3_bucket" "resource-sharing" {
  bucket = var.RESOURCE_SHARING_BUCKET_NAME
}

data "aws_apigatewayv2_apis" "core" {
  name          = var.GLOBAL_PREFIX
}

data "aws_apigatewayv2_api" "core" {
  api_id = data.aws_apigatewayv2_apis.core.ids[0]
}
