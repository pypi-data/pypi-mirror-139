import docker

from os import mkdir

import ddxl


class ContainerManager():
    def __init__(self) -> None:
        self.client = docker.from_env()
        self.bot_containers = {}
        try:
            mkdir(f'/tmp/dockerfiles')
        except FileExistsError:
            pass

    def add(self, context: str, name: str, token: str) -> None:
        if (not self.bot_exists(name)):
            self.bot_containers[name] = ddxl.container.Container(
                self.client, context, name, token)
            self.bot_containers[name].dockerize()
        else:
            raise(ReferenceError(
                f"Container with name '{name}' already exists"))

    async def start(self, name: str) -> None:
        try:
            await self.get_bot_by_name(name).start()
        except ddxl.manager.ContainerNameError as e:
            raise(e('Impossible to start bot '))

    def stop(self, name: str) -> None:
        if (self.bot_exists(name)):
            if (self.bot_containers[name].status == ddxl.container.status.STATUS_RUNNING):
                self.bot_containers[name].stop()
            else:
                raise(ddxl.manager.ContainerNameError("bot is not running"))
        else:
            raise(KeyError(f'No container with name {name}'))

    def bot_exists(self, name: str) -> bool:
        return True if name in self.bot_containers.keys() else False

    def get_online_bots(self) -> list:
        return [bot.name for bot in self.bot_containers.values() if bot.status == ddxl.container.STATUS_RUNNING]

    def get_bot_by_name(self, name: str) -> ddxl.container.Container:
        if (self.bot_exists(name) and self.bot_containers[name].is_container_valid()):
            return self.bot_containers[name]
        raise(ddxl.manager.ContainerNameError(
            f'No container with name \'{name}\''))
