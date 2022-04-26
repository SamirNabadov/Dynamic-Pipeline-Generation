class PipelineWriter:

    @staticmethod
    def parent_job_template():
        parent_job_template = f"""

stages:
  - test
  - build
  - deploy-dev
  - deploy-prod

.test:
  image: openjdk:8-jdk-alpine
  before_script:
    - export GRADLE_USER_HOME=`pwd`/.gradle
  script:
    - ./gradlew :$MODULE:bootJar -x test --no-daemon

.build:
  image: openjdk:8-jdk-alpine
  before_script:
    - export GRADLE_USER_HOME=`pwd`/.gradle
  script:
    - ./gradlew :$MODULE:jib -Djib.to.tags=$CI_PIPELINE_ID -Djib.to.auth.username=$CI_REGISTRY_USER -Djib.to.auth.password=$CI_REGISTRY_PASSWORD --no-daemon
  
.deploy:
  image: dtzar/helm-kubectl
  script:
    - sed -i "s/tag:.*/tag:\ $CI_PIPELINE_ID/" ./deploy/$MODULE/helm-charts/$CI_COMMIT_BRANCH.yaml
    - helm upgrade demo-$MODULE ./deploy/$MODULE/helm-charts --install --values=./deploy/$MODULE/helm-charts/$CI_COMMIT_BRANCH.yaml

.before_script:
  before_script:
    - mkdir -p ~/.kube; echo "$CI_KUBE_CONFIG" > ~/.kube/config; chmod 400 ~/.kube/config

  """

        return parent_job_template

    @staticmethod
    def child_pipeline_job_template(module):
        child_pipeline_job_template = f"""

.{module}-change:
  variables:
    MODULE: "{module}"
  only:
    refs:
      - "develop"
      - "master"
    changes:
      - "{module}/**/*"
      - "common/**/*"
      - "deploy/{module}/**/*"

.deploy-dev-{module}-change:
  variables:
    MODULE: "{module}"
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
      changes:
        - "{module}/**/*"
        - "common/**/*"
        - "deploy/{module}/**/*"

.deploy-prod-{module}-change:
  variables:
    MODULE: "{module}"
  rules:
    - if: '$CI_COMMIT_BRANCH == "master"'
      changes:
        - "{module}/**/*"
        - "common/**/*"
        - "deploy/{module}/**/*"

test-{module}:
  stage: test
  extends:
     - .{module}-change
     - .test

build-{module}:
  stage: build
  extends:
     - .{module}-change
     - .build

deploy-dev-{module}:
  stage: deploy-dev
  extends:
    - .deploy-dev-{module}-change
    - .before_script
    - .deploy
  variables:
    CI_HOSTNAME: "dev-{module}.local.az"
    CI_KUBE_CONFIG: $DEV_KUBERNETES_CLUSTER_KUBE_CONFIG
  environment:
    name: dev-{module}-environment
    url: http://$CI_HOSTNAME/
  resource_group: development

deploy-prod-{module}:
  stage: deploy-prod
  extends:
    - .deploy-prod-{module}-change
    - .before_script
    - .deploy
  variables:
    CI_HOSTNAME: "{module}.local.az"
    CI_KUBE_CONFIG: $PROD_KUBERNETES_CLUSTER_KUBE_CONFIG
  environment:
    name: {module}-environment
    url: http://$CI_HOSTNAME/
  resource_group: production

"""

        return child_pipeline_job_template
