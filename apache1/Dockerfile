# Apache 1.3系の最小構成
# Apache 1.3は非常に古いため、Debian Wheezy (7.0)を使用
FROM debian:wheezy

# セキュリティリポジトリをアーカイブに変更（Wheezyは既にEOL）
RUN echo "deb http://archive.debian.org/debian/ wheezy main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security/ wheezy/updates main" >> /etc/apt/sources.list && \
    echo "Acquire::Check-Valid-Until false;" > /etc/apt/apt.conf.d/99no-check-valid-until

# Apache 1.3をインストール
RUN apt-get update && \
    apt-get install -y apache && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apache設定
RUN echo "ServerName localhost" >> /etc/apache/httpd.conf

# ドキュメントルートを作成
RUN mkdir -p /var/www/html

# ポート80を公開
EXPOSE 80

# Apache起動コマンド
CMD ["/usr/sbin/apache", "-D", "FOREGROUND", "-X"]
