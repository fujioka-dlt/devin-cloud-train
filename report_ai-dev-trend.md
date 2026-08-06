# LLM・コーディングAIエージェント 最新動向レポート

- 作成日: 2026-08-06
- 対象期間: 2026-07-01 〜 2026-08-06（直近約1か月）
- 対象読者: エンジニア
- 情報源の方針: 各ベンダーの公式ブログ / 公式リリースノート / 信頼できる技術メディアのみを参照。未検証の噂・リーク情報は「未確定情報」として明示。
- 構成: 1〜3 は全体動向（表10件・未確定情報・推奨3選）。4〜5 は **Claude / Devin の公式情報に絞った深掘り**。6 は **第三者による検証記事・企業の導入事例**（公式発表ではないことを明示して区別）。

---

## 1. 動向サマリ表（全10件）

| # | カテゴリ | 名称 | 発表日 | 技術的特徴 | 情報源URL |
| --- | --- | --- | --- | --- | --- |
| 1 | モデル | OpenAI GPT-5.6 シリーズ（Sol / Terra / Luna） | 2026-06-26 プレビュー → 2026-07-08 一般公開 | フラッグシップ Sol、日常業務向け Terra（GPT-5.5 相当性能で価格2分の1）、低コスト Luna の3構成。新しい `max` 推論エフォート、およびサブエージェントを使う `ultra` モードを追加。Terminal-Bench 2.1 で当時のSOTA。ExploitBench では Mythos Preview 相当の性能を約1/3の出力トークンで達成 | https://openai.com/index/previewing-gpt-5-6-sol/ , https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html |
| 2 | モデル | OpenAI GPT-Live-1 / GPT-Live-1 mini（音声モデル） | 2026-07-08 | 聞くと話すを同時に行える新世代の音声モデル。ChatGPT ユーザーへグローバル展開。マルチモーダル（音声）用途の刷新 | https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html |
| 3 | モデル | Anthropic Claude Opus 5 | 2026-07-24 | コンテキスト長 1M トークン（既定・最大とも）、最大出力 128k トークン、thinking（拡張思考）が既定ON。価格は Opus 4.8 据え置きの $5 / $25 per MTok。effort 設定で知能とトークン消費のトレードオフを調整可能。Frontier-Bench v0.1 / GDPval-AA で SOTA、OSWorld 2.0（コンピュータ操作）でも同コストなら最良。API 側に「自動フォールバック」ベータを同時提供 | https://www.anthropic.com/news/claude-opus-5 , https://platform.claude.com/docs/en/release-notes/overview |
| 4 | モデル | Google Gemini 3.6 Flash / 3.5 Flash-Lite / 3.5 Flash Cyber | 2026-07-21 | 3.6 Flash: コーディング・マルチモーダル性能を改善しつつ、Artificial Analysis Index 基準で出力トークンを 3.5 Flash 比 17% 削減（DeepSWE では最大 65% 削減）。3.5 Flash-Lite: 350 出力トークン/秒の高速・低コスト。3.5 Flash Cyber: CodeMender エージェントと組み合わせるセキュリティ特化モデル | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/ |
| 5 | モデル | Cognition SWE-1.7 | 2026-07-08 | Kimi K2.7 ベースに独自 RL ポストトレーニング。長時間・非同期タスク向けに self-compaction（作業状態を要約して再開し、実効タスク長を素のコンテキスト長より延長）を実装。Terminal-Bench 2.1 = 81.5%、SWE-Bench Multilingual = 77.8%、FrontierCode 1.1 Main = 42.3%。Devin（Web / Desktop / CLI）で Cerebras 経由 1000 TPS で提供 | https://cognition.ai/blog/swe-1-7 |
| 6 | エージェント | Devin: Stacked PRs（GitHub と協業） | 2026-07-30 | 大規模タスクの成果物を巨大な単一PRではなく、自己完結した小さなPRの「スタック」に自動分解。GitHub ネイティブの stacked PR API 上に構築され、スタックはボトムアップに一括マージ。Devin Review はスタック全体を1画面で扱い、各層のCI・必須レビュー・ブランチ保護を加味したマージ可能性を色で表示。GitHub.com のみ対応 | https://devin.ai/blog/introducing-pr-stacks , https://docs.devin.ai/work-with-devin/stacked-prs |
| 7 | エージェント | Devin Security Swarm | 2026-07-01 | 並列エージェント群（Agentic MapReduce）でコードベースを分割走査し、攻撃経路を合成のうえサンドボックスで実行時に再現して「悪用可能」を検証、修正PRまで作成。GHSA 由来の実在脆弱性50件のベンチで Recall 72% / $90.23 per run（比較対象: Claude 68%・$131.87、Codex 48%・$118.20、Cursor 26%・$4.60） | https://cognition.ai/blog/introducing-devin-security-swarm |
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

## 4. Anthropic Claude 公式の最新動向・アップデート（2026-07-01 〜 2026-08-06）

出典: Anthropic Newsroom / Claude Platform リリースノート / Claude Docs / claude-code CHANGELOG（すべて公式）。

### 4-1. モデル

| 発表日 | 内容 | 技術的ポイント | 情報源URL |
| --- | --- | --- | --- |
| 2026-07-24 | **Claude Opus 5**（`claude-opus-5`）提供開始 | 1M トークンコンテキスト（既定=最大、小容量版なし）／最大出力 128k／thinking 既定ON／$5・$25 per MTok（Opus 4.8 据え置き）。Frontier-Bench v0.1 で Opus 4.8 の2倍超、CursorBench 3.2 では max effort で Fable 5 のピークと 0.5% 差を半額で達成。ARC-AGI 3・OSWorld 2.0・Zapier AutomationBench でも同コスト帯で最良。Claude Max の既定モデル | https://www.anthropic.com/news/claude-opus-5 |
| 2026-06-30 | Claude Sonnet 5 提供開始（対象期間の直前） | コーディング・エージェント・業務タスク向けのスケール重視モデル | https://www.anthropic.com/news |
| 2026-07-01 | Claude Fable 5 / Mythos 5 のアクセス復旧 | 6/30 の「Redeploying Fable 5」告知を受けた復旧。併せてジェイルブレイク深刻度スコアリングの業界共通枠組みを提案 | https://www.anthropic.com/news/redeploying-fable-5 |

### 4-2. Opus 5 の「移行時に効く」仕様変更（エンジニア向け）

| 変更 | 内容 | 情報源URL |
| --- | --- | --- |
| thinking が既定ON | Opus 4.8 では明示指定が必要だったが、Opus 5 は既定で thinking。`max_tokens` は thinking＋本文の合計上限のため、旧設定のままだと出力が切れる可能性あり | https://docs.claude.com/en/docs/about-claude/models/whats-new-opus-5 |
| **破壊的変更**: thinking 無効化の制限 | `thinking: {"type":"disabled"}` は effort が `high` 以下のときのみ許可。`xhigh` / `max` と併用すると 400 エラー | 同上 |
| effort が主制御に | `low / medium / high / xhigh / max` の5段。既定は `high`。effort を上げるほど素直に品質へ変換される設計 | https://docs.claude.com/en/build-with-claude/effort |
| プロンプトキャッシュ最小長の引き下げ | 1,024 → **512 トークン**。短いプロンプトもコード変更なしでキャッシュ対象に | https://docs.claude.com/en/docs/about-claude/models/whats-new-opus-5 |
| Fast mode（research preview） | Opus 5 は Claude API のみ対応（Bedrock / Vertex / Foundry は非対応）。$10 / $50 per MTok。なお Opus 4.7 の fast mode は廃止 | 同上 / https://docs.claude.com/en/release-notes/overview |
| 会話途中のツール変更（beta） | ターン間でツールを追加・削除してもプロンプトキャッシュを保持。`mid-conversation-tool-changes-2026-07-01` ヘッダ | 同上 |
| サーバサイド fallback の `"default"` モード（beta） | 拒否カテゴリごとに Anthropic 推奨のフォールバック先を自動適用。`server-side-fallback-2026-07-01` ヘッダ | https://docs.claude.com/en/release-notes/overview |

### 4-3. プラットフォーム / API（Claude Platform リリースノート）

| 日付 | 内容 | 情報源URL |
| --- | --- | --- |
| 2026-08-01 | Dreams（research preview）が Opus 5 に対応 | https://docs.claude.com/en/release-notes/overview |
| 2026-07-22 | Claude Managed Agents: エージェントのモデル設定に `effort` を指定可能に。環境・メモリストアのライフサイクル webhook（`environment.*` 4種、`memory_store.*` 3種）追加。セッション作成時に `initial_events`（最大50件）で初期イベントを投入し、同一呼び出しでエージェントループを開始可能。スレッド単位のイベントデルタ配信に対応 | 同上 |
| 2026-07-17 | 旧 Workbench を **2026-08-17 に廃止**。実験的プロンプトツール API（generate / improve / templatize）も同日廃止 | 同上 |
| 2026-07-15 | 会話途中のシステムメッセージが Fable 5 / Mythos 5 / Opus 4.8 で利用可能（beta ヘッダ不要） | 同上 |
| 2026-07-14 | Claude Enterprise のユーザー管理を Admin API で実施可能（beta）。メンバー一覧・ロール変更・招待・グループ管理など | 同上 |
| 2026-07-08 | API キー / Admin API キーに**有効期限**を設定可能に。7日以上のキーは失効前にメール通知 | 同上 |
| 2026-07-02 | メモリ API の beta ヘッダを `agent-memory-2026-07-22` に刷新（一覧の順序・`depth`・`path_prefix` の挙動が変更）。各言語 SDK も追随 | 同上 |

### 4-4. Claude Code（CHANGELOG 2.1.22x 系、2026-08 時点）

- `/review` は `/code-review` の別名に統合。`/code-review <PR番号>` で PR レビュー、`/code-review ultra` でクラウド上の深いレビューを実行。effort 未指定時は前回指定値を再利用。
- `CLAUDE_CODE_DISABLE_1M_CONTEXT` が、固定リストではなく **1M ウィンドウを持つ全 Claude モデル**を自動コンパクションで 200K に抑える挙動に変更。
- セキュリティ修正が複数: Bash の権限チェック回避（コマンドの一部を隠蔽できる問題）、タブ／不可視 Unicode による承認ダイアログの偽装、workflow スクリプトが動的 `import()` でサンドボックス外を実行できた問題、`bypassPermissions` が組織ポリシーを無視していた問題。
- worktree 分離セッションとそのサブエージェントが本チェックアウトに破壊的 git コマンドを実行できた問題を修正。
- クラウドセッションで `claude --teleport` によりローカル継続できるヒントを表示。
- 情報源: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- 参考（読み物）: 「The Making of Claude Code」2026-07-06 https://www.anthropic.com/news

---

## 5. Cognition / Devin 公式の最新動向・アップデート（2026-07-01 〜 2026-08-06）

出典: Cognition 公式ブログ / Devin 公式ドキュメント・リリースノート。

### 5-1. モデルとベンチマーク

| 発表日 | 内容 | 技術的ポイント | 情報源URL |
| --- | --- | --- | --- |
| 2026-07-08 | **SWE-1.7** | Kimi K2.7 ベースに独自 RL。Terminal-Bench 2.1 = 81.5%、SWE-Bench Multilingual = 77.8%、FrontierCode 1.1 Main = 42.3%。self-compaction で長時間タスクに対応。Devin（Web / Desktop / CLI）で Cerebras 経由 **1000 TPS** | https://cognition.ai/blog/swe-1-7 |
| 2026-07-13 | **Making Fable Cheaper Than Opus**（Devin Fusion の実測） | FrontierCode 1.1 で 3,000 セッションを4構成比較。Fable 5 + Sidekick = スコア 60.7 / $1.86、Opus 4.8 + Sidekick = 54.6 / $2.04。トークン単価が2倍の Fable 側が**総額で安く、かつ高スコア**。理由はリード側のターン数（11.5 vs 26.5）と持ち込みコンテキスト量（545k vs 1,679k tok）の差。Fable 主導では 81% のランでリードが一度もコード編集しない | https://cognition.ai/blog/making-fable-cheaper-than-opus |
| 2026-07-07 | FrontierCode 1.1 | 評価手法を改訂し、正当なインターネット利用と不正な利用を区別 | https://cognition.ai/blog |

### 5-2. セキュリティ / コンプライアンス

| 発表日 | 内容 | 情報源URL |
| --- | --- | --- |
| 2026-07-01 | **Devin Security Swarm**: 並列エージェントがコードベースを分割走査し、業務ロジック欠陥・認可バイパスの連鎖・サービス跨ぎの攻撃経路を検出。攻撃経路を合成してサンドボックスで実行時に再現し、悪用可能性を確認したうえで修正PRを作成。GHSA 由来 50 件のベンチで Recall 72% / $90.23（Claude 68%・$131.87、Codex 48%・$118.20、Cursor 26%・$4.60）。スキャンプロファイルは既存の脅威モデル文書から生成でき、差分スキャンで回数を重ねるほど低コスト化 | https://cognition.ai/blog/introducing-devin-security-swarm |
| 2026-07-02 | Devin Security Vulnerability Remediation Program（6週間の伴走支援でCVEバックログを解消し、継続運用へ移行） | https://cognition.ai/blog |
| 2026-07-13 | Cognition プラットフォーム全体が **FedRAMP Class D (High) In-Process** に。Devin Desktop / CLI は既に FedRAMP High 認証済み（ITAR、DoW IL4/5/6 対応） | https://cognition.ai/blog/devin-fedramp-high-in-process |
| 2026-07-22 | 米国エネルギー省（DOE）「Genesis Mission」参画の MOU 締結。国立研究所コードベースへのコードセキュリティスキャン提供などを表明 | https://cognition.ai/blog/cognition-doe-genesis-mission |

### 5-3. プロダクト機能（Devin リリースノート / ドキュメント）

| 領域 | 内容 | 情報源URL |
| --- | --- | --- |
| Stacked PRs | 大きな作業を「順序付きの小さなPR列」に分解。GitHub ネイティブの stacked PR として作成され、下から順に**アトミックに一括マージ**。マージ後は残りのPRが自動でトランクへ再ターゲット。Devin Review にスタックパネルと層ごとのマージ可否表示 | https://docs.devin.ai/work-with-devin/stacked-prs , https://docs.devin.ai/work-with-devin/devin-review |
| Skills / プラグイン | スキルをプラグインとして配布し、Devin Cloud / CLI / Desktop に一貫適用。管理者は必須・任意・禁止プラグインを Settings → Marketplace で統制でき、組織はエンタープライズ方針を継承 | https://docs.devin.ai/release-notes/overview |
| コードスキャン | 複数リポジトリを1回のスキャンで横断。関連する検出結果を**連鎖攻撃経路**として関連付け。スキャンプロファイルの種別・モードによる絞り込み、新規スキャン導線の刷新 | 同上 |
| MCP | MCP ツールをセッションのリモートマシンではなく **Devin のサーバ側で実行**。プラグイン提供の MCP サーバをコネクタ画面で分離表示、認証未設定時は動的 OAuth にフォールバック | 同上 |
| モデル選択 | モデルピッカーを刷新し、能力の選択・Fusion のON/OFF・速度・モードを1メニューに集約 | 同上 |
| セキュリティ／運用 | SCIM プロビジョニングが GA、OIDC 短期トークンによるクラウド認証、IP 許可リストを自動化 webhook にも適用、Devin Local 設定の監査ログ化 | 同上 |
| 実行環境 | **Devin Outposts**（自社環境で Devin ワークロードを実行する仕組み。既定は無効） | 同上 |
| ワークフロー | Slack から `!windows` で Windows セッション起動、ブロックされた宛先へのネットワーク許可を Slack から承認、`/ask` などスラッシュコマンド、PR のマージ状況バーに必要承認数／取得済み承認数を表示 | 同上 |

---

## 6. 活用事例・第三者による検証（技術メディア／企業技術ブログ）

公式発表ではないが、**実測値や運用実績が公開されている記事**を対象に収集した。個人の感想レベルの記事は除外している。

### 6-1. Claude（Opus 5 / Claude Code）

| 出典 | 検証内容 | 主な結果 | URL |
| --- | --- | --- | --- |
| 個人検証（Zenn、2026-07-26） | Opus 5 / Opus 4.8 / Fable 5 × effort 4段 を各30試行、計360試行で品質・コスト・処理時間を比較 | Opus 5 のみ全 effort で品質ゲートを通過（T2 通過率 100%）。Opus 5 low = 122秒 / $0.78 に対し xhigh = 332秒 / $1.49。**低 effort でも品質の床が抜けない**点が世代差 | https://zenn.dev/nnakapa/articles/lab-29-opus5-fable5-qcd |
| CodeRabbit（2026-07-24） | 実PR由来の約100件のエラーパターンで、AIコードレビュー品質を3構成×3回計測 | Opus 5 x-high は**アクション可能コメントの精度は改善**（39.3% vs 35.2%）だが既知バグの検出率は低下（55.2% vs 61.1%）、nitpick は約4倍。結論は「唯一のレビュアーには推さない。精度重視の2番手レーンとして有用」 | https://www.coderabbit.ai/ja/blog/opus-5-model-review |
| Fyve（2026-07-26） | 実務寄りの5課題を Opus 5 / Fable 5 / GPT-5.6 Sol に同一条件で投げて実測 | 出力単価が最も高い Fable 5 が**合計金額で最安**（$3.73 / 7.0分）。Opus 5 は $7.70 / 31.2分で出力トークン約4倍。「Opus 5 は盛る、Fable 5 は削る」 | https://fyve.co.jp/claude-code/articles/opus5-fable5-sol-real-test |
| 個人検証（Zenn、2026-07-28） | Opus 5 移行時に「検証しろ」系のプロンプトを残す／消すで 12 ラン比較 | テスト通過は全ラン 29/29 で**品質差ゼロ**。一方コストは出力トークン +38%、ツール呼び出し +125%、実時間 +317%、金額 +185%。**Opus 5 ではプロンプトを足すより消す** | https://zenn.dev/ino_h/articles/2026-07-28-claude-opus-5-migration |
| 個人検証（Zenn、2026-07-25／QAエンジニア） | 凍結済みのテスト設計ベンチでモデルのみ差し替え | 「拾える観点の深さ」は世代で明確に向上したが、**根拠の正確さ（誇張率26%）は Opus 4.8 と同一**。出力の引用を原典と突き合わせる検査レイヤは外せない | https://zenn.dev/mumihatsu/articles/7294b39953b917 |
| DeNA（2026-07-01） | PdM・エンジニア・デザイナーが Claude Code を共通ツールとして使う体制 | 仕様→動くモックの確認サイクルが「2週間〜1か月」から「1〜2日」に短縮。SDD（Spec Driven Development）プラグインで PRD・仕様書生成からコード生成まで自動化し、人間は仕様レビューに専念 | https://engineering.dena.com/blog/2026/07/claude-code-team-collaboration/ |

### 6-2. Devin

| 出典 | 活用内容 | 主な結果 | URL |
| --- | --- | --- | --- |
| ストックマーク（2026-03） | Slack × Devin × Playbook で Biz→エンジニアの社内QAを半自動化 | 1か月の試行で91件を検証し、信頼度「高」の回答は**正答率95%**。本番運用でエンジニア対応が必要な問い合わせが月55件→27件（約49%減）。Devin Wiki によるリポジトリ全体把握と Knowledge 蓄積が精度を支える | https://stockmark-tech.hatenablog.com/entry/2026/03/16/080000 |
| TalentX（2026-06-08） | Ask Devin をテスト設計（仕様把握・観点洗い出し）に適用 | 差分から影響範囲と異常系観点を数分で出力し、**テスト設計のリードタイムを体感8割削減**。コード行へのリンク付きで根拠が追えるためレビューしやすい。残り2割（UX・暗黙仕様）は人間が担当 | https://tech.talentx.co.jp/entry/2026/06/08/111241 |
| TalentX（2026-02-02） | Sentry エラー調査を Devin に委譲（Playbook＋Secrets＋内蔵ブラウザで自動ログイン） | 1件15分かかっていた調査が、スタンプ1つ→5分後にレポート。コンテキストスイッチがほぼゼロになり、調査精度の属人化も解消 | https://tech.talentx.co.jp/entry/2026/02/02/095343 |
| 弥生（2026-02-25） | Slack 連携でチーム開発に組み込み | 依頼〜調査ログがスレッドに残り、ジュニアの学習材料・レビューの横入り・エビデンスとして機能。`(aside)` / `mute` / `!ask` の使い分けが運用の鍵。**小さく具体的なタスクを数多く投げる**のが最も効果的 | https://tech-blog.yayoi-kk.co.jp/entry/2026/02/25/110000 |
| 弥生（2026-02-18） | Devin によるコードレビュー運用 | `.github/devin-review-prompt.md` にレビュー観点を標準化し、GitHub Actions で PR 作成・更新時に自動レビュー。`AGENTS.md` の整備でレスポンスが改善。初回セッションの遅さは課題として残る | https://tech-blog.yayoi-kk.co.jp/entry/2026/02/18/110000 |
| ネクストスケープ（2026-07-08） | Devin Desktop / Devin Local / Devin Cloud を実機検証 | Devin Local は Cascade を Rust で書き直した後継で**約30%のトークン効率向上**とサブエージェント対応。モデル選択時にコストメーターが出る点、既定の Adaptive ルーターがタスク複雑度でモデルを振り分ける点を評価。Cloud では TDD 指示から PR 自動作成まで実施 | https://blog.nextscape.net/archives/2026/07/08/102757 |

### 6-3. 事例から読み取れる実務上の示唆

1. **「強いモデル＝高コスト」は成立しない。** Cognition の公式実測（Fable + Sidekick が Opus + Sidekick より安く高スコア）と、第三者実測（Fable 5 が Opus 5 より総額で安い）が同じ方向を向いている。単価ではなく**ターン数・持ち込みコンテキスト量・委譲の巧拙**が総額を決める。
2. **Opus 5 世代ではプロンプトを削るのが移行作業。** 「必ず検証せよ」型の指示は品質を上げずコストだけを増やす（実測 +185%）。既存プロンプト資産の棚卸しが移行タスクになる。
3. **AIレビューは単独の門番にしない。** Opus 5 は精度重視レーンとしては有効だが検出率は落ちる、という第三者ベンチがある。ルーティング／アンサンブル前提で組むのが安全。
4. **Devin の投資対効果はコード生成以外で先に出やすい。** 社内QA・テスト設計・エラー調査といった「調査系」で、正答率95%・リードタイム8割削減・問い合わせ半減といった数値が公開されている。まず調査系に当て、Playbook / Knowledge / AGENTS.md の整備に投資するのが立ち上がりが速い。

---

## 参照した一次情報源一覧

- OpenAI: https://openai.com/index/previewing-gpt-5-6-sol/
- OpenAI / ChatGPT・Codex changelog: https://learn.chatgpt.com/docs/changelog
- Anthropic: https://www.anthropic.com/news/claude-opus-5
- Anthropic Platform リリースノート: https://platform.claude.com/docs/en/release-notes/overview
- Google: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/
- Cognition: https://cognition.ai/blog , https://cognition.ai/blog/swe-1-7 , https://cognition.ai/blog/introducing-devin-security-swarm , https://cognition.ai/blog/making-fable-cheaper-than-opus , https://cognition.ai/blog/devin-fedramp-high-in-process , https://cognition.ai/blog/cognition-doe-genesis-mission
- Devin: https://devin.ai/blog/introducing-pr-stacks , https://docs.devin.ai/release-notes/overview , https://docs.devin.ai/work-with-devin/stacked-prs , https://docs.devin.ai/work-with-devin/devin-review
- Anthropic Claude docs: https://docs.claude.com/en/release-notes/overview , https://docs.claude.com/en/docs/about-claude/models/whats-new-opus-5
- Claude Code CHANGELOG: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
- GitHub Changelog: https://github.blog/changelog/2026-07-01-copilot-vision-is-generally-available/ , https://github.blog/changelog/2026-07-29-copilot-code-review-agent-skills-and-mcp-now-generally-available/
- Cursor Changelog: https://cursor.com/changelog/cursor-router , https://cursor.com/changelog
- CNBC: https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html
