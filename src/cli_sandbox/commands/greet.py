import typer
import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

load_dotenv() # .envファイルを読み込む

def register(app: typer.Typer):
    @app.command(help="環境変数を使った挨拶")
    def greet_env():
        name = os.getenv("DEFAULT_NAME", "名無し")
        repeat = int(os.getenv("GREETING_REPEAT", 1))
        
        for _ in range(repeat):
            typer.echo(f"こんにちは, {name}さん！")
        
    @app.command(help="あなたの名前を指定して挨拶します。")
    def greet(
        name :str = typer.Option(None, "--name", "-n", help="あなたの名前"),
        upper : bool = typer.Option(False, "--upper", "-u", help="大文字で表示"),
        repeat : int = typer.Option(1, "--repeat", "-r", help="繰り返し回数"),
        use_config : bool = typer.Option(False, "--use-config", help="config.yamlを使用")
    ):
        if use_config:
            config_path = Path("config.yaml")
            if not config_path.exists():
                typer.secho("❌ config.yamlが見つかりません。", fg="red")
                raise typer.Exit()
            
            with open(config_path, "r", encoding="utf-8") as f:
                try:
                    config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    typer.secho(f"⚠️ YAMLファイルの読み込みに失敗しました: {e}", fg="yellow")
                    raise typer.Exit()
            
            name = config.get("default_name", name)
            upper = config.get("uppercase", upper)
            repeat = config.get("repeat", repeat)
            
        if name is None:
            typer.secho("⚠️ 名前を指定されていません。", fg="red")
            raise typer.Exit()
        
        if upper:
            name = name.upper()
        
        for _ in range(repeat):
            print(f"こんにちは, {name}さん！")