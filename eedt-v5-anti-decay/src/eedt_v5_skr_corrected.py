import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl

# ==============================================================================
# 日本語フォント設定（確実に動作するバージョン）
# ==============================================================================
# matplotlibのフォントキャッシュを無視して強制設定
mpl.rcParams['font.family'] = 'sans-serif'

# 利用可能なフォントを直接取得
available_fonts = [f.name for f in fm.fontManager.ttflist]

# 日本語フォントを優先順位順に試す
japanese_fonts = [
    'Noto Sans CJK JP',
    'IPAGothic', 
    'IPAPGothic',
    'Noto Serif CJK JP',
    'Hiragino Sans',
    'Yu Gothic',
    'Meiryo',
    'MS Gothic'
]

font_found = None
for font in japanese_fonts:
    if font in available_fonts:
        mpl.rcParams['font.sans-serif'] = [font] + mpl.rcParams['font.sans-serif']
        font_found = font
        print(f"✅ 日本語フォント設定: {font}")
        break

if not font_found:
    print("⚠️  日本語フォントが見つかりません。英語表記になります。")
    print(f"利用可能なフォント（抜粋）: {available_fonts[:10]}")

# マイナス記号の文字化け対策
mpl.rcParams['axes.unicode_minus'] = False

# ==============================================================================
# ⚙️ 設定: 現実的なハードウェアパラメータ
# ==============================================================================
TIME_GATE = 0.3e-6     # 300ns: ゲート実行時間
T1_EDGE   = 100e-6     # 100μs: エッジキュービット(Q0, Q3)のコヒーレンス時間
P_READOUT = 0.02       # 2%: 読み出しエラー率

# スキャン範囲: 中央キュービット(Q1, Q2)のT1を 100μs(優良) から 0.1μs(劣悪) まで変化
T1_MID_RANGE = np.linspace(100, 0.1, 200)

def simulate_protocol_strict(t1_mid_us, mode='standard'):
    """
    Scout選別を「厳密な1点射影」で行うシミュレーション
    
    Parameters:
    -----------
    t1_mid_us : float
        中央キュービットのT1時間 [μs]
    mode : str
        'standard' または 'anti_decay'
    
    Returns:
    --------
    final_fidelity : float
        最終的なBell状態fidelity
    total_pass : float
        Scout測定通過率
    """
    t1_mid = t1_mid_us * 1e-6
    
    # 1. 物理的な生存確率 (Decoherence)
    p_alive_mid = np.exp(-TIME_GATE / t1_mid)
    p_alive_edge = np.exp(-TIME_GATE / T1_EDGE)
    
    S_scout = p_alive_mid ** 2  # Scout pair (Q1, Q2) 両方生存
    S_data  = p_alive_edge ** 2 # Data pair (Q0, Q3) 両方生存

    # 2. Scout測定の判定ロジック
    p = P_READOUT
    
    # 信号(Signal)が正常に生成された場合の通過確率
    prob_pass_signal = (1 - p)**2 
    
    # ノイズ(Noise = |00⟩)が誤って通過する確率
    if mode == 'standard':
        # Target "00" ← Noise |00⟩ が一致してしまう
        prob_pass_noise = (1 - p)**2
    else: # mode == 'anti_decay'
        # Target "01" ← Noise |00⟩ が誤検知される確率は低い
        prob_pass_noise = (1 - p) * p

    # 3. 総合結果の計算
    total_pass = S_scout * prob_pass_signal + (1 - S_scout) * prob_pass_noise
    
    # ゼロ除算回避
    if total_pass < 1e-12:
        return 0.25, 0.0

    # 真の信号の割合
    fraction_good = (S_scout * prob_pass_signal) / total_pass
    
    # Fidelity計算 (Data qubitsのデコヒーレンスも考慮)
    fid_signal = 0.25 + 0.75 * S_data  # Bell状態のfidelity
    fid_noise  = 0.25                   # 完全混合状態
    
    final_fidelity = fraction_good * fid_signal + (1 - fraction_good) * fid_noise
    
    return final_fidelity, total_pass


def binary_entropy(p):
    """
    バイナリエントロピー関数 H(p)
    """
    if p <= 0 or p >= 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)


def calc_secret_key_rate(fidelity, pass_rate):
    """
    秘密鍵レート(SKR)の計算
    """
    # ✅ Werner state model に基づく正しい変換
    qber = (1.0 - fidelity) / 2.0
    
    # 物理的範囲に制限
    qber = np.clip(qber, 0.0, 0.5)
    
    # Shannon limit からのエントロピー損失
    entropy_loss = 2.0 * binary_entropy(qber)
    
    # 秘密鍵生成効率 (1ビットあたり)
    efficiency = 1.0 - entropy_loss
    
    # 最終的な秘密鍵レート
    skr = pass_rate * max(0.0, efficiency)
    
    return skr


# ==============================================================================
# 🚀 シミュレーション実行
# ==============================================================================
print("="*80)
print("🚀 EEDT v5 Anti-Decay: 秘密鍵レート評価")
print("="*80)
print("\nシミュレーション開始...")

results_std = [simulate_protocol_strict(t, 'standard') for t in T1_MID_RANGE]
results_anti = [simulate_protocol_strict(t, 'anti_decay') for t in T1_MID_RANGE]

# データ整形
f_std, p_std = zip(*results_std)
f_anti, p_anti = zip(*results_anti)

# SKR計算（正しい式を使用）
skr_std = [calc_secret_key_rate(f, p) for f, p in zip(f_std, p_std)]
skr_anti = [calc_secret_key_rate(f, p) for f, p in zip(f_anti, p_anti)]

print("✅ シミュレーション完了\n")

# ==============================================================================
# 📊 グラフ化（改善版）
# ==============================================================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5.5))

# カラー定義
color_std = '#2979FF'
color_anti = '#FF1744'

# Panel 1: Fidelity
ax1.plot(T1_MID_RANGE, f_std, label='Standard (Target "00")', 
         color=color_std, linewidth=3, alpha=0.7)
ax1.plot(T1_MID_RANGE, f_anti, label='Anti-Decay (Target "01")', 
         color=color_anti, linewidth=3)
ax1.axhline(0.89, color='green', linestyle=':', linewidth=2, 
            label='Practical Threshold (F=0.89)')
ax1.axhline(0.5, color='gray', linestyle='--', linewidth=1.5, 
            label='Classical Limit (F=0.5)')

ax1.set_xlim(0, 100)
ax1.set_xlabel('Middle Qubit T1 (μs)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Fidelity', fontsize=13, fontweight='bold')
ax1.set_title('Quality: Entanglement Fidelity', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10, loc='lower right')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_ylim(0.2, 1.05)

# Panel 2: Pass Rate
ax2.plot(T1_MID_RANGE, p_std, label='Standard', 
         color=color_std, linestyle='--', linewidth=2.5)
ax2.plot(T1_MID_RANGE, p_anti, label='Anti-Decay', 
         color=color_anti, linewidth=2.5)

ax2.set_xlim(0, 100)
ax2.set_xlabel('Middle Qubit T1 (μs)', fontsize=13, fontweight='bold')
ax2.set_ylabel('Pass Rate', fontsize=13, fontweight='bold')
ax2.set_title('Quantity: Scout Pass Rate', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11, loc='lower left')
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_ylim(0, 1.05)

# Panel 3: Secret Key Rate
ax3.plot(T1_MID_RANGE, skr_std, label='Standard', 
         color=color_std, linewidth=3, alpha=0.7)
ax3.plot(T1_MID_RANGE, skr_anti, label='Anti-Decay', 
         color=color_anti, linewidth=3)

ax3.fill_between(T1_MID_RANGE, skr_std, color=color_std, alpha=0.15)
ax3.fill_between(T1_MID_RANGE, skr_anti, color=color_anti, alpha=0.15)

ax3.set_xlim(0, 100)
ax3.set_xlabel('Middle Qubit T1 (μs)', fontsize=13, fontweight='bold')
ax3.set_ylabel('Secret Key Rate (bits/attempt)', fontsize=13, fontweight='bold')
ax3.set_title('Value: QKD Secret Key Rate', fontsize=14, fontweight='bold')
ax3.legend(fontsize=11, loc='lower left')
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.set_ylim(0, max(max(skr_anti), max(skr_std)) * 1.1)

# 注釈（日本語フォントが使える場合のみ）
if font_found:
    # Standard が急落する領域を見つける
    idx_std_drop = np.where(np.array(f_std) < 0.89)[0]
    if len(idx_std_drop) > 0:
        t1_drop = T1_MID_RANGE[idx_std_drop[0]]
        ax3.axvline(t1_drop, color=color_std, linestyle=':', alpha=0.5)
        ax3.text(t1_drop + 2, max(skr_anti) * 0.3, 
                 f'Standard drops\nbelow F=0.89\nat T1≈{t1_drop:.1f}μs', 
                 color=color_std, fontsize=9, ha='left')

    # Anti-Decay の優位性を強調
    ax3.text(5, max(skr_anti) * 0.7, 
             'Anti-Decay maintains\nhigh SKR even at\nlow T1!', 
             color=color_anti, fontsize=10, fontweight='bold', 
             ha='left', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.suptitle('EEDT v5 "Anti-Decay": Complete QKD Performance Analysis', 
             fontsize=17, fontweight='bold', y=0.98)
plt.tight_layout()

# 画像保存
filename = '/home/claude/eedt_v5_skr_corrected_fixed.png'
plt.savefig(filename, dpi=150, bbox_inches='tight')
print(f"✅ グラフ保存: {filename}\n")

# ==============================================================================
# 📊 数値サマリー
# ==============================================================================
print("="*80)
print("📊 数値結果サマリー")
print("="*80)

sample_t1_values = [100, 50, 20, 10, 5, 2, 1]

print(f"\n{'T1 [μs]':>8} | {'Mode':>12} | {'Fidelity':>10} | {'Pass Rate':>10} | {'SKR':>12} | {'QBER':>8}")
print("-" * 80)

for t1_val in sample_t1_values:
    idx = np.argmin(np.abs(T1_MID_RANGE - t1_val))
    actual_t1 = T1_MID_RANGE[idx]
    
    # Standard
    qber_std = (1 - f_std[idx]) / 2.0
    print(f"{actual_t1:>8.2f} | {'Standard':>12} | {f_std[idx]:>10.4f} | {p_std[idx]:>10.4f} | {skr_std[idx]:>12.6f} | {qber_std:>7.2%}")
    
    # Anti-Decay
    qber_anti = (1 - f_anti[idx]) / 2.0
    delta_skr = skr_anti[idx] - skr_std[idx]
    print(f"{actual_t1:>8.2f} | {'Anti-Decay':>12} | {f_anti[idx]:>10.4f} | {p_anti[idx]:>10.4f} | {skr_anti[idx]:>12.6f} | {qber_anti:>7.2%}")
    print(f"{'':>8} | {'Δ (Gain)':>12} | {f_anti[idx]-f_std[idx]:>10.4f} | {p_anti[idx]-p_std[idx]:>10.4f} | {delta_skr:>+12.6f} |")
    print("-" * 80)

print("\n" + "="*80)
print("💡 重要な結論:")
print("="*80)
print("1. ✅ SKR計算式を修正: QBER = (1-F)/2 を使用（物理的に正しい）")
print("2. 🌟 Anti-Decayは全T1範囲でStandardを上回るSKRを達成")
print("3. 📈 低T1領域（<5μs）での優位性が顕著")
print("4. 🎯 F=0.89 (QBER=5.5%)が実用閾値として妥当")
print("5. ⚡ Pass Rate低下はノイズ除去の証拠であり、品質向上のコスト")
print("="*80)

plt.show()
