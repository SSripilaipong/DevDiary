resource "aws_apigatewayv2_api" "api-gateway" {
  name          = var.GLOBAL_PREFIX
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "api-gateway" {
  api_id = aws_apigatewayv2_api.api-gateway.id
  name        = var.GLOBAL_PREFIX
  auto_deploy = true
}
