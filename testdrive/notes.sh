
export REGISTRY=registry.podbox.io:5000
export DOCKER_BUILDKIT=0
export COMPOSE_DOCKER_CLI_BUILD=0
APP_OWNER=vkraskov
APP_NAME=ocrapp
APP_VERSION=1.3.0
WORK_DIR=$PWD
docker build ${WORK_DIR} -t ${REGISTRY}/${APP_NAME}:latest -t ${REGISTRY}/${APP_NAME}:${APP_VERSION}
docker image push --all-tags ${REGISTRY}/${APP_NAME}

# curl https://registry.podbox.io:5000/v2/ocrapp/tags/list

docker images
CONTAINTER_ID=`docker run -d -p 8000:8080 -e APP_API_HOST='0.0.0.0' -e APP_API_PORT=8080 registry.podbox.io:5000/ocrapp`
export CONTAINTER_ID
docker exec -it ${CONTAINTER_ID} /bin/bash
curl 'http://localhost:8000/'

cd testdrive
python test.py

docker stop ${CONTAINTER_ID}
docker rm ${CONTAINTER_ID}
docker ps

#(ocrapp-pyQh3D9X-py3.9) (base) ntb-pinal:testdrive vkraskov$ python test.py
#{"status": "ok", "text": "XUNAN DYNASTY BE\n\n     \n    \n\nCHINESE % fs\nRESTAURANT |\n\nWE NOT SEE YOUR\nCAT. STOP ASKING\nTRY OUR CHICKEN\n\nIT'S PURRRFECT\n\f"}


