TAG := $(or $(TAG),main)
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
			docker build -t $$FULL_TAG $$dir; \
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
			docker buildx build $(BUILDX_FLAGS) -t $$FULL_TAG $$dir; \
		fi \
	done