resource "aws_dynamodb_table" "db" {
  name           = "${var.GLOBAL_PREFIX}-identity"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "_Partition"
  range_key       = "_SortKey"

  stream_enabled = true
  stream_view_type = "NEW_IMAGE"

  attribute {
    name = "_Partition"
    type = "S"
  }

  attribute {
    name = "_SortKey"
    type = "S"
  }

}

resource "aws_iam_role_policy" "db-policy" {
  role = aws_iam_role.backend-exec.name

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
        Resource = aws_dynamodb_table.db.arn
      },
    ]
  })

  depends_on = [
    aws_dynamodb_table.db,
  ]
}
