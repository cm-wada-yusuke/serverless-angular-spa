SHELL = /usr/bin/env bash -xeuo pipefail

include Makevars

GIT_COMMIT := $(shell git log -n 1 --format=%h)
BASE := src/functions/handlers
TEMPLATES := $(sort $(notdir $(wildcard templates/labmda_*.yaml)))
TARGETS := $(patsubst lambda_%.yaml, %, $(TEMPLATES))
DEPLOY_TASK := $(addprefix deploy-, $(TARGETS))
SECRETS := $(addprefix guard-, $(SECRET_PARAMETERS))


all: guard-env clean format test-unit test-integ lambda
	@echo $(DEPLOY_TASK)

display:
	@echo $(TARGETS)
	@echo $(DEPLOY_TASK)

install:
	@pip install -r requirements.txt -t


format:
	-yapf -ir src/
	-yapf -ir test/

test-unit:
	@python -m pytest test/

clean:
	-rm -rf deploy/
	-rm packaged-*.yaml
	-rm lambda*.yaml
	-rm infra_*.yaml

push-params: guard-env $(SSM_LAMBDA_PARAMETERS_DIR)/*-$(SSM_LAMBDA_PARAMETERS_FILE) $(SECRETS)
	@ jq -c --arg env $$env 'def addenv(f): f as $$value | "/" + $$env + "/lambda/" + $$value; \
	 .[] |  {Name:addenv(.Name), Value:.Value, Type:"String"} | tostring' $(SSM_LAMBDA_PARAMETERS_DIR)/$$env-$(SSM_LAMBDA_PARAMETERS_FILE) |\
      awk -v env=$$env '{ print "aws ssm put-parameter --overwrite --cli-input-json " $$1}' |\
      sh
	@ aws ssm get-parameters-by-path --path /$${env}/lambda

generate-cfn-parameters: guard-env
	@python environments/template_parameters_generator.py $${env}

lambda: guard-env $(DEPLOY_TASK)
	@echo $(TARGETS)
	@echo $(UPLOAD_TASK)
	@echo $(DEPLOY_TASK)

lambda-%: templates/lambda_%.yaml guard-env generate-cfn-parameters
	@ if [ "${*}" = "" ]; then \
		echo "Target is not set"; \
		exit 1; \
	elif [ ! -d "$(BASE)/${*}" ]; then \
		echo "Target directory $(BASE)/$* does not exists."; \
		exit 1; \
	else \
		cat templates/lambda_${*}.yaml templates/$${env}_lambda_common_parameters.yaml > template_${*}.yaml && \
		stack_name_hyphen=$(subst _,-,$(*)) && \
		aws cloudformation package \
			--template-file template_${*}.yaml \
			--s3-bucket $${env}-$(S3_BUCKET) \
			--output-template-file packaged-${*}.yaml && \
		aws cloudformation deploy \
			--template-file packaged-${*}.yaml \
			--stack-name $${env}-$${stack_name_hyphen}-lambda  \
			--capabilities  CAPABILITY_NAMED_IAM CAPABILITY_IAM \
			--no-fail-on-empty-changeset \
			--parameter-overrides \
				CommitId=$(GIT_COMMIT) ; \
	fi

infra-%: templates/infra_%.yaml guard-env generate-cfn-parameters
	@ if [ "${*}" = "" ]; then \
		echo "Target is not set"; \
		exit 1; \
	else \
		cat templates/infra_${*}.yaml templates/$${env}_lambda_common_parameters.yaml > infra_${*}.yaml && \
		stack_name_hyphen=$(subst _,-,$(*)) && \
		aws cloudformation deploy \
			--template-file infra_${*}.yaml \
			--s3-bucket $${env}-$(S3_BUCKET) \
			--stack-name $${env}-$${stack_name_hyphen}-resource  \
			--capabilities CAPABILITY_NAMED_IAM \
			--no-fail-on-empty-changeset ; \
	fi

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

.PHONY: \
	install \
	test-unit \
	clean \
	format
