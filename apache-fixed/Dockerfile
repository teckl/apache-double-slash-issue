# Apache 2.4 - 修正版（THE_REQUESTを使ってダブルスラッシュを保持）
FROM httpd:2.4-alpine

# CGIモジュールを有効化
RUN sed -i 's/#LoadModule cgid_module/LoadModule cgid_module/' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/#LoadModule rewrite_module/LoadModule rewrite_module/' /usr/local/apache2/conf/httpd.conf

# Apache設定をカスタマイズ
COPY conf/custom.conf /usr/local/apache2/conf/extra/custom.conf
RUN echo "Include conf/extra/custom.conf" >> /usr/local/apache2/conf/httpd.conf

# ポート80を公開
EXPOSE 80
