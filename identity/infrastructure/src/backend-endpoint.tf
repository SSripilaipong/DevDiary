resource "aws_apigatewayv2_integration" "register" {
  api_id = data.aws_apigatewayv2_api.core.id

  integration_uri    = aws_lambda_function.backend.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  payload_format_version = "2.0"

  request_parameters = {
    "overwrite:header.X-Service-Operation": "IdentityRegister",
  }
}

resource "aws_apigatewayv2_route" "register" {
  api_id = data.aws_apigatewayv2_api.core.id

  route_key = "POST /users/register"
  target    = "integrations/${aws_apigatewayv2_integration.register.id}"
}
