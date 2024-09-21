from typing import *

import json
import yaml
from pathlib import Path

import copy

class Config(dict):


    def __init__(self, 
                 config_path=None,
                 update_live:bool = False,
                 *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self._initialized = False

        self.config_path = config_path
        
        self._live_update = update_live
        self._private_vars = set() 
        self._initialized = True

        if config_path is not None:
            self.load(config_path)

    #def __getattr__(self, name):
#
    #    return self.__getitem__(name)
        
    #def __setattr__(self, name, value):
    #    if self._initialized:
    #        self.__setitem__(name, value)
    #    else:
    #        super().__setattr__(name, value)

    
    def __setitem__(self, key, value):

        super().__setitem__(key, value)

        #if self._live_update and self.config_path is not None:
        #    self.save()

    def __getitem__(self, key):
        if key not in list(self.keys()):
            print(f"Configuration parameter {key} does not exist!")
            return None
        else:
            return super().__getitem__(key)

    def set_private_key(self, key, value):
        self._private_vars.add(key)
        self.__setitem__(key, value)

    def save(self, path:Union[Path, str] = None):

        if path is None:
            if self.config_path is not None:
                path = self.config_path
            else:
                print('No path specified for saving config!')
                return

        file_type = str(Path(path).suffix)

        save_dir = copy.deepcopy(self)

        for k in self._private_vars:
            del save_dir[k]

        if file_type == '.json':
            try:
                with open(path, 'w') as f:
                    json.dump(save_dir, f, indent=4)
            except Exception as e:
                print(f'Error saving JSON config: {e}')
        elif file_type == '.yaml':
            try:
                with open(path, 'w') as f:
                    yaml.dump(save_dir, f, default_flow_style=False)
            except Exception as e:
                print(f'Error saving YAML config: {e}')
        else:
            print(f'Invalid file type for saving config!')


    def load(self, path:Union[Path,str] ):
        config_path = Path(path)
        file_type = str(config_path.suffix)

        if file_type == '.json':
            try:
                with open(config_path, 'r') as f:
                    self.update(json.load(f))
            except json.JSONDecodeError as e:
                print(f'Invalid JSON format in {config_path}:\n{e}')
        elif file_type == '.yaml':
            try:
                with open(config_path, 'r') as f:
                    self.update(yaml.safe_load(f))
            except yaml.YAMLError as e:
                print(f'Invalid YAML format in {config_path}:\n{e}')
        else:
            print(f'Invalid file type ({file_type}) in {config_path}!')

    def __str__(self):
        return json.dumps(self, indent=4)




            


                
        