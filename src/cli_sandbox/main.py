import typer
from cli_sandbox.commands import greet, goodbye, save, load, save_json, load_json


app = typer.Typer(help="これはあなた専用の挨拶CLIです。")

__version__ = "0.1.0"

# ← versionコマンドとして分離（ここが新ポイント）
@app.command(name="version", help="バージョン情報を表示します。")
def version():
    """バージョン情報を表示するコマンド"""
    typer.echo(f"greet-cli v{__version__}")
    
#各コマンドを登録する
greet.register(app)
goodbye.register(app)
save.register(app)
load.register(app)
save_json.register(app)
load_json.register(app)


if __name__ == "__main__":
    app()
# # --version　オプションに対応するためのエントリ関数
# @app.callback()
# def main(
#     version: bool = typer.Option(
#         None,
#         callback=lambda v: print(f"greet-cli v{__version__}") or raise_exit(),
#         is_eager=True,
#         help="バージョン情報を表示して終了。"
#     )
# ):
#     pass
# def raise_exit():
#     raise typer.Exit()