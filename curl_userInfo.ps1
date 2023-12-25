$COOKIE_VALUE = "MTk1NjgyNzA6MTcwNDcwMjA5NDE3Mjo5MDg4N2NmYjY0NjBmN2ZiYmYyNDMxMGJiNzdjYWZiMQ"

$URL = "https://profile.callofduty.com/cod/userInfo/$COOKIE_VALUE"
$USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
$OUTPUT_FILE = "userInfo.json"

curl -v $URL -H "Cookie: ACT_SSO_COOKIE=$COOKIE_VALUE" -H "Cookie: ACT_SSO_EVENT=LOGIN_SUCCESS:1703492494179" -H "Cookie: XSRF-TOKEN:x_Pb47Lt1r4KfX5wQrYAO5moyfPKKeDT0cZ99tMBHpLpTIlVRrwTYlyMRR1AKE--" -H "User-Agent: $USER_AGENT" -o $OUTPUT_FILE