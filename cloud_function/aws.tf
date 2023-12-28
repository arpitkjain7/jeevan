variable "env_name" {
  description = "pilot"
}

data "aws_ecr_repository" "cliniq360" {
  name = "cliniq360"
}

resource "aws_lambda_function" "send_data_function" {
  function_name = "send-data-${var.env_name}"
  timeout       = 5 # seconds
  image_uri     = "022262065730.dkr.ecr.ap-south-1.amazonaws.com/cliniq360:terraPOC"
  package_type  = "Image"

  role = aws_iam_role.send_data_function_role.arn

  environment {
    variables = {
      ENVIRONMENT = var.env_name
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
