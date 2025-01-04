$COOKIE_VALUE = ""
$URL = "https://profile.callofduty.com/cod/userInfo/$COOKIE_VALUE"
$USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
$OUTPUT_FILE = "userInfo.json"

curl -v "$URL" -H "Cookie: ACT_SSO_COOKIE=$COOKIE_VALUE" -H "User-Agent: $USER_AGENT" -H "Accept: application/json, text/plain, */*" -H "Referer: https://profile.callofduty.com/" -H "Connection: keep-alive" -H "Accept-Language: en-US,en;q=0.9" --cookie-jar cookies.txt --cookie cookies.txt -o $OUTPUT_FILE
