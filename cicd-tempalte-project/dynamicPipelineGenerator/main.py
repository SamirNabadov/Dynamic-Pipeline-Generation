import os
from PipelineWriter import PipelineWriter

wordCheck = "include"
moduleCheck = "common"
pipelineFilename = "child-pipeline-gitlab-ci.yml"
gradleFilename = "settings.gradle"

def getModules():
  with open(gradleFilename, 'r') as file:
    lines = file.readlines()
    modules = []
    for line in lines:
      if wordCheck in line:
        if moduleCheck in line:
          continue
        else:
          line = line.split(',')
          line = [i.strip() for i in line][0].split("'")[1]
          modules.append(line)

  return modules

def generator():
  with open(pipelineFilename, 'w') as file:
    file.write(PipelineWriter.parent_job_template())
    for module in getModules():
      file.write(PipelineWriter.child_pipeline_job_template(module))


if __name__ == "__main__":
    generator()
