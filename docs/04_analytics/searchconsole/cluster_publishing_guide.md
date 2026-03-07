# LogiShift クラスター記事（自動生成版） 投稿・紐付けマニュアル

このドキュメントでは、`generate_cluster_article.py`で生成されたクラスター記事（Markdown形式）をWordPressに投稿し、海外事例のピラーページ（ポータル）と正しく紐付けるための手順を記載します。

## 1. 投稿手順

1. WordPress管理画面の **「投稿」＞「新規追加」** を開きます
2. 生成されたMarkdownファイル（例：`2026-03-07_us_inventory.md`）の中身をコピーします
   ※ファイルは `media/automation/generated_articles/` フォルダに出力されています
3. WordPressの本文入力欄（ブロックエディタ）に直接ペースト（貼り付け）します
   - ペーストするだけで、Markdownの見出し、箇条書き、表組み、リンクなどが自動的にWPのブロックに変換されます
4. コピーした内容の一番上にある**YAMLフロントマター部分（`---` で囲まれた設定情報）は本文内で不要なので削除**します
5. WordPressのタイトル入力欄に、YAMLに記載されていたタイトル（または生成された見出し）を入力します

## 2. 【必須】パーマリンク（URLスラッグ）の設定

ピラーページからのリンクは、すでに各テーマに対応した「固定のスラッグ」で設計・プログラムされています。紐付けを機能させるため、**公開する前に必ずパーマリンクを以下の通りに設定**してください。

| テーマ内容 | 生成ファイル（目安） | 設定すべきURLスラッグ |
| :--- | :--- | :--- |
| **米国1（在庫精度とAMR）** | `..._us_inventory.md` | `us-inventory-accuracy-2026` |
| **米国2（ウォルマートBOPIS）** | `..._us_walmart_omni.md` | `us-walmart-omnichannel-2026` |
| **米国3（RaaS 月額ロボット）** | `..._us_raas_robotics.md` | `us-robotics-raas-model-2026` |
| **欧米1（EC誤出荷とAS/RS）** | `..._eu_picking.md` | `eu-picking-automation-2026` |
| **欧州2（リバース特化仕分け）** | `..._eu_reverse_logistics.md` | `eu-reverse-logistics-system-2026` |
| **欧米3（サステナブル自動梱包）** | `..._eu_sustainability.md` | `eu-sustainable-packaging-2026` |
| **WMS1（次世代クラウドトレンド）** | `..._global_wms.md` | `global-wms-trend-2026` |
| **WMS2（異機種連携・WES失敗例）** | `..._global_wes_fail.md` | `global-wes-integration-fail-2026` |
| **WMS3（需要予測型AI・配置最適化）** | `..._global_ai_prediction.md` | `global-wms-ai-prediction-2026` |

（※WordPress右側設定パネル ＞ URL または パーマリンク から設定可能です）

## 3. カテゴリ・タグ・アイキャッチ画像の設定（推奨）

*   **カテゴリ**: 適切なカテゴリ（例：「海外トレンド」「事例」）を選択してください。
*   **タグ**: 記事内容に応じたタグ（例：「WMS」「AMR」「ドローン棚卸し」）を設定すると、サイト内の回遊率が高まります。
*   **アイキャッチ画像**: トピックに合った画像をアイキャッチとして設定し、最後に「公開」をクリックします。

---

以上の設定で公開することで、[海外事例ピラーページ（ポータル型）](/pillar-overseas-hub/) 内のカード型リンク（ボタン）から、シームレスに該当記事へと遷移するようになります。
