import pip
from subprocess import call

# read requirements.txt file, create list of package names
requirements = open("requirements.txt", "r")
for package in requirements:
    print(package, call("pip install " + package, shell=True))

#
# import pkg_resources
# from subprocess import call
#
# packages = [dist.project_name for dist in pkg_resources.working_set]
# call("pip install --upgrade " + ' '.join(packages), shell=True)
