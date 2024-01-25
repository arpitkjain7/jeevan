variable "env_name" {
  description = "pilot"
}
data "aws_ecr_authorization_token" "token" {}

resource "aws_ecr_repository" "cliniq360" {
  name                 = "cliniq360"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  provisioner "local-exec" {
    # This is a 1-time execution to put a dummy image into the ECR repo, so 
    #    terraform provisioning works on the lambda function. Otherwise there is
    #    a chicken-egg scenario where the lambda can't be provisioned because no
    #    image exists in the ECR
    command = <<EOF
      docker login ${data.aws_ecr_authorization_token.token.proxy_endpoint} -u AWS -p ${data.aws_ecr_authorization_token.token.password}
      docker pull alpine
      docker tag alpine ${aws_ecr_repository.cliniq360.repository_url}:0.0
      docker push ${aws_ecr_repository.cliniq360.repository_url}:0.0
      EOF
  }
}

# data "aws_ecr_repository" "cliniq360" {
#   name                 = "cliniq360"
#   image_tag_mutability = "MUTABLE"
#   provisioner "local-exec" {
#     command = <<-EOT
#       docker pull alpine
#       docker tag alpine dummy_container
#       docker push dummy_container
#     EOT
#   }
# }

resource "aws_lambda_function" "send_data_function" {
  function_name = "send-data-${var.env_name}"
  timeout       = 60 # seconds
  image_uri     = "${aws_ecr_repository.cliniq360.repository_url}:0.0"
  package_type  = "Image"
  role          = aws_iam_role.send_data_function_role.arn

  environment {
    variables = {
      callback_base_url = var.env_name
    }
  }
}

resource "aws_iam_role" "send_data_function_role" {
  name = "send-data-${var.env_name}"

  assume_role_policy = jsonencode({
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}
resource "aws_lambda_function" "generate_encryption_key_function" {
  function_name = "generate-encryption-key-${var.env_name}"
  timeout       = 60 # seconds
  image_uri     = "${aws_ecr_repository.cliniq360.repository_url}:0.0"
  package_type  = "Image"

  role = aws_iam_role.generate_encryption_key_role.arn

  environment {
    variables = {
      ENVIRONMENT = var.env_name
    }
  }
}

resource "aws_iam_role" "generate_encryption_key_role" {
  name = "generate-encryption-key-${var.env_name}"

  assume_role_policy = jsonencode({
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}
