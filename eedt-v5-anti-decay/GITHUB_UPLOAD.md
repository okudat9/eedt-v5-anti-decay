# GitHubへのアップロード手順

## 📋 手順

### 1. GitHubで新規リポジトリを作成

1. https://github.com にアクセス
2. 「New repository」をクリック
3. Repository name: \`eedt-v5-anti-decay\`
4. Description: \`Quantum entanglement verification protocol with Anti-Decay mode for QKD applications\`
5. **Initialize this repository with: 全てチェックしない**
6. 「Create repository」をクリック

### 2. ローカルでアップロード

\`\`\`bash
cd eedt-v5-anti-decay

git init
git add .
git commit -m "Initial commit: EEDT v5 Anti-Decay implementation"
git remote add origin https://github.com/okudat9/eedt-v5-anti-decay.git
git branch -M main
git push -u origin main
\`\`\`

### 3. 完了

リポジトリURL: https://github.com/okudat9/eedt-v5-anti-decay

---

## 🔄 更新方法

\`\`\`bash
git add .
git commit -m "Update: 説明"
git push
\`\`\`

---

## 📌 注意事項

- URLは全て \`okudat9\` に設定済み
- 画像ファイルも含まれています
- MIT License使用

---

詳細: https://github.com/okudat9/EEDT-Quantum-Stabilizer
