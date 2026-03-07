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
    from automation.seo_optimizer import SEOOptimizer
except ImportError:
    from gemini_client import GeminiClient
    from wp_client import WordPressClient
    from internal_linker import InternalLinkSuggester
    from seo_optimizer import SEOOptimizer

import markdown

CONFIGS = {
    "us_inventory": {
        "title": "米国の物流倉庫における『在庫精度』低下のリアルと、AMR等の最新改善事例",
        "keyword": "米国 在庫精度, 海外 倉庫事例, AMR 導入効果",
        "outline": """
[導入リード文]
日本の物流現場でも深刻な課題となる「在庫精度の低下」。実は、国土が広く労働環境の変動が激しい米国では、この課題はさらに深刻化しており、各社は「テクノロジーによる物理的な解決」を急務としています。本記事では、米国の倉庫事例から在庫精度問題の根本原因を紐解き、ドローンやAMRといった自動化ソリューションがもたらす改善効果を体系的に解説します。（※H2は見出しにしない）

## なぜ米国物流拠点の「在庫精度」は深刻な課題となるのか？
### 広大なフルフィルメントセンターにかかる探索コストとヒューマンエラーの相関
※日米の倉庫面積・環境の違いを俯瞰できる簡単なマークダウンテーブル（比較表）を挿入すること。
### 高い離職率を前提とした「属人的な棚卸しプロセス」の限界

## 精神論ではなくテクノロジーで物理的にズレを防ぐ手法
### 夜間・休日に完全稼働する「自律型ドローン棚卸し」の実態（RFID事例等）
### GTP（Goods to Person）とAMR連携によるピックミスの完全排除

## ロボティクス導入のROI（投資対効果）構造
### リアルタイム在庫同期がもたらす「商機損失」の回避効果
### 「探す時間」ゼロがもたらす倉庫作業員の定着率向上

## AMR・新型システム導入へのアプローチ要件
1. クラウドWMSによるロケーション管理の徹底と基盤構築
2. RaaSを利用した「部分自動化」のスモールスタート検証
3. ボトムアップ（現場任せ）からトップダウン（システム主導）への脱却
"""
    },
    "eu_picking": {
        "title": "北米・欧州を悩ます『誤出荷』の実態と、海外企業が導入するピッキング自動化",
        "keyword": "欧米 誤出荷, EC返品率, AS/RS, ビジョンAI, ピッキング自動化",
        "outline": """
[導入リード文]
昨今、EC市場の急成長に伴い「誤出荷」とそれに伴う「返品」にかかるコストが経営の重荷となっています。特に返品率が高止まりする欧米市場では、誤出荷を「作業員のリテラシー問題」ではなく「システムで排除すべき経営課題」として捉えています。本記事では、欧米企業がこぞって導入を進める「AS/RS（自動立体倉庫）」から「ビジョンAI自動ピッキング」に至る最新の自動化ソリューションと、その導入メリットについて体系的に解説します。（※H2は見出しにしない）

## なぜ欧米では「誤出荷」が最大の経営リスクとして扱われるのか？
### 異常に高いEC返品率とリバースロジスティクスの負荷
※誤出荷に基づく返品処理にかかるコスト・工数の増大構造をマークダウンテーブルで整理すること。
### 環境規制（サステナビリティ要件）が許さない無駄な輸送と廃棄リスク

## 最新のピッキング完全自動化ソリューション
### AS/RS（自動立体倉庫）による超高密度保管と人手介入の排除
※AutoStoreなどの仕組みと導入効果（保管効率・ピック精度向上）を具体的に解説。
### ビジョンAI ＋ アームによる無人化セルの仕組み
※人間の判断に依存しないAIカメラとロボットアーム連携による箱詰めの無人化事例。

## 返品処理（リバースロジスティクス）の自動化アプローチ
### 戻ってきたSKUをいかに速く「再商品化ライン」へ戻すかの最適化
### 専用ソーターとRFID一括識別による仕分けプロセスの自動化

## 自動化設備導入のメリット・デメリット比較指標
※導入前に知っておくべき初期コストやシステム連携の難易度など、判断材料となる比較表を作成。
"""
    },
    "global_wms": {
        "title": "【欧米WMS事情】クラウド型倉庫管理システムの進化と2026年の要件",
        "keyword": "クラウドWMS, 海外 WMS トレンド, WES 統合, API連携, 倉庫管理",
        "outline": """
[導入リード文]
自社倉庫の自動化を進める中で、複数のロボットやシステムが乱立し「全体最適化」が図れないという課題に直面していませんか？最新の海外物流トレンドにおいて、WMS（倉庫管理システム）は単なる在庫台帳から、全自動化設備を統合制御する「司令塔（オーケストレーター）」へと進化しています。本記事では、次世代クラウドWMSの要件から、WES（倉庫運用システム）の統合、API連携の重要性について網羅的に解説します。（※H2は見出しにしない）

## 限界を迎えたレガシーWMS（オンプレミス）の運用課題
### 最新の自動化機器（ロボット群）との接続ハードルの高さ
※旧来のWMSとクラウド型次世代WMSの機能差異（API連携、拡張性など）をマークダウンテーブルで比較すること。
### リアルタイム同期の遅れによる「全体最適化」の不全と機会損失

## 2026年型 次世代クラウドWMSに求められる必須要件
### API・SaaSエコシステムの広範な連携（ECカート・TMS等）
※各種ECプラットフォームや配車システム（TMS）とのシームレスな統合の価値。
### WES（倉庫運用システム）的機能の内包と複数ロボットの群制御
※異なるメーカーのAGVやAMR（異機種ロボット）を、一元的に最適化する仕組み。

## AI需要予測とWMS連携（プレディクティブモデル）
### 外部要因（天候・プロモーション等）から「明日売れる商品」を予測する機能
### 需要予測に基づき、事前に出荷ホットゾーンへ自動配置（在庫流動化）

## 次世代WMSへの移行ステップと選定基準
1. 現行システムからのデータ抽出・移行に向けた課題確認
2. クラウドSaaS型WMSの導入・技術的選定基準（オープンAPIの有無）
3. 稼働前後のベンダーサポートと運用体制の構築
"""
    },
    "us_walmart_omni": {
        "title": "米ウォルマートに学ぶ、実店舗在庫とFC在庫のオムニチャネル一元管理の実態",
        "keyword": "ウォルマート 物流, オムニチャネル, BOPIS, 店舗在庫, FC一元化",
        "outline": """
[導入リード文]
ECと実店舗の垣根がなくなる「オムニチャネル」時代の到来。米国最大の小売企業であるウォルマートは、全米の店舗網を巨大な「分散型フルフィルメント・ハブ」へと変貌させ、BOPIS（店舗受け取り）や最短配送による圧倒的な顧客体験を生み出しています。本記事では、店舗在庫と倉庫（FC）在庫を一元化するアーキテクチャや、実店舗を出荷拠点化するにあたっての技術的課題とその解決策を解説します。（※H2は見出しにしない）

## 実店舗の「フルフィルメントセンター拠点化」が強みとなる背景
### ラストマイル配送コストの圧倒的削減と「BOPIS」需要の拡大
※純粋なEC専用FCからの出荷と、最寄り店舗からの出荷（マイクロFC活用）のコスト・リードタイム差をマークダウンテーブルで比較。

## 店舗在庫・FC一元化を支える技術要素（テクノロジースタック）
### RFIDによる店舗棚在庫のスキャンと、システム上の100%リアルタイム同期
※顧客が直接触れる店舗棚の在庫変動を正確にシステムへ反映し、欠品（Null Pick）を防ぐ仕組み。
### 店舗裏（バックルーム）への超小型AS/RSやAMRの導入事例

## 実店舗在庫（オムニチャネル）完全統合化のメリット
### 物流ネットワークの一部としての店舗活用とその収益効果
### 返品（リバース）受け皿としての店舗機能統合による利益率の底上げ

## 導入時に直面する実務レベルの課題とクリアすべき要件
1. ネット在庫と店舗在庫のシステム的な完全統合ハードルとデータサイロの打破
2. 実店舗スタッフへの物流オペレーション教育とシステムによる負荷軽減策
"""
    },
    "us_raas_robotics": {
        "title": "米国市場を席巻するロボティクス『RaaSモデル』とスモールスタート戦略",
        "keyword": "RaaS, 物流ロボット サブスク, 倉庫自動化, ROI, スモールスタート",
        "outline": """
[導入リード文]
物流倉庫の自動化には「億単位の初期投資（Capex）」と「複数年にわたる回収期間」が必要だという見方は、劇的に変わりつつあります。近年、米国市場等で標準となりつつあるのが、物流ロボットを初期費用ゼロ・月額課金で導入できる「RaaS（Robot as a Service）」モデルです。本記事では、自動化をスモールスタートさせるRaaSの仕組み、ROIの大幅短縮効果、そしてメリット・デメリットの比較について詳しく解説します。（※H2は見出しにしない）

## 従来の「莫大な初期投資（Capex）」ベースの自動化が抱える課題
### 倉庫移転や物量波動に対応できない「固定設備」の硬直性
※従来の買い切り型自動倉庫・ロボット導入と、月額課金型（RaaS）の初期費用・ランニングコスト・柔軟性の違いをマークダウン表で比較。

## RaaS（Robot as a Service）のもたらす運用変革と利便性
### 繁忙期（ピーク時）にのみロボットを増設するダイナミックな労働力調整
※ホリデーシーズンに合わせて追加のAMRを一時的に稼働させる利用事例。
### クラウドWMS・オープンAPIとの連携による即日導入の可能性

## RaaSモデルのメリットと留意すべきデメリットの比較
### 「月額利用料 ＜ 削減した人件費」によるキャッシュフロー上のメリット
### ネットワークインフラ依存や契約形態といった、導入前に知るべき懸念事項

## RaaS導入前に確認すべきチェックリスト
1. 自社の物量波動（ピーク・閑散）の分析と稼働上限のシミュレーション
2. 既存のWMS/WESとの標準APIを用いたシームレスな通信連携可否
"""
    },
    "eu_reverse_logistics": {
        "title": "欧州アパレル企業における『リバースロジスティクス』特化型仕分けシステム",
        "keyword": "リバースロジスティクス, 返品物流, 欧州 アパレル, 再商品化, 自動仕分け",
        "outline": """
[導入リード文]
EC市場、特にアパレル領域において「返品」は避けて通れない事象ですが、処理工数の増大や不良在庫化は企業の利益を大きく圧迫します。返品プロセスそのものを最適化し、いかに早く「再販可能な在庫」へと復帰させるかを問う「リバースロジスティクス」の構築が経営の重要課題となっています。本記事では、環境規制の厳しい欧州アパレル企業が実践する返品自動仕分けシステムと、最速で再商品化（リストック）を行うための仕組みを解説します。（※H2は見出しにしない）

## 返品処理（リバース）が物流全体のボトルネックとなる理由
### 「戻ってきた箱を開けるまで内容が不明」という情報の非対称性
※通常の出荷（フォワード）と返品（リバース）における各作業プロセス・工数・コストの違いを表で比較整理。
### 季節外れ（シーズン落ち）による過剰廃棄リスクと価値の毀損

## 再商品化（リストック）を最速化する欧州発ソリューション
### バッグソーター（天井吊り下げ型コンベヤ）による順立出しと一次保管
※乱雑に返品されたアイテムを一時保管し、次の注文が入った瞬間に即座に出荷ラインへ排出する仕組み。
### RFIDトンネルとAIカメラによる「返品物の自動検品・真贋判定」技術

## サステナビリティ要件が牽引するリバースロジスティクスの進化
### 「廃棄禁止法」などの環境規制が、返品処理の徹底効率化を強制する背景
### 修理・クリーニング専門企業（エコシステム）とのデータ連携の広がり

## 次世代返品処理システム構築へのアクションガイド
1. 返品手続きを「見えないコスト」から「コアプロセス」への切り替え・システム設計
2. 返品商品の即時Web反映（ダイナミックリストック）を実現する業務フローの策定
"""
    },
    "eu_sustainability": {
        "title": "脱炭素と効率化の両立。欧米が推進する『サステナブル自動梱包』技術",
        "keyword": "梱包自動化, 欧米 物流, サステナビリティ, 段ボール削減, 自動梱包機",
        "outline": """
[導入リード文]
物流現場における「箱の無駄遣い」と「過剰な緩衝材」。これらは資源の浪費であるだけでなく、積載効率を低下させ、最終的な輸送コスト（容積重量）に跳ね返ってきます。特にサステナビリティ規制の厳しい欧米では、無駄を削ぎ落とす「ジャストサイズ自動梱包技術（On-Demand Packaging）」が急速に拡大しています。本記事では、梱包自動化のメカニズムと導入によるROI、削減効果の全容を解説します。（※H2は見出しにしない）

## 「空気を運ぶ」無駄がもたらすサプライチェーンのコスト増
### 輸送コスト（容積重量）の不要な高騰とトラック積載効率の悪化
※標準段ボールと緩衝材を用いた仕様と、ジャストサイズ梱包（Fit-to-Size）を実施した場合の「物理的空間」「輸送費」「CO2排出量」の違いを表で比較。

## 自動梱包機（On-Demand Packaging）のメカニズムと事例
### 3Dスキャナによる商品容積のリアルタイム計測と段ボールの自動切り出し
※商品の外寸に合わせて数秒で専用段ボールを成形し、無駄な空間を劇的に削減するプロセス。
### 環境対応：プラスチック緩衝材の全廃と100%リサイクル素材への移行

## サステナビリティ対応がもたらす劇的なコスト削減効果
### 1オーダーあたりのフルフィルメントコスト（配送費含む）の大幅な改善
### 顧客体験（CX）の向上：過剰梱包による廃棄フラストレーションの解消

## 自動梱包システム選びのチェックリスト（導入判断）
1. 自社が発送する現行荷物における「空きスペース（積載ロス）」の事前監査
2. 手作業の人件費・緩衝材費と、自動梱包ソリューションへの月額・初期投資額の厳密な比較
"""
    },
    "global_wes_fail": {
        "title": "異機種ロボット（AMR/AGV）を統合制御する「WES」導入の失敗事例（準備中）",
        "keyword": "WES, 倉庫運用システム, ロボット統合, AMR 連携, API エコシステム",
        "outline": """
[導入リード文]
近年、倉庫作業を自動化するためにメーカーの異なるロボット（AMRやAGV）やマテハン機器を一元管理する「WES（倉庫運用システム）」の導入に関心が集まっています。しかし、異なるシステムを安易につなぎ合わせることで、ロボット同士が衝突したりデータの連携エラーが発生したりする導入失敗事例も多発しています。本記事では、異機種統合の難しさと失敗パターンを分析し、正しいアーキテクチャの選定基準について解説します。（※H2は見出しにしない）

## 異機種メーカーによる「夢の統合」が招く現場の混乱リスク
### 各社独自の通信プロトコルと制御システムの物理的衝突
※旧来の「個別システム間のポイントツーポイントAPI連携」と「WESを経由した群制御」のメリット・デメリット・運用負荷の違いを表で比較。
### 予測不可能なデッドロック（ルート渋滞）による倉庫内業務の完全停止

## 失敗事例から導き出す、WES・WMSの正しい選定要件
### ベンダーロックインを回避する「オープンAPI」と「標準規格（VDA5050等）」の重要視
※欧州発のロボット共通通信規格（VDA5050）など、相互運用性を担保する動きの解説。
### リアルタイムな状況判断（渋滞回避・動的ルート生成）を支えるAIアルゴリズム性能

## 自社単独開発の限界と、SaaSエコシステム連携へのパラダイムシフト
### 個別SaaSや独自開発のみで群制御の複雑化に対応しきれない理由
### 標準化されたトップレベルのSaaS同士を繋ぎ合わせる速度的・コスト的優位性

## 新規WESシステム導入時に避けるべきアンチパターン
1. ロボット選定時に「ハードウェア」の単体性能に気を取られ、「上位接続性」を軽視すること
2. 現場の自動化機器を先行導入し、全体設計（WMS/WES）の精査を後回しにするアプローチ
"""
    },
    "global_ai_prediction": {
        "title": "データサイエンスが描く未来。WMS内蔵AIによる『需要予測型』出荷・配置最適化",
        "keyword": "AI 需要予測, WMS, 在庫配置, データサイエンス, 倉庫最適化",
        "outline": """
[導入リード文]
倉庫内オペレーションは「注文が入ってからピッキング・出荷作業を開始する」事後対応型が一般的ですが、その手法は極限の即日配送を求めるEC環境下において限界を迎えつつあります。そこで海外の先進倉庫で導入が進んでいるのが、WMS（倉庫管理システム）に内蔵されたAIが需要予測を行い、在庫を自律的に最適配置する「プレディクティブ・ロジスティクス」です。本記事では、データサイエンスを活用した次世代の在庫配置アルゴリズムと、データ基盤の重要性について解説します。（※H2は見出しにしない）

## レスポンシブ（事後対応型）物流オペレーションの決定的な限界
### 即日配送を持続・迅速化するための「数時間の捻出」の難しさ
※「通常の事後ピッキング出荷」と、「AI予測に基づく最適配置・事前準備済みの出荷」の工程とリードタイム削減効果を表で詳細に整理。

## AIによる需要予測の実態（プレディクティブ・ロジスティクス）
### 天候、プロモーション情報、SNSトレンドのWMSへの自動フィード
※「明日急激に冷え込むからコートが売れる」といった外部情報をアルゴリズムが学習し、前日の夜間（アイドルタイム）にAMR等を使って奥の棚から出荷口近く（ホットゾーン）へ在庫を自動配置替えする仕組み。
### 作業員のシフト予測と必要人員の自動計算

## AIロジスティクスを支えるデータ活用基盤の重要性
### 経験と勘による現場管理から、データサイエンスによるアルゴリズム管理への移行
### 物理設備（ロボット）投資以上に優先検討すべき、分析基盤の設計・クレンジング

## AI活用・WMS最適化のロードマップ
1. 自社のWMSが蓄積している「出荷データ」のクレンジングと分析基盤の構築
2. 在庫の「固定ロケーション」から、AI主導の「流動的ロケーション」への移行基準
"""
    }
}

SLUG_MAP = {
    "us_inventory": "us-inventory-accuracy-2026",
    "us_walmart_omni": "us-walmart-omnichannel-2026",
    "us_raas_robotics": "us-robotics-raas-model-2026",
    "eu_picking": "eu-picking-automation-2026",
    "eu_reverse_logistics": "eu-reverse-logistics-system-2026",
    "eu_sustainability": "eu-sustainable-packaging-2026",
    "global_wms": "global-wms-trend-2026",
    "global_wes_fail": "global-wes-integration-fail-2026",
    "global_ai_prediction": "global-wms-ai-prediction-2026"
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
5. **構成の厳守**: 今回提供される【対象キーワード】と【構成案】のテーマにのみ集中し、他のテーマや関係のない話題を絶対に混ぜないでください。
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
    seo = SEOOptimizer(client=gemini)
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
    
    # 5. Generate Hero Image & Publish to WordPress
    if not dry_run:
        image_path = None
        media_id = None
        print("\nGenerating hero image for the cluster article...")
        try:
            content_summary = content[:1000]  # Use first 1000 chars as summary
            image_prompt = gemini.generate_image_prompt(config["title"], content_summary, "Cluster Article")
            
            image_filename = f"{date_str}_{target_key}_hero.png"
            image_path = os.path.join(output_dir, image_filename)
            
            # Call image generation via the wrapper (DALL-E 3)
            generated_image_path = gemini.generate_image(image_prompt, image_path, aspect_ratio="16:9")
            if generated_image_path:
                print(f"✅ Hero image generated successfully: {image_filename}")
                if wp:
                    print("Uploading image to WordPress...")
                    media_data = wp.upload_media(image_path, alt_text=f"Hero image for {config['title']}")
                    if media_data:
                        media_id = media_data.get('id')
                        print(f"✅ Image uploaded, ID: {media_id}")
            else:
                print("⚠️ Failed to generate hero image.")
        except Exception as e:
            print(f"⚠️ Error during image generation: {e}")

        # 6. Publish to WordPress
        if wp and seo:
            print("\nPublishing to WordPress...")
            try:
                import requests
                # Convert markdown to HTML (removing frontmatter if present)
                md_content = content
                yaml_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                if yaml_match:
                    md_content = content[yaml_match.end():].strip()
                html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
                text_content = re.sub('<[^<]+?>', '', html_content)
                
                # Generate SEO meta
                print("Generating SEO Metadata...")
                meta_desc = seo.generate_meta_description(config["title"], text_content, config["keyword"])
                ai_summary = ""
                if hasattr(gemini, 'generate_structured_summary'):
                    try:
                        ai_summary = gemini.generate_structured_summary(text_content).get('summary', '')
                    except Exception as e:
                        print(f"Warning: Failed to generate AI summary: {e}")
                    
                seo_meta = {
                    "_yoast_wpseo_metadesc": meta_desc[:150],
                    "_yoast_wpseo_focuskw": config["keyword"],
                    "_logishift_ai_summary": ai_summary
                }
                
                slug = SLUG_MAP.get(target_key, f"cluster-{target_key}")
                
                post_data = {
                    "title": config["title"],
                    "content": html_content,
                    "status": "publish",
                    "slug": slug,
                    "meta": seo_meta
                }
                if media_id:
                    post_data["featured_media"] = media_id
                
                url = f"{wp.api_url}/posts"
                response = requests.post(url, json=post_data, auth=wp.auth)
                response.raise_for_status()
                res_json = response.json()
                print(f"🎉 Successfully published! Post ID: {res_json.get('id')} | URL: {res_json.get('link')}")
                
            except Exception as e:
                print(f"❌ Error publishing to WordPress: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(e.response.text)
        else:
            print("\nNote: WordPress or SEO client not available. Skipping auto-publish.")
        
    return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, choices=list(CONFIGS.keys()), help="Target cluster article to generate")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    args = parser.parse_args()
    
    generate_cluster_article(args.target, args.dry_run)
