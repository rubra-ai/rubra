TAG := $(or $(TAG),main)
REGISTRY := $(or $(REGISTRY),index.docker.io)

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

push_images: build_images
	@if [ -z "$(REGISTRY)" ] || [ -z "$(ORG)" ]; then \
		echo "Error: REGISTRY and ORG must be set to push images."; \
		exit 1; \
	fi
	@for dir in ./services/backend/* ./services/frontend/*; do \
		if [ -d "$$dir" ] && [ -f "$$dir/Dockerfile" ]; then \
			SERVICE=$$(basename $$dir); \
			FULL_TAG=$(call get_full_tag,$$SERVICE); \
			echo "Pushing Docker image $$FULL_TAG"; \
			docker push $$FULL_TAG; \
		fi \
	done