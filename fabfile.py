from fabric.api import *
from fabric.contrib.files import *
from fabric.colors import *

env.colorize_errors = 'True'

def deploy():
    """Deploy Container """
    print(green("-----> Running Docker Compose..."))
    local('/usr/local/bin/docker-compose build')
    local('/usr/local/bin/docker-compose up -d')
    local('/usr/local/bin/docker-compose ps')

def stop():
    local('/usr/local/bin/docker-compose down')
