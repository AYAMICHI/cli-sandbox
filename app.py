import streamlit as st
from src.cli_sandbox.commands.greet import generate_greetings
from src.cli_sandbox.commands.save import save_greetings
from src.cli_sandbox.commands.load import load_greetings
import os
from dotenv import load_dotenv
from pathlib import Path
import glob


load_dotenv()  # .envファイルを読み込む

st.set_page_config(
    page_title="挨拶ツール",
    page_icon="👋",
    layout="centered",
)
st.title("👋 挨拶ジェネレーター")
st.caption("名前を入力して、繰り返し挨拶を生成・保存・ダウンロードできるツールです。")
st.markdown("---")

# * 挨拶入力セクション
st.header("✍️ 挨拶を生成する")

col, col2, col3 = st.columns(3)

with col:
    name = st.text_input("名前", value=os.getenv("DEFAULT_NAME", "ゲスト"))
with col2:
    repeat = st.slider("回数", 1, 10, int(os.getenv("GREETING_REPEAT", 1)))
with col3:
    upper = st.checkbox("大文字にする")

col4, col5 = st.columns([3, 1])
with col4:
    # 保存ファイル名の入力
    file_name_input = st.text_input("保存ファイル名:", value="greetings.json")
#　ファイル名を整える(.jsonがなければつける)
file_name = file_name_input if file_name_input.endswith(".json") else file_name_input + ".json"

#  * 実行と保存
if st.button("🚀 挨拶する"):
    messages = generate_greetings(name, repeat, upper)
    # 表示
    for msg in messages:
        st.success(msg)
    # 保存
    save_greetings(name, messages, file=file_name)
    st.session_state["last_saved_file"] = file_name  # 最後に保存したファイル名をセッションステートに保存
    st.info(f"✅ {file_name}に保存しました。")

#  * ログ表示セクション
st.header("📖 保存されたメッセージを表示")
if st.button("📂 ログを読み込む"):
    messages = load_greetings(file_name)
    if messages:
        st.info("📄 保存されたメッセージ一覧 :")
        for msg in messages:
            st.write(f"- {msg}")
    else:
        st.warning("⚠️ 指定されたファイルが見つかりません。")

# * ダウンロードセクション
st.header("📥 JSONファイルをダウンロード")
# JSONファイル一覧
json_files = glob.glob("*.json")

if json_files:
    selected_file = st.selectbox("ファイル選択", json_files)
    file_path = Path(selected_file)
    with open(file_path, "rb") as f:
        st.download_button(
            label=f"📥 {selected_file} をダウンロード",
            data=f,
            file_name=selected_file,
            mime="application/json"
        )
else:
    st.info("💾 保存された .json ファイルが見つかりませんでした。")