data "aws_caller_identity" "current" {}

data "aws_ecr_repository" "priceChecker" {
  name                 = "price-checker"
}

data "aws_iam_role" "docker-price-checker-role" {
  name = "docker-price-checker-role-umwe0r8o"
}

resource "aws_lambda_function" "docker-price-checker_tf" {
  function_name = "docker-price-checker_tf"
  timeout           = 45 # seconds
  image_uri         = "${data.aws_ecr_repository.priceChecker.repository_url}:latest"
  package_type      = "Image"
  memory_size       = "1024"
  
  ephemeral_storage {
    size = "800"
  }


  role = data.aws_iam_role.docker-price-checker-role.arn

  environment {
    variables = {
      FLIGHT1 = "4501",
      FLIGHT2 = "3157",
      FLIGHT3 = "2343"
      URL1 = "https://www.google.com/travel/flights/booking?tfs=CBwQAhpGEgoyMDI0LTEwLTE1IiAKA0xHQRIKMjAyNC0xMC0xNRoDREFMKgJXTjIENDUwMWoNCAISCS9tLzAyXzI4NnIHCAESA0RBTEABSAFwAYIBCwj___________8BmAEC",
      URL2 = "https://www.google.com/travel/flights/booking?tfs=CBwQAhpGEgoyMDI0LTEwLTIyIiAKA0RBTBIKMjAyNC0xMC0yMhoDTEdBKgJXTjIEMzE1N2oHCAESA0RBTHINCAISCS9tLzAyXzI4NkABSAFwAYIBCwj___________8BmAEC"
      URL3 = "https://www.google.com/travel/flights/booking?tfs=CBwQAhpAEgoyMDI0LTA5LTE2IiAKA1BIWBIKMjAyNC0wOS0xNhoDREFMKgJXTjIEMjM0M2oHCAESA1BIWHIHCAESA0RBTEABSAFwAYIBCwj___________8BmAEC"
    }
  }
}

resource "aws_ecr_lifecycle_policy" "priceCheckerPolicy" {
    repository = data.aws_ecr_repository.priceChecker.name
    
    policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Expire untagged images older than 1 day",
            "selection": {
                "tagStatus": "any",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

data "aws_iam_role" "schedulerRole" {
  name = "Amazon_EventBridge_Scheduler_LAMBDA_b4c9a7d45d"
}

resource "aws_scheduler_schedule" "FlightPriceCheckLambdaSchedule" {
  name       = "FlightPriceCheckLambdaTF"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 */6 ? * * *)"

  schedule_expression_timezone = "America/New_York"

  start_date = "2024-07-27T05:50:00Z"

  target {
    arn      = aws_lambda_function.docker-price-checker_tf.arn
    role_arn = data.aws_iam_role.schedulerRole.arn

    retry_policy {
    maximum_event_age_in_seconds = 900
    maximum_retry_attempts = 1
    }
  }
}