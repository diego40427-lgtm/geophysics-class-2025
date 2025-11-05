import numpy as np

# --- 1. 定義常數 (Values in mGal, meter, degree) ---
# WGS84 橢球體參數 (用於計算理論重力 g_theo)
G_E = 978032.7  # 赤道重力 (mGal)
k = 0.0053024   # 重力扁率常數
k_prime = 0.0000059 # 另一個常數項 (用於1980年國際重力公式簡化形式)

# 修正項常數
FAA_GRADIENT = 0.3086  # 自由空氣梯度 (mGal/m)
BOUGUER_DENSITY = 2.67 # 陸地 Bouguer 校正密度 (g/cm^3)
BOUGUER_CONSTANT = 0.04192  # Bouguer 板校正常數 (mGal/(g/cm^3 * m))
WATER_DENSITY = 1.03 # 海水密度 (g/cm^3)

# --- 2. 輸入數據 ---
LATITUDE = 48.1195  # 緯度 (度 N)
ELEVATION = 487.9  # 高度 H (m) / 水深 D (m)
G_OBS = 980717.39 # 觀測重力 (mGal)

print(f"--- 重力站點數據 ---")
print(f"緯度 (phi): {LATITUDE:.4f} °N")
print(f"高度/水深: {ELEVATION:.1f} m")
print(f"觀測重力 (g_obs): {G_OBS:.2f} mGal\n")

# --- 3. 定義計算函數 ---

def theoretical_gravity(phi_deg):
    """計算理論重力 (g_theo)"""
    phi_rad = np.deg2rad(phi_deg)
    sin2_phi = np.sin(phi_rad)**2
    sin4_phi = np.sin(phi_rad)**4
    
    # g_theo = G_E * (1 + k * sin^2(phi) - k' * sin^4(phi))
    g_theo = G_E * (1 + k * sin2_phi - k_prime * sin4_phi)
    return g_theo

def free_air_correction(H):
    """計算自由空氣校正 (FAC)"""
    return FAA_GRADIENT * H

def bouguer_correction(H, rho):
    """計算簡單 Bouguer 板校正 (BC)"""
    return BOUGUER_CONSTANT * rho * H

# ----------------------------------------------------
# --- 問題 (a): 陸地站點計算 ---
# ----------------------------------------------------
print("="*40)
print("--- (a) 陸地站點計算 (H=487.9 m) ---")
print("="*40)

# i) 理論重力 (g_theo)
g_theo_a = theoretical_gravity(LATITUDE)
print(f"i) Theoretical Gravity (g_theo): {g_theo_a:.3f} mGal")

# ii) 自由空氣校正 (FAC)
fac_a = free_air_correction(ELEVATION)
print(f"ii) Free Air Correction (FAC): +{fac_a:.3f} mGal")

# iii) Bouguer 校正 (BC, 密度 2.67 g/cm^3)
rho_a = BOUGUER_DENSITY
bc_a = bouguer_correction(ELEVATION, rho_a)
print(f"iii) Bouguer Correction (BC): -{bc_a:.3f} mGal")

# iv) 自由空氣異常 (FAA)
# FAA = g_obs - g_theo + FAC
faa_a = G_OBS - g_theo_a + fac_a
print(f"iv) Free Air Gravity Anomaly (FAA): {faa_a:.3f} mGal")

# v) 布格異常 (BA)
# BA = FAA - BC
ba_a = faa_a - bc_a
print(f"v) Bouguer Gravity Anomaly (BA): {ba_a:.3f} mGal")

# ----------------------------------------------------
# --- 問題 (b): 海洋站點計算 (水深 487.9 m) ---
# ----------------------------------------------------
print("\n"+"="*40)
print("--- (b) 海洋站點計算 (觀測在海平面, 水深 D=487.9 m) ---")
print("="*40)

# 觀測點在海平面，即 H=0。

# Recompute FAA:
# i) 理論重力 (g_theo) 仍為 g_theo_a。
# ii) 自由空氣校正 (FAC_b): H=0 時 FAC = 0
fac_b = free_air_correction(0) 
print(f"i) Free Air Correction (FAC): +{fac_b:.3f} mGal (因 H=0)")

# ii) Free Air Gravity Anomaly (FAA_b)
# FAA_b = g_obs - g_theo + FAC_b
faa_b = G_OBS - g_theo_a + fac_b 
print(f"ii) Free Air Gravity Anomaly (FAA_b): {faa_b:.3f} mGal")


# Recompute Bouguer Gravity Anomaly (BA_b):
# 在海洋中，BC 稱為 Bouguer 板校正 (BC_water)
# 需要校正水柱的影響：BC_ocean = G_b * D * (rho_water - rho_crust)
water_depth = ELEVATION # 水深 D = 487.9 m
rho_contrast_b = WATER_DENSITY - BOUGUER_DENSITY # 1.03 - 2.67 = -1.64 g/cm^3

# iii) 海洋 Bouguer 校正 (BC_ocean)
# 由於對比密度為負，BC_ocean 為負值 (需加上一個負值)
bc_ocean = bouguer_correction(water_depth, rho_contrast_b)
print(f"iii) Bouguer Correction (BC_ocean, rho_c={rho_contrast_b:.2f}): {bc_ocean:.3f} mGal")

# iv) 布格異常 (BA_b)
# BA_b = FAA_b + BC_ocean
ba_ocean_b = faa_b + bc_ocean
print(f"iv) Bouguer Gravity Anomaly (BA_b): {ba_ocean_b:.3f} mGal")

print("\n"+"="*40)
print("--- 計算完成 ---")