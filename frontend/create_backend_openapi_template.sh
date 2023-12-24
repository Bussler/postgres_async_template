cd ../backend
python create_openapi.py
cd ../
docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
    -i /local/backend/openapi.json \
    -g typescript-fetch \
    -o /local/frontend/src/generated-sources
chown -R "$USER:$USER" frontend/src/generated-sources