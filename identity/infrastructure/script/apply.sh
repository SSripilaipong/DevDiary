#!/bin/bash
if [ -z "${AWS_REGION}" ] || [ -z "${TF_BACKEND_BUCKET_NAME}" ] || [ -z "${TF_BACKEND_BUCKET_PATH}" ]; then
  echo ERROR: variables needed to be set: AWS_REGION \(\""$AWS_REGION"\"\), TF_BACKEND_BUCKET_NAME \(\""$TF_BACKEND_BUCKET_NAME"\"\), TF_BACKEND_BUCKET_PATH \(\""$TF_BACKEND_BUCKET_PATH"\"\) 1>&2
  exit 1
fi

sed s/AWS_REGION/"$AWS_REGION"/g ../template/terraform.template.tf |
  sed s/TF_BACKEND_BUCKET_NAME/"$TF_BACKEND_BUCKET_NAME"/g |
  sed s:TF_BACKEND_BUCKET_PATH:"$TF_BACKEND_BUCKET_PATH":g > terraform.tf
terraform init
terraform apply --auto-approve
