import typer

from fractalgebra.helpers import Fractalgebra

helpstring = """two or more rational numbers (e.g. 2/3, -2/3, 1_1/2, -1_1/2, 5)
separated by a spaces and an operator (one of +, -, *, or /)
        e.g: 8 * 1/2 - -18/3 / -1_10/5 => 1
    
** note that mixed number with a negative fraction (e.g. 4_-1/2) is NOT a rational number
    """

app = typer.Typer()


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def main(
    ctx: typer.Context,
    input: str = typer.Argument("", help=helpstring, show_default=False),
):
    """
    Perform basic arithmatic on two or more fractions (or mixed number)
    using the pattern <fraction> <operator> <fraction> <operator> <fraction>

    """
    # typer.echo(ctx.args)
    # typer.echo(ctx.params)
    input_list = [ctx.params["input"]] + ctx.args
    # typer.echo(input_list)

    try:
        fractalgebra_answer: str = Fractalgebra.solve(input_list)
        typer.echo(f"= {fractalgebra_answer}")
    except Exception as e:
        typer.echo(f"Error: {e}")


def calc():
    app()
