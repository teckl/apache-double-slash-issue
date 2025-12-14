# Apache 2.4系の最小構成
FROM httpd:2.4-alpine

# Apache設定をカスタマイズ（必要に応じて）
RUN echo "ServerName localhost" >> /usr/local/apache2/conf/httpd.conf

# ドキュメントルートはデフォルトの /usr/local/apache2/htdocs/ を使用

# ポート80を公開
EXPOSE 80

# Apache起動（デフォルトのCMDを使用）
# CMD ["httpd-foreground"]
