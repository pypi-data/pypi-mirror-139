"""Command-line interface."""
import cli
from erp_visard import PROJECT_ROOT
from routines import read
from web import app
from web import layout
from web import plot


def main() -> None:
    """ERP Visual Wizard main function."""
    data = read.load_csv(PROJECT_ROOT / "data" / "demo.csv")
    fruit, amount, city = data.columns
    app.layout = layout.home(
        plot.bar(
            data=data,
            x=fruit,
            y=amount,
            color=city,
            barmode="group",
        )
    )
    cli.entrypoint(prog_name="erp-visard")  # pragma: no cover


main()
