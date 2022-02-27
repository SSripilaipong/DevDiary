data "archive_file" "lambda-default-handler" {
  type = "zip"
  source_dir  = "../template/lambda"
  output_path = "../template/lambda.zip"
}

resource "aws_s3_object" "lambda-default-handler" {
  bucket = aws_s3_bucket.resource-sharing.id

  key    = "template/lambda-default.zip"
  source = data.archive_file.lambda-default-handler.output_path

  etag = filemd5(data.archive_file.lambda-default-handler.output_path)
}
