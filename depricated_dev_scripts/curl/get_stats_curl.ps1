# Set your default values here
$PROF = "" # The % replaces the # for the Activision ID (e.g. Ahrimdon%231597)
# You do not need numbers for PSN or XBL 
# Delete $PROF when getting maps and game modes.
$COOKIE_VALUE = "ACCT_SSO_COOKIE"

$URL = "AddLinkHere"
$USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
$OUTPUT_FILE = "stats.json"

curl -v $URL -H "Cookie: ACT_SSO_COOKIE=$COOKIE_VALUE" -H "User-Agent: $USER_AGENT" -o $OUTPUT_FILE