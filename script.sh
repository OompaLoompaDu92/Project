# take the url of the site
url="https://finance.yahoo.com/quote/%5EFTSE?p=^FTSE&.tsrc=fin-srch"

# Fetch the content of the web page
CONTENT=$(curl -s "$url")

# Extract the FTSE 100 index value using pup
FTSE100_VALUE=$(echo "$CONTENT" | grep -o '<fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="^FTSE" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value=".*" active="">.*</fin-streamer>' | grep -o 'value="[0-9,.]\+"' | grep -o '[0-9,.]\+')


# Print the result in 3 columns (date of today, current time, value of the stock index)
echo "$(date +'%Y-%m-%d'),$(date -d "2 hours $(date '+%T')" '+%T'),$FTSE100_VALUE" >> FTSE100_VALUE.txt


