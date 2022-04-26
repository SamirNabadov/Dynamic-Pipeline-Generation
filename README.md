__Dynamic Pipeline Generation__
================================

Generation Dynamic Pipeline on Gitlab

![Screenshot](GitOpsImage.png)

Basic settings
------------
* GitLab CI Pipeline
* Helm Charts for deploy to Kubernetes
* Continuous Deployment using Helm
* Python scripts for generation dynamic pipelines
* Using the jib on the gradle to build and push images to gitlab registry

Dynamic Pipeline Generation Structure
------------
![Screenshot](dynamic_pipeline_generation.png)

Note
------------
You can add variables in Gitlab at the group level from Settings -> CICD -> Variables

* CI_GITLAB_USERNAME: cicd_user
* CI_GITLAB_PASSWORD: password
* CI_REGISTRY_USER: registry_user
* CI_REGISTRY_PASSWORD: password
* CI_PROJECT_TEMPLATE: devops/cicd-template-project




stages:
  - generate-child-pipeline
  - trigger-child-pipeline

stages:
  - test
  - build
  - deploy-dev
  - deploy-prod


__Requirements__
------------
* Gitlab
* Python
* Helm
* Kubernetes Environment (Dev & Prod)

__Author Information__
------------------

Samir Nabadov
