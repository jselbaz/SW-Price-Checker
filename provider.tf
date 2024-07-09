terraform {
 required_providers {
   aws = {
     source  = "hashicorp/aws"
     version = "~> 5.0"
   }
 }

  backend "s3" {
    bucket = "selbaz-terraform-config"
    key    = "aws-automation/terraform.tfstate"
    encrypt = true
    region = "us-east-1"
    dynamodb_table = "selbaz-terraform-config"
  }
}