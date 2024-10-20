import typer

app = typer.Typer()

import subprocess

def run_command(command: str):
    print(f"Running: '{command}'")
    subprocess.run(command, shell=True)


@app.command()
def register_ecr(
    aws_region: str = "us-east-1",
    aws_account: str = "537741441658"
):
    login_ecr = f"aws ecr get-login-password --region {aws_region} | docker login --username AWS --password-stdin {aws_account}.dkr.ecr.us-east-1.amazonaws.com"
    run_command(login_ecr)


@app.command()
def create_docker_repository(
    docker_repository: str = "docker-image",
    aws_region: str = "us-east-1"
): 
    create_repository = f"aws ecr create-repository --repository-name {docker_repository} --region {aws_region}"
    run_command(create_repository)


@app.command()
def make_lambda_function(
    function_name: str,
    image_name: str,
    folder: str,
    docker_repository: str = "docker-image",
    aws_account: str = "537741441658",
    aws_region: str ="us-east-1",
    role_name: str ="service-role/minhalambda-role-3wpi1o38"
):
    build_image = f"docker build -t {docker_repository}:{image_name} {folder}"
    tag_image = f"docker tag {docker_repository}:{image_name} {aws_account}.dkr.ecr.{aws_region}.amazonaws.com/{docker_repository}:{image_name}"
    push_image = f"docker push {aws_account}.dkr.ecr.{aws_region}.amazonaws.com/{docker_repository}:{image_name}"
    create_function = f"""aws lambda create-function \
      --function-name {function_name} \
      --package-type Image \
      --code ImageUri={aws_account}.dkr.ecr.{aws_region}.amazonaws.com/{docker_repository}:{image_name} \
      --role arn:aws:iam::{aws_account}:role/{role_name}
    """
    run_command(build_image)
    run_command(tag_image)
    run_command(push_image)
    run_command(create_function)

if __name__ == "__main__":
    app()