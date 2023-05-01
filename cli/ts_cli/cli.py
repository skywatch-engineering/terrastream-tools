import click
from commands.api_products import ApiProductsCommands


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    TS-Utils Command Line Interface
    """
    if not ctx.invoked_subcommand:
        click.secho(ctx.get_help(), fg="green")
        ctx.exit()


@cli.command("configure")
def configure():
    """
    TODO: Set configurations for tenant name, account id, api urls, user name/password and stage
    """
    pass


@cli.command("create-custom-product")
@click.option("--payload", "-p", required=True, type=click.Path(exists=True))
@click.option("--input-file", "-i", required=True, type=click.Path(exists=True))
@click.option("--skip-upload", "-s", required=False, is_flag=True, default=False)
@click.option("--sequential", "-l", required=False, is_flag=True, default=False)
@click.option("--thread-num", "-t", required=False, type=int, default=10)
@click.option("--chunk-size-mb", "-c", required=False, type=int, default=50)
def api_create_custom_product(
    payload, input_file, skip_upload, sequential, thread_num, chunk_size_mb
):
    """
    Api: create custom product for a given request/result,
    uploads multipart product using single or multiple threads
    and confirms the product creation/upload calling TS api endpoints

    --payload indicates the file to read details of the custom product
    --input-file indicates the file to be uploaded to s3
    --skip-upload ignores the file upload
    --sequential runs the upload in a single thread
    --thread-num number of concurrent threads to upload file to s3
    """
    parallel = not sequential
    ApiProductsCommands().create_custom_product(
        payload, input_file, skip_upload, parallel, thread_num, chunk_size_mb
    )


if __name__ == "__main__":
    cli()  # type: ignore # noqa
