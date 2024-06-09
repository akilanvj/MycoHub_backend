for i in $(seq 0 24); do
  curl -X 'POST' \
    'http://127.0.0.1:8000/items/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d "$(jq .[$i] items.json)"
done
