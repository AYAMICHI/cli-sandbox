from typer.testing import CliRunner
from cli_sandbox.main import app

runner = CliRunner()

def test_greet_cli():
    result = runner.invoke(app, ["greet", "--name", "太郎", "--repeat", "2"])
    assert result.exit_code == 0
    assert "こんにちは, 太郎さん！" in result.stdout