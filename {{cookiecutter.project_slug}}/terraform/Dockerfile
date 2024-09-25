FROM hashicorp/terraform:latest

# Install any other dependencies if needed
# For example:
# RUN apk add --no-cache python3 py3-pip

# Copy entrypoint script
COPY terraform/docker_entrypoint.sh /terraform/docker_entrypoint.sh

# Ensure the entrypoint script is executable
RUN chmod +x /terraform/docker_entrypoint.sh
