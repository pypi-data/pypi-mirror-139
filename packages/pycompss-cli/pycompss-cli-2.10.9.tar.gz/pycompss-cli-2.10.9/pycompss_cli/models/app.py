import os

class App(object):
    def __init__(self, name: str, 
                       env_id: str,
                       source_dir: str,
                       remote_dir: str = None) -> None:
        self.name = name
        self.env_id = env_id
        self.source_dir = source_dir
        self.remote_dir = remote_dir
        self.app_dir = os.path.expanduser('~') + f'/.COMPSsApps/{env_id}/{name}'

    @classmethod
    def fromdict(cls, dictionary: dict):
        name = dictionary['name']
        env_id = dictionary['env_id']
        source_dir = dictionary['source_dir']
        remote_dir = dictionary['remote_dir'] if 'remote_dir' in dictionary else None
        return cls(name, env_id, source_dir, remote_dir)