#!/usr/bin/env python3
"""
LogiShift Cluster Article Generator
Generates pillar-related cluster articles with a predefined structure, 
including automatic internal linking to recent flow articles.

Usage: 
  python3 generate_cluster_article.py --target us_inventory
"""
import argparse
import os
import sys
import json
import re
from datetime import datetime

# Adjust path to import automation modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from automation.gemini_client import GeminiClient
    from automation.wp_client import WordPressClient
    from automation.internal_linker import InternalLinkSuggester
except ImportError:
    from gemini_client import GeminiClient
    from wp_client import WordPressClient
    from internal_linker import InternalLinkSuggester

CONFIGS = {
    "us_inventory": {
        "title": "米国の物流倉庫における『在庫精度』低下のリアルと、AMR等の最新改善事例",
        "keyword": "米国 在庫精度, 海外 倉庫事例, AMR 導入効果",
        "outline": """
[導入リード文]
日本以上にシビアな米国の在庫精度の現状と、本記事の目的。（※H2は見出しにしない）

## なぜ米国の物流倉庫は「在庫精度」が低いのか？
### 広大なフルフィルメントセンターにかかる探索コストの罠
※日米の倉庫面積・離職率の違いを俯瞰できる簡単なマークダウンテーブル（比較表）を挿入すること。
### 高い離職率と属人的な「棚卸しプロセス」の崩壊

## 精神論ではなく「テクノロジー」で物理的にズレを防ぐ
### 夜間・休日に完全稼働する「自律型ドローン棚卸し」の実態と仕組み（RFID連動）
### GTP（Goods to Person）とAMR連携によるピックミス撲滅

## LogiShiftの視点：大手小売（Amazon等）に学ぶ、在庫精度向上のROI
### リアルタイム在庫同期がもたらす機会損失の回避
### 「探す時間」ゼロがもたらす作業員エンゲージメントの向上

## まとめ：明日から意識すべきアクション（日本企業への提言）
1. クラウドWMSによるロケーション管理の徹底
2. RaaSを利用した「部分自動化」のスモールスタート
3. 精神論からの脱却
"""
    },
    "eu_picking": {
        "title": "北米・欧州を悩ます『誤出荷』の実態と、海外企業が導入するピッキング自動化",
        "keyword": "欧米 誤出荷, EC返品率, AS/RS, ビジョンAI, ピッキング自動化",
        "outline": """
[導入リード文]
「ブラケティング（まとめ買いと無料返品）」文化が根付く欧米市場において、倉庫側のミス（誤出荷）が引き起こす致命的なコストと環境負荷についての問題提起。本記事の目的。（※H2は見出しにしない）

## なぜ欧米では「誤出荷」が最大の経営リスクなのか？
### 異常に高いEC返品率とリバースロジスティクスの負荷
※欧米の返品率の高さや返品処理にかかるコスト構造をマークダウンテーブルで整理すること。
### 環境規制（サステナビリティ要件）が許さない無駄な輸送と廃棄

## ヒューマンエラーを「ゼロ」にするピッキング完全自動化
### AS/RS（自動立体倉庫）による超高密度保管と人手介入の排除
※AutoStoreなどのキューブ型倉庫群の仕組みと導入効果（保管効率・ピック精度）を具体的に解説。
### ビジョンAI ＋ アームによる無人化セルの衝撃
※人間の判断に依存しないAIカメラとロボットアームの連携による箱詰めの自動化事例。

## LogiShiftの視点：返品処理（リバース）の高速化という新たな戦場
### 戻ってきたSKUをいかに速く「再商品化ライン」へ戻すか
### 専用ソーターとRFID一括識別による仕分けの自動化

## まとめ：明日から意識すべきアクション（日本企業への提言）
1. 「ミスは起きるもの」という前提に立ち、検品プロセスをシステムで強固にする
2. 返品（リバースロジスティクス）のコストを可視化し、自動化投資のROIに組み込む
3. ピッキング作業から「探す・判断する」プロセスを排除する仕組み作り
"""
    },
    "global_wms": {
        "title": "【欧米WMS事情】クラウド型倉庫管理システムの進化と2026年の要件",
        "keyword": "クラウドWMS, 海外 WMS トレンド, WES 統合, API連携, 倉庫管理",
        "outline": """
[導入リード文]
数万坪の自動化設備も、優れた頭脳であるWMS（倉庫管理システム）なしには稼働しない。レガシーなオンプレミス台帳から「オーケストレーター」へと進化する次世代WMSの海外トレンドを読み解く。（※H2は見出しにしない）

## 限界を迎えたレガシーWMS（オンプレミス）の課題
### 自動化機器（ロボット群）との接続ハードルの高さ
※旧来のWMSと次世代クラウドWMSの機能差異（API連携速度、WES機能の有無など）をマークダウンテーブルで比較すること。
### リアルタイム同期の遅れによる「全体最適化」の不全

## 2026年、次世代クラウドWMSに求められる必須要件
### API・SaaSエコシステムの広範な連携（ヘッドレスコマース・TMS）
※ShopifyなどのECプラットフォームや配車システム（TMS）とのシームレスな統合事例。
### WES（倉庫運用システム）的機能の内包：複数ロボットの群制御
※異なるメーカーのAGVやAMR（異機種ロボット群）を、WMSがハブとなって一元的に最適化する仕組み。

## LogiShiftの視点：予測エンジンに基づく「自律的最適化」の時代
### 過去データと外部要因（天候等）から「明日売れる商品」を予測
### 需要予測に基づき、事前に出荷ホットゾーンへ在庫を自動配置する（在庫流動化）

## まとめ：明日から意識すべきアクション（日本企業への提言）
1. 自社開発やオンプレミスのレガシーシステムからの脱却（クラウドSaaSへの移行）
2. WMSを単なる「在庫台帳」ではなく「自動化システムの司令塔（オーケストレーター）」として再定義する
3. システム選定において、他社SaaSやロボットAPI群との「連携性（オープンさ）」を最優先する
"""
    },
    "us_walmart_omni": {
        "title": "米ウォルマートに学ぶ、実店舗在庫とFC在庫のオムニチャネル一元管理の実態",
        "keyword": "ウォルマート 物流, オムニチャネル, BOPIS, 店舗在庫, FC一元化",
        "outline": """
[導入リード文]
Amazonに対抗する最大の小売巨人・ウォルマートがいかにして全米の店舗網を巨大な「分散ロジスティクスハブ」へと変貌させているか、その裏側にある強力な在庫同期システムとROIについて深掘りする。

## なぜ「店舗在庫」をフルフィルメント（FC）に組み込むのか
### ラストマイル配送コストの圧倒的な削減と「BOPIS」需要の爆発
※純粋なEC専用FCから出荷する場合と、最寄り店舗の裏側（マイクロFC）から出荷・受け渡しする場合のコスト差とリードタイム差をマークダウンテーブルで比較。

## 実店舗を「出荷拠点化」するための技術スタック
### RFIDによる店舗棚在庫と100%のリアルタイム同期
※顧客が直接触れる店舗棚の在庫変動をいかに正確に捉え、欠品（Null Pick）を防ぐか。
### 店舗裏（バックルーム）への超小型AS/RSとAMRの導入事例

## LogiShiftの視点：Amazonの弱点を突く物理的ネットワークの強み
### 「返品」の受け皿としての店舗機能の再定義（リバースロジスティクスの統合）
### 物流と実店舗の境界線が消える2026年のオムニチャネル戦略

## まとめ：明日から意識すべきアクション（日本企業への提言）
1. ネットと店舗で別々に管理されている在庫データの完全統合
2. 店舗のバックルームを利用した「店舗出荷型（Ship from Store）」の検証
"""
    },
    "us_raas_robotics": {
        "title": "米国市場を席巻するロボティクス『RaaSモデル』とスモールスタート戦略",
        "keyword": "RaaS, 物流ロボット サブスク, 倉庫自動化, ROI, スモールスタート",
        "outline": """
[導入リード文]
億単位の初期投資が必要だった自動倉庫時代は終わりを迎えた。「Robot as a Service (RaaS)」サブスクリプションにより、中小規模の米国倉庫がいかに素早く・低リスクで自動化を果たしているか解説。

## 莫大な初期投資（Capex）からの脱却
### 倉庫移転や波動に対応できない硬直化した「固定設備」の限界
※従来の買い切り型自動倉庫（AS/RS等）と、月額課金型（RaaS）AMRの初期投資・ランニングコスト・柔軟性の違いをマークダウン表で比較。

## RaaS（Robot as a Service）がもたらす破壊的変化
### 繁忙期（ピークシーズン）だけロボットを「増員」するダイナミックな労働力調整
※ホリデーシーズンに合わせて追加のAMRを稼働させ、終了後に返却するLocus Robotics等の事例。
### 即日導入、即日稼働を可能にするクラウドWMSとの連携

## LogiShiftの視点：ロボット導入のROIを数年から「数ヶ月」へ圧縮
### 導入初日から「支払額 ＜ 削減した人件費」を実現するキャッシュフローモデル
### ハードウェアの陳腐化リスクをサプライヤーに負わせる戦略的意義

## まとめ：日本企業のアクション（提言）
1. 億単位の予算取りを待つのではなく、月数十万の経費（Opex）で実証実験を開始する
2. 完全自動化を目指さず「人とロボットの協働（ピッキング支援）」で早期効果を狙う
"""
    },
    "eu_reverse_logistics": {
        "title": "欧州アパレル企業における『リバースロジスティクス』特化型仕分けシステム",
        "keyword": "リバースロジスティクス, 返品物流, 欧州 アパレル, 再商品化, 自動仕分け",
        "outline": """
[導入リード文]
返品をコストではなく「再商品化レース」と捉え直す欧州エコシステム。ファッション・アパレル業界における返品物流（リバースロジスティクス）を黒字化するための専用ソリューションに迫る。

## なぜ返品処理（リバース）が物流のボトルネックとなるのか
### 「戻ってきた箱を開けるまで何が入っているか分からない」情報の非対称性
※出荷（フォワード）と返品（リバース）における作業プロセスの違いやハードルの高さを表で比較整理。
### 季節外れ（シーズン落ち）による価値の急速な毀損と廃棄コスト

## 再商品化（リストック）を最速化する欧州発のリバースソリューション
### バッグソーター（天井吊り下げ型コンベヤ）による順立出しと一次保管
※乱雑に返品された個別アイテムを一時保管し、次の注文が入った瞬間に即座に出荷ラインへ自動排出する仕組み。
### RFIDトンネルとAIカメラによる「返品物の自動検品・真贋判定」の萌芽

## LogiShiftの視点：サステナビリティ規制が後押しするエコシステム化
### 「廃棄禁止法」などの環境要件がリバースの効率化を強制する背景
### 修理・クリーニング専門企業とのデータエコシステム連携

## まとめ：日本企業への提言
1. 返品を「例外処理」ではなく「コアプロセス」としてWMS内で設計する
2. 返品商品の即時EC再販（ダイナミックリストック）を実現するシステムフローの構築
"""
    },
    "eu_sustainability": {
        "title": "脱炭素と効率化の両立。欧米が推進する『サステナブル自動梱包』技術",
        "keyword": "梱包自動化, 欧米 物流, サステナビリティ, 段ボール削減, 自動梱包機",
        "outline": """
[導入リード文]
「空気を運ぶ」無駄を一掃し、環境負荷と輸送コストを同時削減する。欧米における最新のジャストサイズ自動梱包技術（On-Demand Packaging）の真価と導入効果。

## 「空気を運ぶ」無駄がもたらす致命的なコスト増
### 輸送コスト（容積重量）の高騰と積載効率の悪化
※商品に対して大きすぎる標準段ボールを使用し緩衝材を詰めた場合と、ジャストサイズ梱包（Fit-to-Size）した場合の「空間浪費」「輸送費」「CO2排出量」の違いを表で比較。

## 自動梱包機（On-Demand Packaging）のメカニズム
### 3Dスキャナによる商品容積のリアルタイム計測と段ボールの自動切り出し
※Packsize社などの技術事例。商品の外寸に合わせて数秒で専用段ボールを成形し、無駄な空間をゼロにするプロセス。
### プラスチック緩衝材（プチプチ等）の完全廃止と100%リサイクル化

## LogiShiftの視点：サステナビリティは「CSR」から「コスト削減の切り札」へ
### 1商品あたりのフルフィルメントコスト（配送費含む）の劇的な改善効果
### 顧客体験（CX）の向上：開封体験（Unboxing）の簡素化とゴミ問題の解消

## まとめ：日本企業への提言
1. 自社の「容積重量（Dim Weight）」の無駄を可視化・監査する
2. 汎用段ボール数種類による手作業梱包から、自動梱包機による個別最適化への移行検討
"""
    },
    "global_wes_fail": {
        "title": "異機種ロボット（AMR/AGV）を統合制御する「WES」導入の失敗事例（準備中）",
        "keyword": "WES, 倉庫運用システム, ロボット統合, AMR 連携, API エコシステム",
        "outline": """
[導入リード文]
A社の無人搬送車とB社のピッキングロボット。異なるメーカーの群制御を夢見てWES（Warehouse Execution System）を導入したものの、実稼働で大惨事を招いた海外のリアルな失敗事例から、正しいアーキテクチャの選び方を学ぶ。

## 「夢の統合」が招く現場の混乱（サイロ化の罠）
### 各メーカー独自の通信プロトコルと制御網の衝突
※旧来の「ポイント・ツー・ポイント接続（各システム間の個別API連携）」と「WESを中心としたハブ＆スポーク型連携」の保守性・拡張性の違いを表で比較。
### デッドロック（ロボット同士の渋滞）による倉庫全体のトラフィック崩壊

## 失敗から学ぶ、WESの正しい選定基準
### ベンダーロックインを避ける「オープンAPI」と「標準規格（VDA5050等）」の重要性
※欧州発のロボット共通通信規格（VDA5050）がいかに相互運用性を高めているか。
### リアルタイムな状況判断（渋滞回避・迂回ルート生成）を支えるAIアルゴリズム

## LogiShiftの視点：自社開発の終焉と「エコシステム」への参加
### もはや単独のソフトウェアベンダー（あるいは自社開発）では群制御の複雑性に太刀打ちできない
### トップSaaSエコシステムに相乗りすることの速度的・コスト的優位性

## まとめ：日本企業への提言
1. ロボット選定時にハードウェアスペック以上に「外部システムとの接続性（APIの質）」を評価する
2. 全体のオーケストレーションを担う上位システム（WMS/WES）側の設計を先に固める
"""
    },
    "global_ai_prediction": {
        "title": "データサイエンスが描く未来。WMS内蔵AIによる『需要予測型』出荷・配置最適化",
        "keyword": "AI 需要予測, WMS, 在庫配置, データサイエンス, 倉庫最適化",
        "outline": """
[導入リード文]
「注文が入ってから」動く時代は終わる。次世代WMSが膨大な過去データと外部API（天候やSNSトレンド等）を掛け合わせ、「明日何が売れ、どこに配置しておくべきか」を事前に自律指示する世界観を解説。

## レスポンシブ（事後対応型）物流からの脱却
### 即日・翌日配送の限界突破に必要な「数時間」の捻出
※注文後の「ピッキング〜出荷準備時間」と、予測に基づいて最適配置済みの商品の「出荷準備時間」の違い（リードタイム削減効果）を表で整理。

## AIによる予測的（プレディクティブ）ロジスティクスの実態
### 天候、プロモーション情報、SNSトレンドのWMSへの自動フィード
※「明日急激に冷え込むからコートが売れる」といった外部情報をアルゴリズムが学習し、前日の夜間（アイドルタイム）にAMR等を使って奥の棚から出荷口近く（ホットゾーン）へ在庫を自動配置替えする仕組み。
### 作業員のシフト予測と必要人員の自動計算

## LogiShiftの視点：データを「貯める」から「使って動かす」へのパラダイムシフト
### 経験と勘による現場管理を、データサイエンスによるアルゴリズム管理へ
### 経営陣が投資すべきはハードウェア（倉庫の箱やロボット）以上に、それを動かす頭脳（データ基盤）

## まとめ：日本企業への提言
1. 自社のWMSが蓄積している「出荷データ」のクレンジングと分析基盤の構築
2. 在庫の「固定ロケーション（ABC分析の固定化）」を捨て、AI主導の「流動的ロケーション」を受け入れる組織風土の醸成
"""
    }
}

SYSTEM_INSTRUCTION = """
あなたは、物流業界向けの専門メディア「LogiShift」のシニア・エディターです。
今回はピラーページからリンクされる「クラスター記事」を生成します。

【厳守するトーン＆マナー（LogiShift標準仕様）】
1. **文体**: 専門的だが分かりやすい「です・ます」調。読者（物流現場のリーダー、経営層）に実践的な示唆を与える「提言型」のトーン。
2. **フォーマット**: 
   - YAMLフロントマターから開始すること。必要なキーは `title`, `date`, `keyword`。
   - 導入部には必ず端的なリード文を書くこと（H2は見出しとして使わない）。
   - 各セクションで指示された構造（H2, H3）を必ず守ること。
   - 【必須】情報・比較等は箇条書きだけでなく、積極的にMarkdownの「テーブル（表）」を用いて図解・整理すること。
3. **内部リンク**: 
   - 後述される「関連フロー記事」の情報を参考に、セクションの終わりの自然な箇所で `参考記事: [記事タイトル](URL)` の形式の内部リンクを挿入すること。
4. **具体性と深掘り（圧倒的な情報量）**: 一般論や表面的な解説に終始せず、米国におけるドローン棚卸しやAMRなどの最新テクノロジー事例について、「具体的な数値（コスト削減率、ROI、離職率など）」を交えて徹底的に深掘りしてください。各見出し（H3）に対してプロの視点で十分な解説を行い、全体として「3000〜4000文字程度」の読み応えと説得力のある重厚な記事に仕上げること。内容が薄い構成は絶対に避けてください。
"""

def generate_cluster_article(target_key, dry_run=False):
    config = CONFIGS.get(target_key)
    if not config:
        print(f"Error: Unknown target '{target_key}'")
        sys.exit(1)
        
    print(f"Starting generation for: {config['title']}")
    
    # 1. Init clients
    print("Initializing clients...")
    gemini = GeminiClient()
    try:
        wp = WordPressClient()
        linker = InternalLinkSuggester(wp, gemini)
        print("WordPress Client & Internal Linker initialized.")
    except Exception as e:
        print(f"WP Client Init Error (Linking will be skipped): {e}")
        wp = None
        linker = None

    # 2. Get internal links context
    internal_links_context = ""
    if linker is not None:
        print("Fetching internal link candidates from LogiShift...")
        try:
            candidates = linker.fetch_candidates(limit=20)
            scoring_context = f"Keyword: {config['keyword']}\nOutline:\n{config['outline']}"
            relevant_links = linker.score_relevance(config['keyword'], scoring_context, candidates)
            
            if relevant_links:
                print(f"Found {len(relevant_links)} relevant links.")
                links_text = "\n".join([f"- Title: {l['title']} | URL: {l['url']}" for l in relevant_links])
                internal_links_context = f"\n\n【関連フロー記事（内部リンク候補）】\n以下の既存記事から、文脈に関係の深いものを `参考記事: [記事タイトル](URL)` として記事中の適切なセクションや末尾に、自然な形で挿入（最大2,3個まで）してください。\n{links_text}"
            else:
                print("No strictly relevant links found above the threshold.")
        except Exception as e:
            print(f"Warning: Internal linking calculation failed: {e}")
            
    # 3. Build Prompt
    prompt = f"""{SYSTEM_INSTRUCTION}

以下の構成案と条件に従い、クラスター記事のマークダウン原稿を作成してください。

【対象キーワード】: {config['keyword']}
【記事タイトル】: {config['title']}
【構成案】:
{config['outline']}
{internal_links_context}

出力はYAMLフロントマターを含めたMarkdownテキストのみとしてください（コードブロックの ```markdown や ``` で全体を囲まないこと）。
"""

    print("Requesting content from Gemini (this may take a minute)...")
    response = gemini.generate_content(prompt)
    
    if not response or not response.text:
        print("Failed to generate content.")
        return False
        
    content = response.text
    # Cleanup markdown block if Gemini still adds it
    if content.startswith("```markdown"):
        content = content[11:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()
    
    # 4. Save to file
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{target_key}.md"
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_articles")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"✅ Article generated successfully: {filepath}")
    
    # 5. Generate Hero Image
    if not dry_run:
        print("\nGenerating hero image for the cluster article...")
        try:
            content_summary = content[:1000]  # Use first 1000 chars as summary
            image_prompt = gemini.generate_image_prompt(config["title"], content_summary, "Cluster Article")
            print(f"Image prompt generated.")
            
            image_filename = f"{date_str}_{target_key}_hero.png"
            image_path = os.path.join(output_dir, image_filename)
            
            # Call image generation via the wrapper (DALL-E 3)
            generated_image_path = gemini.generate_image(image_prompt, image_path, aspect_ratio="16:9")
            if generated_image_path:
                print(f"✅ Hero image generated successfully: {image_filename}")
            else:
                print("⚠️ Failed to generate hero image.")
        except Exception as e:
            print(f"⚠️ Error during image generation: {e}")

        print("\nNote: In this flow, please manually check the generated markdown and image, then publish to WordPress.")
        
    return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, choices=list(CONFIGS.keys()), help="Target cluster article to generate")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    args = parser.parse_args()
    
    generate_cluster_article(args.target, args.dry_run)
