# Set your default values here
$PROF = "Ahrimdon%231597" # The % replaces the # for the Activision ID
$COOKIE_VALUE = "INSERT ACT_SSO_COOKIE COOKIE HERE FOR AUTHENTICATION"

$URL = "https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/battle/gamer/$PROF/profile/type/mp"
$USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
$OUTPUT_FILE = "stats.json"

curl -v $URL -H "Cookie: ACT_SSO_COOKIE=$COOKIE_VALUE" -H "User-Agent: $USER_AGENT" -o $OUTPUT_FILE