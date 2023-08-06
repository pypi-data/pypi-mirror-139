# pyterrafile

Manages external Terraform modules, controlled by a `Terrafile`.

This is basically a Python version of the tool described at [http://bensnape.com/2016/01/14/terraform-design-patterns-the-terrafile/](http://bensnape.com/2016/01/14/terraform-design-patterns-the-terrafile/)

Additionally, python-terrafile supports modules from the Terraform Registry, as well as modules in local directories identified by a relative path starting with either `./` or `../` or an absolute path starting with `/`.

## Naming

This project was forked from [https://github.com/claranet/python-terrafile](claranet/python-terrafile). It is first release since version 0.5.0 on PyPI as `pyterrafile`.

## Installation

```shell
pip install pterrafile
```

## Usage

```shell
pterrafile [path]
```

If `path` is provided, it must be the path to a `Terrafile` file, or a directory containing one. If not provided, it looks for the file in the current working directory.

## Examples

```yaml
# Terraform Registry module
terraform-aws-lambda:
  source: "claranet/lambda/aws"
  version: "0.7.0"

# Git module (HTTPS)
terraform-aws-lambda:
  source: "https://github.com/claranet/terraform-aws-lambda.git"
  version: "v0.7.0"

# Git module (SSH)
terraform-aws-lambda:
  source: "git@github.com:claranet/terraform-aws-lambda.git"
  version: "v0.7.0"

# Local directory module
terraform-aws-lambda:
  source: "../../modules/terraform-aws-lambda"
```

This project add quilt support for patching management.
