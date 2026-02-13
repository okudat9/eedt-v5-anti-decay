# EEDT v5 "Anti-Decay": Entanglement Verification Protocol

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[**English**](README.md) | [日本語](README.ja.md)

## 📋 Overview

Simulation of **quantum entanglement verification protocol** on IBM Quantum computers (Heron/Sherbrooke class).

This project proposes a novel **Anti-Decay mode** that maintains high fidelity even in environments with mixed-quality qubits, complementing the [EEDT-Quantum-Stabilizer](https://github.com/okudat9/EEDT-Quantum-Stabilizer) runtime stabilization framework.

### 🌟 Key Features

- **Anti-Decay approach**: Dramatically reduces false positives by distinguishing noise state |00⟩ from target |01⟩
- **Secret Key Rate (SKR) evaluation**: Practical performance metrics for QKD applications
- **Physically accurate**: Correct QBER calculation based on Werner state theory
- **Realistic parameters**: Based on measured values from IBM Heron processors

### 🎯 Main Results

| Condition | Standard Mode | Anti-Decay Mode | Improvement |
|-----------|--------------|----------------|-------------|
| T1 = 10μs | F=0.95, SKR=0.65 | F=0.99, SKR=0.86 | **+32%** |
| T1 = 1μs  | F=0.68, SKR=0.00 | F=0.98, SKR=0.49 | **∞** |

**Anti-Decay works even at T1 = 1μs (extreme conditions)!**

---

## 🚀 Quick Start

### 1. Setup

\`\`\`bash
# Clone the repository
git clone https://github.com/okudat9/eedt-v5-anti-decay.git
cd eedt-v5-anti-decay

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 2. Run Simulation

\`\`\`bash
# Run main simulation
python src/eedt_v5_skr_corrected.py

# Run comparison analysis
python src/comparison_analysis.py
\`\`\`

### 3. View Results

After execution, graphs will be saved in \`results/\` directory.

---

## 📊 Usage

### Basic Usage

\`\`\`python
from src.eedt_v5_skr_corrected import simulate_protocol_strict, calc_secret_key_rate

# Simulate at T1 = 10μs
fidelity, pass_rate = simulate_protocol_strict(t1_mid_us=10.0, mode='anti_decay')

# Calculate secret key rate
skr = calc_secret_key_rate(fidelity, pass_rate)

print(f"Fidelity: {fidelity:.4f}")
print(f"Pass Rate: {pass_rate:.4f}")
print(f"Secret Key Rate: {skr:.6f} bits/attempt")
\`\`\`

---

## 🔬 Physics Background

### Werner State Model

Relationship between Bell state fidelity **F** and QBER:

\`\`\`
QBER = (1 - F) / 2
\`\`\`

### Secret Key Rate (SKR)

Calculation based on simplified BB84 protocol:

\`\`\`
SKR = PassRate × max(0, 1 - 2H(QBER))
\`\`\`

See [\`docs/expert_review.md\`](docs/expert_review.md) for details.

---

## 📈 Critical Fix

### Original Version Issue

The original code used incorrect formula **QBER = 1 - F**, underestimating SKR by up to **∞×**.

| Fidelity | Correct QBER | Wrong QBER | Correct SKR | Wrong SKR |
|----------|--------------|------------|-------------|-----------|
| 0.89 | 5.5% | 11% | 0.385 | 0.000 |

**Always use the corrected version for papers and presentations!**

---

## 🔗 Related Projects

- [EEDT-Quantum-Stabilizer](https://github.com/okudat9/EEDT-Quantum-Stabilizer) - Runtime stabilization layer for NISQ devices

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues or PRs.

- **Issue Tracker**: [GitHub Issues](https://github.com/okudat9/eedt-v5-anti-decay/issues)
- **Discussions**: [GitHub Discussions](https://github.com/okudat9/eedt-v5-anti-decay/discussions)

---

## 📧 Contact

For questions or collaboration:
- Open an issue: https://github.com/okudat9/eedt-v5-anti-decay/issues
- Main EEDT Project: https://github.com/okudat9/EEDT-Quantum-Stabilizer

---

**⭐ If this project helps your research, please give it a star!**
