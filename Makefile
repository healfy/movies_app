# General commands to for serivce management
PROJECT=movies_app
REGISTRY_BASE_URL=baratrum/movies
SERVICE=movies
# By default is used dev env, it can be overidden by setting PROD=1 or STAGE=1
PROD ?= 0
STAGE ?= 0
ifeq ($(PROD), 1)
	ENV=prod
	IMAGE_TAG=prod
else ifeq ($(STAGE), 1)
	ENV=stage
	IMAGE_TAG=stage
else
	ENV=dev
	IMAGE_TAG=dev
endif

DEPLOYMENT_FILE=deployment-$(ENV).yaml

all: build

# Build and push docker main image with source code
build: IMAGE_URL=$(REGISTRY_BASE_URL):$(IMAGE_TAG)
build: _build

# build command template
_build:
	docker build . --tag $(IMAGE_URL)
	docker push $(IMAGE_URL)


# Deploy built image into kuberntes
deploy: DEPLOYMENT_FILE_TMP=/tmp/$(SERVICE)-$(DEPLOYMENT_FILE)
deploy: build
	sed -re "s=COMMIT_HASH=`git rev-parse HEAD`=" $(DEPLOYMENT_FILE) > $(DEPLOYMENT_FILE_TMP)
	echo "*** DEPLOYING ***"
	kubectl apply -f $(DEPLOYMENT_FILE_TMP)
	rm -rf $(DEPLOYMENT_FILE_TMP)
