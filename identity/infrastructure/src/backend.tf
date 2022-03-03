locals {
  BACKEND_NAME = "${var.GLOBAL_PREFIX}-identity-backend"
}

resource "aws_iam_role" "backend-exec" {
  name = local.BACKEND_NAME

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

data "archive_file" "lambda" {
  type = "zip"
  source_dir  = "../../backend/src"
  output_path = "../../backend/lambda.zip"
}

resource "aws_s3_object" "lambda" {
  bucket = aws_s3_bucket.identity.id

  key    = "backend/lambda.zip"
  source = data.archive_file.lambda.output_path

  etag = filemd5(data.archive_file.lambda.output_path)
}

resource "aws_lambda_function" "backend" {
  function_name = local.BACKEND_NAME

  s3_bucket = aws_s3_bucket.identity.id
  s3_key    = "backend/lambda.zip"
  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.9"
  handler = "main.handler"

  role = aws_iam_role.backend-exec.arn

  depends_on = [
    aws_iam_role.backend-exec,
  ]
}

resource "aws_cloudwatch_log_group" "backend" {
  name = "/aws/lambda/${local.BACKEND_NAME}"
  retention_in_days = 1
}

resource "aws_iam_role_policy_attachment" "backend-policy" {
  role       = aws_iam_role.backend-exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  depends_on = [
    aws_iam_role.backend-exec,
  ]
}

resource "aws_apigatewayv2_integration" "backend" {
  api_id = data.aws_apigatewayv2_api.core.id

  integration_uri    = aws_lambda_function.backend.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_lambda_permission" "api-gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.backend.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${data.aws_apigatewayv2_api.core.execution_arn}/*/*"
}

resource "aws_apigatewayv2_route" "GET_hello" {
  api_id = data.aws_apigatewayv2_api.core.id

  route_key = "GET /hello"
  target    = "integrations/${aws_apigatewayv2_integration.backend.id}"
}
