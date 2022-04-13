resource "aws_lambda_event_source_mapping" "relay" {
  event_source_arn  = aws_dynamodb_table.db.stream_arn
  function_name     = aws_lambda_function.backend.arn
  starting_position = "LATEST"
  function_response_types = ["ReportBatchItemFailures"]
  batch_size = 10
  maximum_retry_attempts = 1  # experimental

  depends_on = [
    aws_dynamodb_table.db,
    aws_lambda_function.backend,
    aws_iam_role_policy.db-policy,
  ]
}

resource "aws_iam_role_policy" "publish-topic-RegistrationEmailNeededToBeConfirmedEvent" {
  role = aws_iam_role.backend-exec.name

  policy = jsonencode({
    Statement = [
      {
        Sid = "PublishTopicRegistrationEmailNeededToBeConfirmedEvent"
        Effect = "Allow"
        Action = [
          "sns:Publish",
        ]
        Resource = aws_sns_topic.RegistrationEmailNeededToBeConfirmedEvent.arn
      },
    ]
  })

  depends_on = [
    aws_sns_topic.RegistrationEmailNeededToBeConfirmedEvent,
  ]
}
