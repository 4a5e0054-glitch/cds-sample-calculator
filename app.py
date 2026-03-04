import streamlit as st
from datetime import datetime, time
from datetime import datetime
from zoneinfo import ZoneInfo

st.set_page_config(page_title="試吃用量計算", layout="centered")
st.title("CDS 試吃用量計算器")

DAY_HOURS = 10.5  # 全天固定時數

# --- 開始時間：兩顆按鈕 ---
st.subheader("開始時間（按一下就填好）")

if "start_time" not in st.session_state:
    st.session_state.start_time = None

c1, c2 = st.columns(2)
with c1:
    if st.button("09:15"):
        st.session_state.start_time = time(9, 15)
with c2:
    if st.button("08:45"):
        st.session_state.start_time = time(8, 45)

# 顯示目前選到的開始時間
if st.session_state.start_time is None:
    st.info("請先按 09:15 或 08:45 選擇開始時間")
else:
    st.success(f"已選擇開始時間：{st.session_state.start_time.strftime('%H:%M')}")

# --- 輸入 ---
st.subheader("輸入")
initial = st.number_input("初始試吃量", min_value=0.0, step=0.5, format="%.2f")
remain  = st.number_input("剩餘試吃量", min_value=0.0, step=0.5, format="%.2f")

# --- 計算函式 ---
def elapsed_hours_from_start(start_t: time) -> float:
    """用『今天的現在時間』與 start_t 計算經過小時數，若跨午夜則自動補 24 小時。"""
    now = datetime.now(ZoneInfo("Asia/Taipei"))
    start_dt = datetime.combine(now.date(), start_t)
    delta = now - start_dt
    hours = delta.total_seconds() / 3600.0
    if hours < 0:
        hours += 24.0
    return hours

# --- 計算 & 顯示 ---
st.subheader("結果")

if st.session_state.start_time is None:
    st.warning("先選開始時間後才會計算。")
else:
    elapsed = elapsed_hours_from_start(st.session_state.start_time)

    used = max(initial - remain, 0.0)

    per_hour = 0.0
    if elapsed > 0:
        per_hour = used / elapsed

    predict = per_hour * DAY_HOURS
    diff = predict - initial  # 預估差額 = 預估用量 - 初始量

    st.write(f"目前時間：{datetime.now().strftime('%H:%M:%S')}")
    st.write(f"已進行時間_小時：{elapsed:.2f}")
    st.write(f"已使用量：{used:.2f}")
    st.write(f"每小時用量：{per_hour:.2f}")
    st.write(f"全天預估用量（{DAY_HOURS} 小時）：{predict:.2f}")
    st.write(f"預估差額（預估用量 - 初始量）：{diff:.2f}")

    if diff > 0:
        st.error("❌ 試吃品不足（照目前速度，可能不夠）")
    else:
        st.success("✅ 試吃品足夠（照目前速度，應該夠用）")

