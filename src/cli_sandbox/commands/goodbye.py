import typer

def register(app: typer.Typer):
    @app.command(help="丁寧に or ラフに別れを告げます")
    def goodbye(
        name :str = typer.Option(..., "--name", "-n"),
        polite : bool = typer.Option(False, "--polite", "-p")
    ):
        if polite:
            print(f"{name}さん,ごきげんよう。")
        else:
            print(f"じゃあな、{name}！")