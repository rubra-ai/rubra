.PHONY: create-tag

TAG := $(or $(TAG),main)
GITHUB_WORKFLOW := $(or $(GITHUB_WORKFLOW),local)
REGISTRY := $(or $(REGISTRY),index.docker.io)
PLATFORMS := linux/amd64,linux/arm64
BUILDX_FLAGS := --platform $(PLATFORMS) --push

define get_full_tag
$(if $(REGISTRY),$(REGISTRY)/)$(if $(ORG),$(ORG)/)$(if $(REPO),$(REPO)/)$(1):$(TAG)
endef

build_images:
	@for dir in ./services/backend/* ./services/frontend/*; do \
		if [ -d "$$dir" ] && [ -f "$$dir/Dockerfile" ]; then \
			SERVICE=$$(basename $$dir); \
			FULL_TAG=$(call get_full_tag,$$SERVICE); \
			echo "Building Docker image $$FULL_TAG"; \
			docker build -t $$FULL_TAG --build-context core=./core $$dir; \
		else \
			if [ -d "$$dir" ]; then \
				echo "Skipping $$dir, no Dockerfile found."; \
			fi \
		fi \
	done

build_and_push_images:
	@if [ -z "$(REGISTRY)" ] || [ -z "$(ORG)" ]; then \
		echo "Error: REGISTRY and ORG must be set to push images."; \
		exit 1; \
	fi
	docker buildx create --use
	@for dir in ./services/backend/* ./services/frontend/*; do \
		if [ -d "$$dir" ] && [ -f "$$dir/Dockerfile" ]; then \
			SERVICE=$$(basename $$dir); \
			FULL_TAG=$(call get_full_tag,$$SERVICE); \
			echo "Pushing Docker image $$FULL_TAG"; \
			if [ "$(GITHUB_WORKFLOW)" != "local" ]; then \
				BUILDX_CACHE_FLAGS="--cache-from type=gha,scope=$$SERVICE --cache-to type=gha,mode=max,scope=$$SERVICE"; \
			else \
				BUILDX_CACHE_FLAGS=""; \
			fi; \
			docker buildx build --build-context core=./core $(BUILDX_FLAGS) $$BUILDX_FLAGS_EXTRA -t $$FULL_TAG $$dir; \
		fi \
	done

create-tag:
	@if [ -z "$(VERSION)" ]; then \
		echo "VERSION is not set. Usage: make create-tag VERSION=x.y.z"; \
		exit 1; \
	fi
	$(eval TAURI_VERSION := $(patsubst v%,%,$(VERSION)))
	@jq '.package.version = "$(TAURI_VERSION)"' ./tauri/src-tauri/tauri.conf.json > temp.json && mv temp.json ./tauri/src-tauri/tauri.conf.json
	@git add ./tauri/src-tauri/tauri.conf.json
	@git commit -m "Update version to $(VERSION)"
	@git tag -a "$(VERSION)" -m "Release $(VERSION)"
	@echo "Tagged version $(VERSION)"

init-docs:
	docker run --rm --workdir=/docs -v $${PWD}/docs:/docs node:18-buster yarn install

# Ensure docs build without errors. Makes sure generated docs are in-sync with CLI.
validate-docs:
	docker run --rm --workdir=/docs -v $${PWD}/docs:/docs node:18-buster yarn build
	if [ -n "$$(git status --porcelain --untracked-files=no)" ]; then \
		git status --porcelain --untracked-files=no; \
		echo "Encountered dirty repo!"; \
		git diff; \
		exit 1 \
	;fi
