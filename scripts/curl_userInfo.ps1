$COOKIE_VALUE = ""

$URL = "https://profile.callofduty.com/cod/userInfo/$COOKIE_VALUE"
$USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
$OUTPUT_FILE = "userInfo.json"

curl -v $URL -H "Cookie: ACT_SSO_COOKIE=$COOKIE_VALUE" -H "User-Agent: $USER_AGENT" -o $OUTPUT_FILE