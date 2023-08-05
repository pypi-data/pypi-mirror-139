import json

import typer
from terrasnek.api import TFC

from .terraform_cloud import get_workspace_output, get_workspace_outputs

app = typer.Typer()
tfc_token_opt = typer.Option(
    default=...,
    envvar=["TFE_TOKEN", "TFC_TOKEN"],
    help="Terraform Cloud access token",
    is_eager=True,
)


@app.command(name="get-output")
def get_output_cli(
    workspace_ref: str = typer.Argument(
        default=...,
        help="Reference to a Terraform Cloud workspace in "
        "'<org_name>/<workspace_name>/<output_name>' format.",
    ),
    tfc_token: str = tfc_token_opt,
):
    """Get the value of a Terraform Cloud workspace output.

    For example: `python -m tfc_utils get-output hashicorp/primary-workspace/instance_ip_addr`
    """
    tfc = TFC(api_token=tfc_token)
    try:
        org, workspace, output = workspace_ref.split("/")
    except ValueError as e:
        raise ValueError(
            "Invalid Terraform output reference, must be in "
            "'<org_name>/<workspace_name>/<output_name>' format"
        ) from e
    output = get_workspace_output(tfc, org, workspace, output)
    typer.echo(output)


@app.command(name="get-workspace-outputs")
def get_workspace_outputs_cli(
    tfc_token: str = tfc_token_opt,
    tfc_organization: str = typer.Option(
        default=...,
        envvar=["TFC_ORGANIZATION", "TFE_ORGANIZATION"],
        help="Terraform Cloud organization name",
    ),
    tfc_workspace: str = typer.Option(
        default=...,
        envvar=["TFC_WORKSPACE", "TFE_WORKSPACE"],
        help="Terraform Cloud workspace name",
    ),
    prefix: str = typer.Option(
        default="",
        help="Optional prefix for filtering out outputs (case-sensitive)",
    ),
    to_upper: bool = typer.Option(
        default=False,
        help="Convert output names to uppercase",
    ),
):
    """Get outputs of a Terraform Cloud workspace as JSON string."""
    tfc = TFC(api_token=tfc_token)
    outputs_dict = get_workspace_outputs(
        tfc=tfc,
        organization_name=tfc_organization,
        workspace_name=tfc_workspace,
        prefix=prefix,
        preserve_case=not to_upper,
    )
    typer.echo(json.dumps(outputs_dict, separators=(",", ":")))


@app.callback()
def callback():
    """A CLI helper tool for Terraform Cloud."""
