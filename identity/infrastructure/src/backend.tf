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

resource "aws_lambda_function" "backend" {
  function_name = local.BACKEND_NAME

  s3_bucket = data.aws_s3_bucket.resource-sharing.id
  s3_key    = "template/lambda-default.zip"
  source_code_hash = base64sha256("NO NEED")

  runtime = "python3.9"
  handler = "default.handler"

  role = aws_iam_role.backend-exec.arn

  lifecycle {
    ignore_changes = [
      "s3_bucket",
      "s3_key",
      "source_code_hash",  # will be deployed by workflow
    ]
  }
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
