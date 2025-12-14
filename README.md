# Apache 2.4 検証環境

Apache 2.4系の動作を検証するための最小構成Docker環境です。

## ディレクトリ構成

```
.
├── apache2/
│   └── Dockerfile          # Apache 2.4系の設定
├── www/
│   └── index.html          # 検証用HTMLファイル
├── docker-compose.yml      # Docker Compose設定
└── README.md              # このファイル
```

## 環境構築

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

### アクセス方法

起動後、以下のURLでApacheにアクセスできます：

- **Apache 2.4系**: http://localhost:8080

### 停止方法

```bash
# 停止
docker-compose down

# コンテナとイメージを削除
docker-compose down --rmi all
```

## 検証項目の例

### 1. HTTPバージョンの確認

```bash
curl -I http://localhost:8080
```

### 2. レスポンスヘッダーの確認

```bash
curl -v http://localhost:8080 2>&1 | grep -E "^< "
```

### 3. Serverヘッダーの確認

```bash
curl -I http://localhost:8080 | grep Server
```

### 4. 設定ファイルの確認

```bash
docker exec apache2 cat /usr/local/apache2/conf/httpd.conf
```

### 5. モジュール一覧の確認

```bash
docker exec apache2 httpd -M
```

## Apache 2.4の主な特徴

### アーキテクチャ

- **マルチプロセスモジュール（MPM）**: prefork/worker/event から選択可能
- **HTTP/2 サポート**: mod_http2モジュールで対応
- **マルチスレッド対応**: workerやevent MPMで効率的な処理
- **モジュラー設定**: httpd.conf + conf.d/*.conf による柔軟な設定

### セキュリティ

- デフォルトでより厳格なセキュリティ設定
- 新しいアクセス制御構文（Require ディレクティブ）
- SSL/TLS設定の改善

### パフォーマンス

- イベント駆動型MPM（event）による高パフォーマンス
- 非同期I/Oのサポート
- より効率的なメモリ使用

## トラブルシューティング

### ログの確認

```bash
# ログを確認
docker-compose logs apache2

# コンテナ内で直接確認
docker-compose exec apache2 /bin/bash
```

### ポートが既に使用されている場合

`docker-compose.yml`のportsセクションを変更してください：

```yaml
ports:
  - "8082:80"  # 8080の代わりに8082を使用
```

## カスタマイズ

### HTMLファイルの追加

`www/`ディレクトリにファイルを追加すると、Apacheで公開されます。

### Apache設定のカスタマイズ

`apache2/Dockerfile`を編集してApacheの設定を変更できます。

設定ファイルの例：

```dockerfile
# カスタム設定を追加
RUN echo "LoadModule rewrite_module modules/mod_rewrite.so" >> /usr/local/apache2/conf/httpd.conf
```

## 参考資料

- [Apache HTTP Server 公式サイト](https://httpd.apache.org/)
- [Apache 2.4 ドキュメント](https://httpd.apache.org/docs/2.4/)
- [Docker Official Image - httpd](https://hub.docker.com/_/httpd)

## ライセンス

MIT
