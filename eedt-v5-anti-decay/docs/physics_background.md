# 物理的背景：Werner State と QBER 計算

## Werner State Model

Bell状態 Φ⁺ = (|00⟩ + |11⟩)/√2 が depolarizing channel を通過した場合：

\`\`\`
ρ(F) = F|Φ⁺⟩⟨Φ⁺| + (1-F)/4 · I₄
\`\`\`

### Fidelity から QBER への変換

この状態をZ基底で測定した場合のエラー率：

\`\`\`
QBER = (1 - F) / 2
\`\`\`

#### 導出

- |00⟩または|11⟩が測定される確率: P(correct) = F/2 + (1-F)/4 = (2F+1)/4
- |01⟩または|10⟩が測定される確率: P(error) = (1-F)/4 + (1-F)/4 = (1-F)/2

したがって、QBER = P(error) = **(1-F)/2**

## 典型的な値

| Fidelity | QBER | 意味 |
|----------|------|------|
| 1.00 | 0.0% | 完璧なBell状態 |
| 0.95 | 2.5% | 高品質 |
| 0.89 | 5.5% | QKD実用閾値 |
| 0.75 | 12.5% | 中程度 |
| 0.50 | 25.0% | 古典限界 |
| 0.25 | 37.5% | 完全混合状態 |

## Secret Key Rate (SKR)

簡易BB84プロトコルでの漸近的キーレート：

\`\`\`
r = 1 - h(e_X) - h(e_Z)
\`\`\`

depolarizing近似では e_X = e_Z = QBER なので：

\`\`\`
r = 1 - 2h(QBER) = 1 - 2h((1-F)/2)
\`\`\`

最終的な秘密鍵レート：

\`\`\`
SKR = PassRate × max(0, r)
\`\`\`

## 参考文献

1. Werner, R. F. (1989). "Quantum states with Einstein-Podolsky-Rosen correlations"
2. Devetak, I., & Winter, A. (2005). "Distillation of secret key and entanglement"
3. Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing"
