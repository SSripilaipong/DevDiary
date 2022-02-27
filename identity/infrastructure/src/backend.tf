resource "aws_lambda_function" "backend" {
  function_name = "${var.GLOBAL_PREFIX}-identity-backend"

  s3_bucket = data.aws_s3_bucket.resource-sharing.id
  s3_key    = "template/lambda-default.zip"

  runtime = "python3.9"
  handler = "default.handler"

  source_code_hash = base64sha256("NO NEED")

  role = aws_iam_role.backend-exec.arn
}

resource "aws_cloudwatch_log_group" "backend" {
  name = "/aws/lambda/${aws_lambda_function.backend.function_name}"
  retention_in_days = 1
}

resource "aws_iam_role" "backend-exec" {
  name = aws_lambda_function.backend.function_name

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

resource "aws_iam_role_policy_attachment" "backend-policy" {
  role       = aws_iam_role.backend-exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
