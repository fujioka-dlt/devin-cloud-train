# LLM・コーディングAIエージェント 最新動向レポート

- 作成日: 2026-08-06
- 対象期間: 2026-07-01 〜 2026-08-06（直近約1か月）
- 対象読者: エンジニア
- 情報源の方針: 各ベンダーの公式ブログ / 公式リリースノート / 信頼できる技術メディア（CNBC 等）のみを参照。未検証の噂・リーク情報は「未確定情報」として明示。

---

## 1. 動向サマリ表（全10件）

| # | カテゴリ | 名称 | 発表日 | 技術的特徴 | 情報源URL |
| --- | --- | --- | --- | --- | --- |
| 1 | モデル | OpenAI GPT-5.6 シリーズ（Sol / Terra / Luna） | 2026-06-26 プレビュー → 2026-07-08 一般公開 | フラッグシップ Sol、日常業務向け Terra（GPT-5.5 相当性能で価格2分の1）、低コスト Luna の3構成。新しい `max` 推論エフォート、およびサブエージェントを使う `ultra` モードを追加。Terminal-Bench 2.1 で当時のSOTA。ExploitBench では Mythos Preview 相当の性能を約1/3の出力トークンで達成 | https://openai.com/index/previewing-gpt-5-6-sol/ , https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html |
| 2 | モデル | OpenAI GPT-Live-1 / GPT-Live-1 mini（音声モデル） | 2026-07-08 | 聞くと話すを同時に行える新世代の音声モデル。ChatGPT ユーザーへグローバル展開。マルチモーダル（音声）用途の刷新 | https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html |
| 3 | モデル | Anthropic Claude Opus 5 | 2026-07-24 | コンテキスト長 1M トークン（既定・最大とも）、最大出力 128k トークン、thinking（拡張思考）が既定ON。価格は Opus 4.8 据え置きの $5 / $25 per MTok。effort 設定で知能とトークン消費のトレードオフを調整可能。Frontier-Bench v0.1 / GDPval-AA で SOTA、OSWorld 2.0（コンピュータ操作）でも同コストなら最良。API 側に「自動フォールバック」ベータを同時提供 | https://www.anthropic.com/news/claude-opus-5 , https://platform.claude.com/docs/en/release-notes/overview |
| 4 | モデル | Google Gemini 3.6 Flash / 3.5 Flash-Lite / 3.5 Flash Cyber | 2026-07-21 | 3.6 Flash: コーディング・マルチモーダル性能を改善しつつ、Artificial Analysis Index 基準で出力トークンを 3.5 Flash 比 17% 削減（DeepSWE では最大 65% 削減）。3.5 Flash-Lite: 350 出力トークン/秒の高速・低コスト。3.5 Flash Cyber: CodeMender エージェントと組み合わせるセキュリティ特化モデル | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ |
| 5 | モデル | Cognition SWE-1.7 | 2026-07-08 | Kimi K2.7 ベースに独自 RL ポストトレーニング。長時間・非同期タスク向けに self-compaction（作業状態を要約して再開し、実効タスク長を素のコンテキスト長より延長）を実装。Terminal-Bench 2.1 = 81.5%、SWE-Bench Multilingual = 77.8%、FrontierCode 1.1 Main = 42.3%。Devin（Web / Desktop / CLI）で Cerebras 経由 1000 TPS で提供 | https://cognition.com/blog/swe-1-7 |
| 6 | エージェント | Devin: Stacked PRs（GitHub と協業） | 2026-07-30 | 大規模タスクの成果物を巨大な単一PRではなく、自己完結した小さなPRの「スタック」に自動分解。GitHub のスタック機能と連携し、各層のCI・レビュー・マージ可能性をまとめて追跡 | https://devin.ai/blog/introducing-pr-stacks |
| 7 | エージェント | Devin Security Swarm | 2026-07-01 | 並列エージェント群（Agentic MapReduce）でコードベースを分割走査し、攻撃経路を合成のうえサンドボックスで実行時に再現して「悪用可能」を検証、修正PRまで作成。GHSA 由来の実在脆弱性50件のベンチで Recall 72% / $90.23 per run（比較対象: Claude 68%・$131.87、Codex 48%・$118.20、Cursor 26%・$4.60） | https://cognition.com/blog/introducing-devin-security-swarm |
| 8 | エージェント | GitHub Copilot vision の一般提供（GA） | 2026-07-01 | 画像（JPEG/PNG/GIF/WebP）と PDF をチャットに直接添付し、コードと合わせて推論可能に。VS Code の Copilot Chat（ask / plan / agent モード）、github.com のチャット、Copilot CLI で利用可。Free を含む全プランで既定ON | https://github.blog/changelog/2026-07-01-copilot-vision-is-generally-available/ |
| 9 | エージェント | GitHub Copilot code review: Agent skills / MCP の GA | 2026-07-29 | `.github/skills` 配下の `SKILL.md` で社内規約・独自ツールをレビューに注入可能。MCP サーバ接続で外部コンテキストを参照（MCP ツール呼び出しは read-only 制限）。GitHub / Playwright MCP は既定ON。skills・MCP 由来のコメントには出所が表示される | https://github.blog/changelog/2026-07-29-copilot-code-review-agent-skills-and-mcp-now-generally-available/ |
| 10 | エージェント | Cursor Router（Auto モードの刷新） | 2026-07-22 | リクエストをタスク種別と複雑度で分類し、フロンティアモデルと低コストモデルへ自動振り分け。最適化モードは Intelligence / Balance / Cost の3種。管理者はチーム・グループ単位の有効化、モード制限、既定モード、モデルの allow/block を設定可能。desktop / web / iOS / CLI / SDK で利用可、Teams プランは既定ON | https://cursor.com/changelog/cursor-router |

---

## 2. 未確定情報（公式に「予定・進行中」とされているもの / 時期未定）

以下は噂・リークではなく **公式ブログに記載された未リリース事項** だが、提供時期・最終仕様が未確定のため区別して記載する。

| 内容 | 現在のステータス | 情報源URL |
| --- | --- | --- |
| Google **Gemini 3.5 Pro** | パートナーとテスト中。「準備でき次第、広く提供」と記載のみで時期未定 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ |
| Google **Gemini 4** | 「最も野心的な事前学習を開始した」との言及のみ。仕様・時期とも未公表 | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ |
| OpenAI **Codex の GPT-5.4 / GPT-5.4 mini 廃止** | 2026-08-31 に Codex から退役予定（告知済み・実施前） | https://learn.chatgpt.com/docs/changelog |

なお、本レポートの対象期間内に **Meta（Llama 系）から新モデルの公式発表は確認できなかった**（直近の公式発表は Llama 4 系のまま）。

---

## 3. エンジニア視点：業務に取り入れる価値がありそうな項目 3選

### ① Devin: Stacked PRs（#6）
**理由:** エージェント活用の最大のボトルネックは「生成量」ではなく「レビュー可能性」。数千行・数十ファイルの単一PRは、実質的にレビュー不能でマージ判断が属人化する。Stacked PRs は成果物を自己完結した小さな差分の順序付き列に分解するため、既存のレビュー文化（1PR=1関心事）をそのまま維持できる。エージェント導入の障壁が「品質」ではなく「レビュー体制」にあるチームほど、導入効果が即座に出る。CI・マージ可能性の追跡が自動化される点も、スタック運用の手作業コストを消すという意味で実務的。

### ② GitHub Copilot code review の Agent skills / MCP（#9）
**理由:** レビュー自動化の一般解は「一般論の指摘しか出ない」ため定着しにくい。`.github/skills/SKILL.md` にチーム固有のコーディング規約・命名規則・禁止パターンを書けば、AIレビューがそのままチームの規約チェッカーになる。ファイルをリポジトリに置くだけで完結し、専用インフラも不要。しかも同じ SKILL.md 資産は Copilot cloud agent 等でも再利用でき、投資が二重に効く。MCP 呼び出しが read-only に制限されている点はセキュリティレビュー上も通しやすい。

### ③ Cursor Router / Gemini 3.6 Flash に代表される「コスト最適化レイヤ」（#10, #4）
**理由:** モデル性能の上限競争と並行して、この1か月の最大の実務トレンドは **同一品質をより安く出す**こと（Router による自動振り分け、Gemini 3.6 Flash の出力トークン17%削減、Opus 5 の effort 設定、SWE-1.7 の self-compaction）。エージェント利用が日常化すると費用は利用量に比例して線形に増えるため、「どのタスクにどのモデルを割り当てるか」をアプリ側で作り込むのではなく、Router のような仕組みに委ねられる価値は大きい。管理者がモード制限・モデル allow/block を掛けられるため、コスト上限とモデルガバナンス（承認済みモデルのみ使用）を同じ仕組みで担保できるのも組織導入向き。

---

## 参照した一次情報源一覧

- OpenAI: https://openai.com/index/previewing-gpt-5-6-sol/
- OpenAI / ChatGPT・Codex changelog: https://learn.chatgpt.com/docs/changelog
- Anthropic: https://www.anthropic.com/news/claude-opus-5
- Anthropic Platform リリースノート: https://platform.claude.com/docs/en/release-notes/overview
- Google: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/
- Cognition: https://cognition.com/blog/swe-1-7 , https://cognition.com/blog/introducing-devin-security-swarm
- Devin: https://devin.ai/blog/introducing-pr-stacks
- GitHub Changelog: https://github.blog/changelog/2026-07-01-copilot-vision-is-generally-available/ , https://github.blog/changelog/2026-07-29-copilot-code-review-agent-skills-and-mcp-now-generally-available/
- Cursor Changelog: https://cursor.com/changelog/cursor-router , https://cursor.com/changelog
- CNBC: https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html
