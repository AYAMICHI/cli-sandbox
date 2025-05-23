import pandas as pd
import streamlit as st
from src.cli_sandbox.commands.greet import generate_greetings
from src.cli_sandbox.commands.save import save_greetings
from src.cli_sandbox.commands.load import load_greetings
from src.cli_sandbox.commands.log import save_log
from src.cli_sandbox.commands.log import (
    load_logs,
    convert_logs_to_csv,
    upload_logs_to_google_sheets,
    convert_logs_to_dataframe
)
from src.cli_sandbox.version import __version__
import os
from dotenv import load_dotenv
from pathlib import Path
import glob
import altair as alt


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
    st.markdown("### 🔍 ログを絞り込んで表示")
    filter_name = st.text_input("名前でフィルター（空欄で全件表示）", value="")
    filter_date = st.text_input("日付でフィルター(例: 2025-05-18)", value="")
    
    if st.button("🔍 フィルターを検索"):
        logs = load_logs()
        if logs:
            filtered_logs = []
            for log in logs:
                name_match = filter_name in log["name"] if filter_name else True
                date_match = filter_date in log["timestamp"] if filter_date else True
                if name_match and date_match:
                    filtered_logs.append(log)
                    
            st.success(f"🔎 該当ログ: {len(filtered_logs)} 件")
            
            if filtered_logs:
                for log in filtered_logs[::-1]:  # 最新のログから表示
                    st.write(f"🕒 {log['timestamp']} | 🙋‍♂️ {log['name']} | 🔁 {log['repeat']}")
                    for msg in log["messages"]:
                        st.markdown(f"- {msg}")
                    st.markdown("---")    
            else:
                st.info("❌ 該当するログはありません。")
        else:
            st.info("📭 ログがまだありません。")
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
    json_files = glob.glob("*.json")
    
    if json_files:
        selected_file = st.selectbox("☁️ アップロードするログファイルを選んでください", json_files)
    
        if st.button("☁️ Google Sheetsにアップロード"):
            try:
                # Google Sheetsにアップロード
                success = upload_logs_to_google_sheets(json_file=selected_file)
                if success:
                    st.success("✅ Google Sheetsにアップロードしました。")
                else:
                    st.error("❌ アップロードに失敗しました。usage_log.jsonが存在するか確認してください。")
            except FileNotFoundError:
                st.error("❌ ファイルが存在しません。")
    else:
        st.info("📭 アップロード可能なファイルが存在しません。")
        
st.markdown("### 名前ごとの累計挨拶回数グラフ")

df = convert_logs_to_dataframe()
if not df.empty:
    # 日付だけに変換
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    
    # 各日付ごとの回数を合計
    daily_counts = df.groupby(["date", "name"])["repeat"].sum().reset_index()
    
    # Altair 折れ線グラフ
    chart = alt.Chart(daily_counts).mark_line(point=True).encode(
        x=alt.X('date:T', title="日付"),
        y=alt.Y('repeat:Q', title="挨拶回数"),
        tooltip=['date', 'repeat']
    ).properties(
        width=600,
        height=300,
        title="日付ごとの挨拶回数推移"
    )
    st.altair_chart(chart, use_container_width=True)
    
    # name_counts = df.groupby("name")["repeat"].sum().reset_index()
    # # グラフの作成
    # chart = alt.Chart(name_counts).mark_bar().encode(
    #     x=alt.X('repeat:Q', title="挨拶回数"),
    #     y=alt.Y('name:N', sort='-x', title="名前"),
    #     tooltip=['name', 'repeat']
    # ).properties(
    #     width=500,
    #     height=300,
    #     title="名前と別の累計挨拶回数"
    # )
    
    # st.altair_chart(chart, use_container_width=True)
else:
    st.info("📭 表示できるログがまだありません。")
    
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