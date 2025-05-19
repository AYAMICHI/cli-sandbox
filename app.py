import streamlit as st
from src.cli_sandbox.commands.greet import generate_greetings
from src.cli_sandbox.commands.save import save_greetings
from src.cli_sandbox.commands.load import load_greetings
from src.cli_sandbox.commands.log import save_log
from src.cli_sandbox.commands.log import load_logs
from src.cli_sandbox.commands.log import convert_logs_to_csv
from src.cli_sandbox.commands.log import upload_logs_to_google_sheets
from src.cli_sandbox.version import __version__
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
tab1, tab2, tab3 = st.tabs([
    "✍️ 挨拶を生成する",
    "📂 保存ファイル表示",
    "📊 使用履歴表示"
])

# --- タブ1 : 挨拶生成 ---
with tab1:
    st.markdown("### ✍️ 挨拶を生成する")
    st.markdown("---")
    with st.container():
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
        save_log(name, repeat, messages)  # ログ保存
        st.session_state["last_saved_file"] = file_name  # 最後に保存したファイル名をセッションステートに保存
        st.info(f"✅ {file_name}に保存しました。")
# --- タブ2 : 保存ファイル表示 ---
with tab2:
    st.markdown("### 📂 保存ファイル表示")
    st.markdown("---")
    if st.button("📄 表示する"):
        messages = load_greetings(file_name)
        if messages:
            st.info("📄 保存されたメッセージ一覧 :")
            for msg in messages:
                st.write(f"- {msg}")
        else:
            st.warning("⚠️ 指定されたファイルが見つかりません。")

# --- タブ3 : 使用履歴表示 ---
with tab3:
    st.markdown("### 📊 使用履歴表示")
    st.markdown("---")
    if st.button("📂 ログを表示"):
        logs = load_logs()
        if logs:
            st.success(f"🔎 過去のログ {len(logs)} 件を表示中")
            for log in logs[::-1]:  # 最新のログから表示
                st.write(f"🕒 {log['timestamp']} | 🔁 {log['repeat']}")
                for msg in log["messages"]:
                    st.markdown(f"- {msg}")
                st.markdown("---")
        else:
            st.info("📭 ログファイルがまだありません。")
    
    # CSVダウンロードボタン
    df = convert_logs_to_csv()
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 CSVファイルをダウンロード",
            data=csv,
            file_name="usage_log.csv",
            mime="text/csv"
        )
    else:
        st.info("📭 CSVファイルがまだありません。")
    
    # Google Sheetsアップロードボタン
    if st.button("☁️ Google Sheetsにアップロード"):
        success = upload_logs_to_google_sheets()
        if success:
            st.success("✅ Google Sheetsにアップロードしました。")
        else:
            st.error("❌ アップロードに失敗しました。usage_log.jsonが存在するか確認してください。")
        
        
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

# * バージョン表示
st.markdown("---")
st.caption(f"🛠️ アプリバージョン: v{__version__}")