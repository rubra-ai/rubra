.PHONY: create-tag init-docs validate-docs

# Default values for variables
TAG ?= main
GITHUB_WORKFLOW ?= local
REGISTRY ?= index.docker.io
PLATFORMS := linux/amd64,linux/arm64
BUILDX_FLAGS := --platform $(PLATFORMS) --push

create-tag:
	@if [ -z "$(VERSION)" ]; then \
		echo "VERSION is not set. Usage: make create-tag VERSION=x.y.z"; \
		exit 1; \
	fi
	@git tag -a "$(VERSION)" -m "Release $(VERSION)"
	@echo "Tagged version $(VERSION)"

init-docs:
	@echo "Initializing documentation..."
	# Add commands for initializing docs here if any setup is needed

validate-docs:
	@echo "Validating documentation..."
	# Add commands for building or checking docs here
	# This could be local commands if you're using a static site generator like Jekyll or Hugo