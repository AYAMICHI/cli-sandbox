import PyInstaller.__main__

PyInstaller.__main__.run([
    "src/cli_sandbox/main.py",
    "--name=cli",
    "--onefile",
    "--console",
])