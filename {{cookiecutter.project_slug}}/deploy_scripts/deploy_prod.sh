#!/usr/bin/bash

$(dirname "$0")/deploy_new_image.sh && \
\
$(dirname "$0")/execute_migrations_task_prod.sh && \
$(dirname "$0")/execute_collectstatic_task_prod.sh && \
\
$(dirname "$0")/force_new_deploy_prod.sh
