# Apache 2.4 ダブルスラッシュ問題 検証環境

Apache 2.4において、URLに含まれるダブルスラッシュ（`//`）が単一のスラッシュ（`/`）に正規化される問題を検証・修正するための環境です。

## 問題の概要

Apache 2.4では、URLパスの正規化が標準で有効になっており、連続するスラッシュ（`//`）が単一のスラッシュ（`/`）に変換されます。

### 具体例

```
リクエスト: /myapp/content/Revolution//Evolution
↓ Apache 2.4で正規化
実際の処理: /myapp/content/Revolution/Evolution
```

これにより、コンテンツパスに `//` を含むURLが正しく処理されなくなります。

### 影響範囲

- パス名に `//` を含むコンテンツ（例: `.hack//MOE`、`http://example.com/`）
- 特殊文字などで `//` を使用しているパス（例: `(//∇//)`）

## 検証環境の構成

この環境では、2つの異なる設定のApacheコンテナを起動します：

| コンテナ名 | ポート | 説明 |
|-----------|--------|------|
| apache-default | 8080 | デフォルト設定（問題が発生） |
| apache-fixed | 8081 | 修正版（THE_REQUESTを使用） |

## セットアップ

### 前提条件

- Docker
- Docker Compose

### 起動方法

```bash
# コンテナをビルドして起動
docker-compose up --build

# バックグラウンドで起動する場合
docker-compose up -d --build
```

### 停止方法

```bash
docker-compose down
```

## 検証方法

### 1. デフォルト設定での動作確認（問題再現）

```bash
# ダブルスラッシュを含むURLにアクセス
curl "http://localhost:8080/myapp/content/Revolution//Evolution"

# または、ブラウザで以下にアクセス
http://localhost:8080/myapp/content/Revolution//Evolution
```

**期待される結果**: content_pathが `Revolution/Evolution` と表示される（`//` が `/` に変換されている）

### 2. 修正版での動作確認（修正後）

```bash
# 同じURLにアクセス
curl "http://localhost:8081/myapp/content/Revolution//Evolution"

# または、ブラウザで以下にアクセス
http://localhost:8081/myapp/content/Revolution//Evolution
```

**期待される結果**: content_pathが `Revolution//Evolution` と表示される（`//` が保持されている）

### 3. 様々なパターンでのテスト

```bash
# .hack//MOE の例
curl "http://localhost:8080/myapp/content/.hack//MOE"
curl "http://localhost:8081/myapp/content/.hack//MOE"

# 3つ以上のスラッシュ
curl "http://localhost:8080/myapp/content/test///multi"
curl "http://localhost:8081/myapp/content/test///multi"

# URLを含むパス
curl "http://localhost:8080/myapp/content/http://example.com/"
curl "http://localhost:8081/myapp/content/http://example.com/"
```

## 修正方法の詳細

### 問題の原因

Apache 2.4では、`RewriteRule`の`$2`などのキャプチャグループには、既に正規化されたURLが渡されます。

```apache
# 問題のある設定
RewriteRule ^/([a-zA-Z0-9_\-\.]+)/content/(.*)$ /cgi-bin/show.cgi?content_path=$2 [PT,L,QSA]
# $2 には正規化後の値が入る（// → /）
```

### 解決策: THE_REQUESTを使用

`THE_REQUEST` 変数には、正規化される前の元のHTTPリクエストラインが含まれています。

```apache
# 修正版の設定
# THE_REQUESTから元のコンテンツパスを抽出
RewriteCond %{THE_REQUEST} "\s/(?:[^\s/]+)/content/([^\s\?]*)"
RewriteRule .* - [E=RAW_CONTENT_PATH:%1]

# 環境変数を使用してコンテンツパスを渡す
RewriteRule ^/([a-zA-Z0-9_\-\.]+)/content/(.*)$ /cgi-bin/show.cgi?content_path=%{ENV:RAW_CONTENT_PATH} [PT,L,QSA]
```

### THE_REQUESTの内容

`THE_REQUEST` には以下のような形式でリクエスト情報が含まれます：

```
GET /myapp/content/Revolution//Evolution HTTP/1.1
```

この値は正規化される前のURLを含んでいるため、`//` も保持されています。

## 設定ファイルの比較

### デフォルト設定（apache-default/conf/custom.conf）

```apache
RewriteRule ^/([a-zA-Z0-9_\-\.]+)/content/(.*)$ /cgi-bin/show.cgi?site_name=$1&content_path=$2 [PT,L,QSA]
```

### 修正版（apache-fixed/conf/custom.conf）

```apache
# THE_REQUESTから元のコンテンツパスを取得
RewriteCond %{THE_REQUEST} "\s/(?:[^\s/]+)/content/([^\s\?]*)"
RewriteRule .* - [E=RAW_CONTENT_PATH:%1]

# 環境変数を使用
RewriteRule ^/([a-zA-Z0-9_\-\.]+)/content/(.*)$ /cgi-bin/show.cgi?site_name=$1&content_path=%{ENV:RAW_CONTENT_PATH} [PT,L,QSA]
```

## ディレクトリ構成

```
.
├── apache-default/
│   ├── Dockerfile
│   └── conf/
│       └── custom.conf       # デフォルト設定
├── apache-fixed/
│   ├── Dockerfile
│   └── conf/
│       └── custom.conf       # 修正版設定
├── cgi-bin/
│   └── show.cgi              # リクエスト情報を表示するCGI
├── docker-compose.yml        # Docker Compose設定
└── DOUBLE_SLASH_TEST.md     # このファイル
```

## トラブルシューティング

### ポートが既に使用されている場合

`docker-compose.yml`のportsセクションを変更してください：

```yaml
ports:
  - "8082:80"  # 8080の代わりに8082を使用
```

### CGIが実行されない場合

CGIスクリプトに実行権限があることを確認してください：

```bash
chmod +x cgi-bin/show.cgi
```

### コンテナのログを確認

```bash
# デフォルト設定のログ
docker-compose logs apache-default

# 修正版のログ
docker-compose logs apache-fixed
```

## 参考資料

- [Apache 2.4 mod_rewrite Documentation](https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html)
- [Apache 2.4 Upgrading Guide](https://httpd.apache.org/docs/2.4/upgrading.html)

## 実用例

この問題は、以下のようなシステムで発生する可能性があります：

- ユーザー生成コンテンツを扱うシステム（コンテンツ名/パスに特殊文字を許可している場合）
- レガシーシステムからの移行（古いApacheバージョンで動作していたURL構造）
- 外部システムとの統合（既存のURL構造を維持する必要がある場合）
