from obspy.clients.fdsn import Client
from obspy import UTCDateTime

# 1. 定義時間和台站參數
# 起始時間: 2025/10/07 23:52:12
starttime_str = "2025-10-07T23:52:12.000Z"
duration_seconds = 120  # 持續時間: 120 秒

# 轉換為 ObsPy 的 UTCDateTime 物件
starttime = UTCDateTime(starttime_str)
endtime = starttime + duration_seconds

# 選擇一個範例台站和通道 (Network.Station.Location.Channel)
network = "IU"    # 國際台網 (International Network)
station = "ANMO"  # Albuquerque, New Mexico
location = "00"   # Location ID
channel = "LHZ"   # Long-period High-gain Vertical Channel

# 檔案名稱
filename_mseed = f"{network}_{station}_{channel}_{starttime.date}.mseed"
filename_plot = f"{network}_{station}_{channel}_{starttime.date}.png"

# 2. 連接到 FDSN 客戶端
client = Client("IRIS")
print(f"正在連接 IRIS FDSN 服務器...")

# 3. 抓取波形數據 (Waveform Data)
try:
    # get_waveforms 函數用於抓取波形資料
    st = client.get_waveforms(
        network=network,
        station=station,
        location=location,
        channel=channel,
        starttime=starttime,
        endtime=endtime,
        attach_response=True # 包含儀器響應信息
    )
    print(f"\n成功抓取 {len(st)} 條 Trace 資料。")
    print(st) # 輸出 Stream 物件的摘要信息

    # 4. 繪製波形圖 (Plotting)
    print(f"\n正在繪製波形圖並儲存為 {filename_plot}...")
    
    # ObsPy Stream 物件的 plot() 方法
    st.plot(
        outfile=filename_plot,      # 儲存繪圖結果
        size=(1200, 400),           # 圖片大小 (寬, 高)
        title=f"Waveform from {network}.{station}.{location}.{channel}",
        show=False                  # 在 Notebook 中不顯示，直接儲存
    )
    
    # 5. 儲存 MiniSEED 數據 (Saving)
    print(f"正在儲存 MiniSEED 數據為 {filename_mseed}...")
    st.write(filename_mseed, format="MSEED")
    
    print("\n任務完成！數據和圖片已儲存。")
    
except Exception as e:
    print(f"\n抓取數據時發生錯誤: {e}")
    print("請檢查指定的台網、台站和時間段是否有數據可用。")