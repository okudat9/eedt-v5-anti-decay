# EEDT v5 "Anti-Decay": 量子エンタングルメント検証プロトコル

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [**日本語**](README.ja.md)

## 📋 概要

IBM量子コンピュータ（Heron/Sherbrooke クラス）上での**量子エンタングルメント検証プロトコル**のシミュレーション実装です。

本プロジェクトでは、[EEDT-Quantum-Stabilizer](https://github.com/okudat9/EEDT-Quantum-Stabilizer)のランタイム安定化フレームワークを補完する形で、**Anti-Decay モード**という新しいアプローチを提案し、低品質キュービットが混在する環境でも高いFidelityを維持できることを実証しています。

### 🌟 主な特徴

- **Anti-Decay方式**: ノイズ状態 |00⟩ とターゲット |01⟩ を区別することで誤検知を大幅削減
- **秘密鍵レート(SKR)評価**: QKD（量子鍵配送）への応用を想定した実用的な性能指標
- **物理的に正確な実装**: Werner state 理論に基づく正しい QBER 計算
- **現実的なパラメータ**: IBM Heronプロセッサの実測値に基づくシミュレーション

### 🎯 主な結果

| 条件 | Standard Mode | Anti-Decay Mode | 改善率 |
|------|--------------|----------------|--------|
| T1 = 10μs | F=0.95, SKR=0.65 | F=0.99, SKR=0.86 | **+32%** |
| T1 = 1μs | F=0.68, SKR=0.00 | F=0.98, SKR=0.49 | **∞** |

**T1 = 1μs（極悪条件）でも Anti-Decay は使用可能！**

---

## 🚀 クイックスタート

\`\`\`bash
git clone https://github.com/okudat9/eedt-v5-anti-decay.git
cd eedt-v5-anti-decay
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/eedt_v5_skr_corrected.py
\`\`\`

---

## 📊 使用例

\`\`\`python
from src.eedt_v5_skr_corrected import simulate_protocol_strict, calc_secret_key_rate

fidelity, pass_rate = simulate_protocol_strict(t1_mid_us=10.0, mode='anti_decay')
skr = calc_secret_key_rate(fidelity, pass_rate)

print(f"Fidelity: {fidelity:.4f}")
print(f"SKR: {skr:.6f} bits/attempt")
\`\`\`

---

## ⚠️ 重要な修正

オリジナル版は **QBER = 1 - F** という誤った式を使用し、SKRを過小評価していました。

| Fidelity | 正しいQBER | 誤ったQBER | 正しいSKR | 誤ったSKR |
|----------|-----------|-----------|----------|----------|
| 0.89 | 5.5% | 11% | 0.385 | 0.000 |

**論文・研究発表には必ず修正版を使用してください！**

---

## 🔗 関連プロジェクト

- [EEDT-Quantum-Stabilizer](https://github.com/okudat9/EEDT-Quantum-Stabilizer) - NISQデバイス用ランタイム安定化レイヤー

---

## 📄 ライセンス

MIT License

---

**⭐ 役に立ったらスターをお願いします！**
