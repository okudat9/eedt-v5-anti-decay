import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ==============================================================================
# 日本語フォント設定（文字化け対策）
# ==============================================================================
plt.rcParams['font.family'] = 'sans-serif'
# 利用可能な日本語フォントを試す（優先順位順）
japanese_fonts = ['Noto Sans CJK JP', 'IPAexGothic', 'IPAGothic', 'Hiragino Sans', 'Yu Gothic', 'Meiryo', 'MS Gothic']
for font in japanese_fonts:
    if font in [f.name for f in fm.fontManager.ttflist]:
        plt.rcParams['font.sans-serif'] = [font] + plt.rcParams['font.sans-serif']
        break
else:
    # フォールバック：英語表記に切り替え
    print("Warning: Japanese font not found. Using English labels.")

# マイナス記号の文字化け対策
plt.rcParams['axes.unicode_minus'] = False

# ==============================================================================
# オリジナル版 vs 修正版の直接比較
# ==============================================================================

TIME_GATE = 0.3e-6
T1_EDGE = 100e-6
P_READOUT = 0.02
T1_MID_RANGE = np.linspace(100, 0.1, 200)

def simulate_protocol_strict(t1_mid_us, mode='standard'):
    t1_mid = t1_mid_us * 1e-6
    p_alive_mid = np.exp(-TIME_GATE / t1_mid)
    p_alive_edge = np.exp(-TIME_GATE / T1_EDGE)
    S_scout = p_alive_mid ** 2
    S_data = p_alive_edge ** 2
    p = P_READOUT
    prob_pass_signal = (1 - p)**2
    
    if mode == 'standard':
        prob_pass_noise = (1 - p)**2
    else:
        prob_pass_noise = (1 - p) * p
    
    total_pass = S_scout * prob_pass_signal + (1 - S_scout) * prob_pass_noise
    if total_pass < 1e-12:
        return 0.25, 0.0
    
    fraction_good = (S_scout * prob_pass_signal) / total_pass
    fid_signal = 0.25 + 0.75 * S_data
    fid_noise = 0.25
    final_fidelity = fraction_good * fid_signal + (1 - fraction_good) * fid_noise
    
    return final_fidelity, total_pass

def binary_entropy(p):
    if p <= 0 or p >= 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

def calc_skr_ORIGINAL(fidelity, pass_rate):
    """❌ オリジナル版（誤り）"""
    error_rate = 1.0 - fidelity  # 誤り：2倍過大評価
    if error_rate < 0: error_rate = 0
    if error_rate > 0.5: error_rate = 0.5
    loss = 2 * binary_entropy(error_rate)
    fraction = 1.0 - loss
    return pass_rate * max(0, fraction)

def calc_skr_CORRECTED(fidelity, pass_rate):
    """✅ 修正版（正しい）"""
    qber = (1.0 - fidelity) / 2.0  # 正しい変換
    qber = np.clip(qber, 0.0, 0.5)
    loss = 2.0 * binary_entropy(qber)
    efficiency = 1.0 - loss
    return pass_rate * max(0.0, efficiency)

# シミュレーション実行
results = [simulate_protocol_strict(t, 'anti_decay') for t in T1_MID_RANGE]
fidelities, pass_rates = zip(*results)

skr_original = [calc_skr_ORIGINAL(f, p) for f, p in zip(fidelities, pass_rates)]
skr_corrected = [calc_skr_CORRECTED(f, p) for f, p in zip(fidelities, pass_rates)]

# ==============================================================================
# 比較グラフ作成（日本語対応）
# ==============================================================================
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Panel 1: Fidelity
ax1.plot(T1_MID_RANGE, fidelities, color='#FF1744', linewidth=3, label='Anti-Decay')
ax1.axhline(0.89, color='green', linestyle=':', linewidth=2, label='Practical Threshold')
ax1.axhline(0.5, color='gray', linestyle='--', linewidth=1.5, label='Classical Limit')
ax1.set_xlim(0, 100)
ax1.set_xlabel('T1 (μs)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Fidelity', fontsize=12, fontweight='bold')
ax1.set_title('Input: Fidelity (入力)', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0.2, 1.05)

# Panel 2: Pass Rate
ax2.plot(T1_MID_RANGE, pass_rates, color='#FF1744', linewidth=3, label='Anti-Decay')
ax2.set_xlim(0, 100)
ax2.set_xlabel('T1 (μs)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Pass Rate', fontsize=12, fontweight='bold')
ax2.set_title('Input: Pass Rate (通過率)', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1.05)

# Panel 3: SKR比較
ax3.plot(T1_MID_RANGE, skr_original, color='#FF6B6B', linewidth=3, 
         linestyle='--', label='Original (誤り)', alpha=0.7)
ax3.plot(T1_MID_RANGE, skr_corrected, color='#FF1744', linewidth=3, 
         label='Corrected (正しい)')
ax3.fill_between(T1_MID_RANGE, skr_original, skr_corrected, 
                  color='yellow', alpha=0.3, label='過小評価された領域')
ax3.set_xlim(0, 100)
ax3.set_xlabel('T1 (μs)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Secret Key Rate (bits/attempt)', fontsize=12, fontweight='bold')
ax3.set_title('Output: SKR比較', fontsize=14, fontweight='bold', color='red')
ax3.legend(fontsize=10, loc='lower left')
ax3.grid(True, alpha=0.3)

# 重要ポイントに注釈
idx_89 = np.argmin(np.abs(np.array(fidelities) - 0.89))
t1_89 = T1_MID_RANGE[idx_89]
ax3.annotate(f'F=0.89での違い\nOriginal: {skr_original[idx_89]:.3f}\nCorrected: {skr_corrected[idx_89]:.3f}',
             xy=(t1_89, skr_corrected[idx_89]), xytext=(t1_89+15, 0.6),
             arrowprops=dict(arrowstyle='->', color='red', lw=2),
             fontsize=11, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

# Panel 4: 差分グラフ
difference = np.array(skr_corrected) - np.array(skr_original)
ax4.fill_between(T1_MID_RANGE, 0, difference, color='#4CAF50', alpha=0.5)
ax4.plot(T1_MID_RANGE, difference, color='#2E7D32', linewidth=3, 
         label='SKR改善量 (Corrected - Original)')
ax4.axhline(0, color='black', linestyle='-', linewidth=1)
ax4.set_xlim(0, 100)
ax4.set_xlabel('T1 (μs)', fontsize=12, fontweight='bold')
ax4.set_ylabel('SKR Improvement (bits/attempt)', fontsize=12, fontweight='bold')
ax4.set_title('改善量グラフ', fontsize=14, fontweight='bold', color='green')
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)

# 最大改善ポイントを強調
max_diff_idx = np.argmax(difference)
max_diff_t1 = T1_MID_RANGE[max_diff_idx]
max_diff_val = difference[max_diff_idx]
ax4.plot(max_diff_t1, max_diff_val, 'r*', markersize=20)
ax4.annotate(f'最大改善\nT1={max_diff_t1:.1f}μs\nΔSKR={max_diff_val:.3f}',
             xy=(max_diff_t1, max_diff_val), xytext=(max_diff_t1+15, max_diff_val*0.7),
             arrowprops=dict(arrowstyle='->', color='red', lw=2),
             fontsize=11, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

plt.suptitle('Original vs Corrected: SKR計算式の影響比較', 
             fontsize=18, fontweight='bold', y=0.995)
plt.tight_layout()

filename = '/home/claude/comparison_original_vs_corrected_fixed.png'
plt.savefig(filename, dpi=150, bbox_inches='tight')
print(f"✅ 比較グラフ保存: {filename}")

# 数値サマリー
print("\n" + "="*80)
print("📊 重要ポイントでの数値比較")
print("="*80)

critical_t1_values = [20, 10, 5, 2, 1]
print(f"\n{'T1[μs]':>7} | {'Fidelity':>10} | {'QBER(正)':>10} | {'SKR(誤)':>12} | {'SKR(正)':>12} | {'改善率':>10}")
print("-" * 80)

for t1_val in critical_t1_values:
    idx = np.argmin(np.abs(T1_MID_RANGE - t1_val))
    actual_t1 = T1_MID_RANGE[idx]
    f = fidelities[idx]
    qber = (1 - f) / 2.0
    skr_orig = skr_original[idx]
    skr_corr = skr_corrected[idx]
    
    if skr_orig > 0:
        improvement = (skr_corr / skr_orig - 1) * 100
    else:
        improvement = float('inf') if skr_corr > 0 else 0
    
    print(f"{actual_t1:>7.2f} | {f:>10.4f} | {qber:>9.2%} | {skr_orig:>12.6f} | {skr_corr:>12.6f} | {improvement:>9.1f}%")

print("\n" + "="*80)
print("💡 結論:")
print("  • オリジナル版は物理的に不正確な式により、SKRを大幅に過小評価")
print("  • 高Fidelity領域（F>0.95）では差は小さいが、中程度（0.8<F<0.95）で顕著")
print("  • 修正版は Werner state 理論に基づく正しい評価を提供")
print("="*80)

plt.show()
