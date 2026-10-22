# AGENTS.md

Claudeと作ったHTMLツールを置くリポジトリ。各HTMLは単体で動く1ファイル完結を基本とし、GitHub Pagesで公開している（`https://nu424.github.io/html-okiba-byclaude/<name>.html`）。

## 新しいHTMLを追加したとき

1. `README.md` の「おしながき」に1行追加する（書式は下記）。
2. コミットしてプッシュする。コミットメッセージは既存の流儀に合わせる（例: `feat: 〇〇を追加した` / `docs: READMEに〇〇を追加した`）。
3. アイコンは作らない。ユーザーから明示的に指示されたときだけ対応する（下記「アイコン」）。

### READMEの説明文の指針

- 形式: `- [name.html](公開URL): 説明。`
- 1文、60字前後まで。末尾は「。」。
- 「何を入力して、何が得られるか」を先頭に置く。技術名（Canvas、WebGL等）より、使う人の行動で書く。
- 外部サービスや前提があれば末尾に括弧で添える（例: `（OpenRouter / Chrome内蔵AI）`）。
- 「シンプルな」「便利な」など中身のない形容は避ける。既存の行を参考に温度感を揃える。

## アイコン（ユーザーの明示的な指示があったときのみ）

配置: `assets/icons/<htmlのファイル名(拡張子なし)>.png`（256px、角丸タイル付き、角は透過）。
各HTMLの `<title>` の直後に次の2行を入れる。

```html
<link rel="icon" type="image/png" href="assets/icons/<name>.png">
<link rel="apple-touch-icon" href="assets/icons/<name>.png">
```

### スタイルガイド

- 被写体は1つ。要素は1〜2個に絞り、**太い線とベタ塗り**で描く。細線・質感・小さな装飾・文字（かな1文字や「M」程度は可）は入れない。
- 16pxのタブで見分けられることが最優先。縮小して確認する。
- 色: Claudeらしい暖色。クリーム背景 `#faf5ee`、アクセントのテラコッタオレンジ `#d97757`（1色）、主線・細部は焦げ茶 `#2b211c`。青は使わない。
- ほんのりFluent Design風: 角丸、淡い面、やわらかい雰囲気。タイル色は `#faf5ee`（`tools/make_icon.py` の `TILE`）。
- 構図: 被写体はタイルの約64%に収め、中央に置く。

### 作り方

1. `aitool generate-image` で候補を作る（1:1、1024px）。アプリごとに3案ほど並列生成し、一覧画像にまとめて見せて選んでもらう。プロンプトの骨子:

   ```
   Minimal flat app icon, rounded-square, one centered subject: <被写体>.
   Very few shapes, thick bold strokes and solid fills, high contrast, must stay
   recognizable at 16x16 pixels as a browser tab favicon. NO fine lines, NO textures,
   NO small details, no extra text. Subtle Microsoft Fluent Design feel: soft rounded
   corners, very light translucent acrylic layer and gentle soft shadow.
   No blue. warm cream background (#faf5ee). Palette: terracotta orange (#d97757)
   as the ONE accent color plus dark warm brown-black (#2b211c) for outlines.
   ```

   案の分け方: 案1=オレンジ1色＋茶の線（採用）、案2=オレンジのベタ塗り中心、案3=淡いピーチ＋オレンジ。
2. 採用画像を加工する: `python tools/make_icon.py <生成画像> assets/icons/<name>.png`
   被写体だけを切り出し、淡色の背景・影を透過にして、統一タイルの中央に再配置する（生成画像の背景色ムラを消し、全アイコンの余白と角丸を揃えるため）。
3. 該当HTMLにlinkタグを入れる。既にインラインのfaviconがあれば置き換える。
4. 一覧にして16px/256pxで見え方を確認する。

### 注意

- 生成画像の被写体に、背景の影とは別の不自然なグラデーション（縁の茶色いにじみ等）が出ることがある。切り出しでは除けないので、プロンプトに「Flat solid colors only, no gradients inside the subject」を足して再生成する。
- 時計など幾何形状は崩れやすい。「perfectly round」「symmetric」「no tick marks」と明記し、複数枚生成して一番整ったものを選ぶ。
- 生成画像は被写体の下に影が出ることがある。切り出しの閾値（`tools/make_icon.py`）を調整して影を除く。
- 候補の生成画像はリポジトリに入れない（採用後の `assets/icons/*.png` のみコミット）。
