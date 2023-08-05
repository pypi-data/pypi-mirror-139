import docker
import docker.errors
import docker.client

from distutils.dir_util import copy_tree
from os import mkdir


from .. import manager
from . import errors
from . import status


class Container():

    def __init__(self, client, path: str, name: str, token: str):
        self.client = client
        self.ctn = None
        self.path = path
        self.name = name
        self.ctn_name = 'ddx-' + name
        self.docker_context = f'/tmp/dockerfiles/{self.ctn_name}'
        self.status = self.STATUS_EXITED
        self.img_name = f'{self.name}_img'
        self.token = token

    def dockerize(self):
        try:
            mkdir(self.docker_context)
        except FileExistsError:
            pass

        f = open(f'{self.docker_context}/Dockerfile', 'w')
        f.write("FROM python:latest\nCOPY ./app /app \nCOPY ./requirements.txt /requirements.txt \nRUN pip install -r /requirements.txt\nCMD python /app/main.py\n")
        f.close()

        copy_tree(self.path, self.docker_context)

        self.client.images.build(path=self.docker_context, tag=self.img_name)

        try:
            self.client.containers.get(self.ctn_name).remove(force=True)
        except docker.errors.NotFound:
            pass

        self.ctn = self.client.containers.create(
            image=self.img_name,
            name=self.ctn_name,
            environment=[f'BOT_TOKEN={self.token}'],
            network_mode='bridge',
            auto_remove=True)

    def start(self):
        try:
            self.ctn.start()
        except docker.errors.APIError as e:
            raise(e('Api Error'))
        except Exception as e:
            raise(e('Already Started'))
        self.status = self.STATUS_RUNNING

    def stop(self):
        self.ctn.stop()
        self.status = self.STATUS_EXITED

    async def is_running(self) -> bool:
        try:
            self.ctn = self.client.containers.get(self.ctn_name)
            if (self.ctn.status == status.STATUS_RUNNING):
                return True
            else:
                return False
        except docker.errors.NotFound as e:
            raise(manager.errors.ReferenceError(
                f'Impossible to access container : {e}'))

    def is_container_valid(self) -> bool:
        try:
            self.ctn = self.client.containers.get(self.ctn_name)
            return True
        except docker.errors.NotFound as e:
            raise (errors.ValidityError(
                f'Impossible to access container : {e}'))
