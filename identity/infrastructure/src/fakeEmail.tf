locals {
  FAKE_EMAIL_NAME = "${var.GLOBAL_PREFIX}-identity-fakeEmail"
}

resource "aws_iam_role" "fakeEmail-exec" {
  count = var.GLOBAL_PREFIX != "prod" ? 1 : 0

  name = local.FAKE_EMAIL_NAME

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

data "archive_file" "fakeEmail" {
  count = var.GLOBAL_PREFIX != "prod" ? 1 : 0

  type = "zip"
  source_dir  = "../../fakeEmail/src"
  output_path = "./fakeEmail.zip"
}

resource "aws_lambda_function" "fakeEmail" {
  count = var.GLOBAL_PREFIX != "prod" ? 1 : 0

  function_name = local.FAKE_EMAIL_NAME
  filename = data.archive_file.fakeEmail[0].output_path
  source_code_hash = data.archive_file.fakeEmail[0].output_base64sha256

  runtime = "python3.9"
  handler = "main.handler"
  timeout = 5

  environment {
    TABLE_NAME = aws_dynamodb_table.fakeEmail[0].name,
  }

  role = aws_iam_role.fakeEmail-exec[0].arn

  depends_on = [
    aws_iam_role.fakeEmail-exec,
    aws_dynamodb_table.fakeEmail,
    data.archive_file.fakeEmail,
  ]
}

resource "aws_cloudwatch_log_group" "fakeEmail" {
  count = var.GLOBAL_PREFIX != "prod" ? 1 : 0

  name = "/aws/lambda/${aws_lambda_function.fakeEmail[0].function_name}"
  retention_in_days = 1
}

resource "aws_iam_role_policy_attachment" "fakeEmail-policy" {
  count = var.GLOBAL_PREFIX != "prod" ? 1 : 0

  role       = aws_iam_role.fakeEmail-exec[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  depends_on = [
    aws_iam_role.fakeEmail-exec,
  ]
}

resource "aws_dynamodb_table" "fakeEmail" {
  count = var.GLOBAL_PREFIX != "prod" ? 1 : 0

  name           = local.FAKE_EMAIL_NAME
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }

}

resource "aws_iam_role_policy" "fakeEmail-dynamodb-policy" {
  count = var.GLOBAL_PREFIX != "prod" ? 1 : 0

  role = aws_iam_role.fakeEmail-exec[0].name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "ListAndDescribe"
        Effect = "Allow"
        Action = [
          "dynamodb:List*",
          "dynamodb:DescribeReservedCapacity*",
          "dynamodb:DescribeLimits",
          "dynamodb:DescribeTimeToLive",
        ]
        Resource = "*"
      },
      {
        Sid = "SpecificTable"
        Effect = "Allow"
        Action = [
          "dynamodb:BatchGet*",
          "dynamodb:DescribeStream",
          "dynamodb:DescribeTable",
          "dynamodb:Get*",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWrite*",
          "dynamodb:CreateTable",
          "dynamodb:Delete*",
          "dynamodb:Update*",
          "dynamodb:PutItem",
        ]
        Resource = aws_dynamodb_table.fakeEmail[0].arn
      },
    ]
  })

  depends_on = [
    aws_iam_role.fakeEmail-exec,
    aws_dynamodb_table.fakeEmail,
  ]
}
