#!/bin/sh

# Webアプリケーションのリクエスト情報表示CGI（検証用）
# リクエスト情報を表示

echo "Content-Type: text/html; charset=utf-8"
echo ""

cat <<'EOF'
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>リクエスト情報</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            max-width: 1200px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 30px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .important {
            background-color: #fff3cd;
        }
        .success {
            background-color: #d4edda;
        }
        .warning {
            background-color: #f8d7da;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>コンテンツページ リクエスト情報</h1>

        <h2>クエリパラメータ</h2>
        <table>
            <tr>
                <th>パラメータ名</th>
                <th>値</th>
            </tr>
EOF

# クエリパラメータを表示
echo "            <tr><td>QUERY_STRING</td><td>${QUERY_STRING:-<em>(empty)</em>}</td></tr>"

# site_nameとcontent_pathを抽出
SITE_NAME=""
CONTENT_PATH=""
if [ -n "$QUERY_STRING" ]; then
    for param in $(echo "$QUERY_STRING" | tr '&' '\n'); do
        key=$(echo "$param" | cut -d= -f1)
        value=$(echo "$param" | cut -d= -f2- | sed 's/+/ /g')
        # URLデコード（簡易版）
        value=$(echo -e "$(echo "$value" | sed 's/%\([0-9A-F][0-9A-F]\)/\\x\1/g')")
        if [ "$key" = "site_name" ]; then
            SITE_NAME="$value"
        elif [ "$key" = "content_path" ]; then
            CONTENT_PATH="$value"
        fi
        echo "            <tr><td>$key</td><td>$value</td></tr>"
    done
fi

cat <<EOF
        </table>

        <h2>重要な環境変数</h2>
        <table>
            <tr>
                <th>変数名</th>
                <th>値</th>
                <th>説明</th>
            </tr>
            <tr class="important">
                <td>REQUEST_URI</td>
                <td><code>${REQUEST_URI:-<em>(empty)</em>}</code></td>
                <td>正規化後のURI（// は / になる）</td>
            </tr>
            <tr class="important">
                <td>PATH_INFO</td>
                <td><code>${PATH_INFO:-<em>(empty)</em>}</code></td>
                <td>正規化後のPATH_INFO</td>
            </tr>
            <tr class="important">
                <td>content_path<br/>（クエリパラメータ）</td>
                <td><code>${CONTENT_PATH:-<em>(empty)</em>}</code></td>
                <td>RewriteRuleで渡されたコンテンツパス</td>
            </tr>
        </table>

        <h2>判定結果</h2>
        <table>
            <tr>
                <th>項目</th>
                <th>判定</th>
            </tr>
EOF

# ダブルスラッシュの有無を確認
if echo "$CONTENT_PATH" | grep -q '//'; then
    echo "            <tr class=\"success\"><td>ダブルスラッシュ（//）の保持</td><td>✓ 成功（// が保持されています）</td></tr>"
else
    if echo "$REQUEST_URI" | grep -q '/content/.*//'; then
        echo "            <tr class=\"warning\"><td>ダブルスラッシュ（//）の保持</td><td>✗ 失敗（// が / に正規化されました）</td></tr>"
    else
        echo "            <tr><td>ダブルスラッシュ（//）の保持</td><td>- 元のURLに // は含まれていません</td></tr>"
    fi
fi

cat <<EOF
        </table>

        <h2>すべての環境変数</h2>
        <table>
            <tr>
                <th>変数名</th>
                <th>値</th>
            </tr>
EOF

# すべての環境変数を表示
env | sort | while IFS='=' read -r key value; do
    echo "            <tr><td>$key</td><td><code>$value</code></td></tr>"
done

cat <<'EOF'
        </table>
    </div>
</body>
</html>
EOF
