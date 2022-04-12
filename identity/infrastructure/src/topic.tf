resource "aws_sns_topic" "RegistrationEmailNeededToBeConfirmedEvent" {
  name = "${var.GLOBAL_PREFIX}-Identity-RegistrationEmailNeededToBeConfirmedEvent"
}
