# Getting Started With Pulumi Python - AWS VPC and EC2 Instance Example

Pulumi is a modern infrastructure as code platform that allows you to use familiar programming languages and tools to build, deploy, and manage cloud infrastructure.

## AWS Credentials

This example utilizes AWS, so you'll need to generate and set your credentials accordingly.

## Prerequisites

In order to use Pulumi with Python, you will need the following.

- [Pulumi](https://www.pulumi.com/docs/get-started/install/)
- [Language Runtime](https://www.pulumi.com/docs/get-started/aws/begin/#install-language-runtime)
  - [Python](https://www.python.org/downloads/) >= 3.7+

## Initialization of Python Environment

[Using Pulumi PyPI Packages](https://www.pulumi.com/docs/intro/languages/python/)

## Initialization of Pulumi Project

Use existing code example:
1. Clone git respo
2. cd into project
3. `pulumi login --local` (Uses the filesystem backend to store your checkpoint files locally on your machine.)
4. `pulumi up`
5. Enter a stack name when prompted
6. Review proposed changes and confirm execution
7. `pulumi destroy`