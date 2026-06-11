import json
import os
import logging
from typing import Union, Dict

# Subject to change
DEFAULT_DIR : str = os.path.join("examples")  #! Example folder

class JSONLoader:
    
    @staticmethod
    def _resolve_path(input_path: str) -> str:
        """
        Private helper
        Resolves absolute path / relative path vs just a file name (uses DEFAULT_DIR)
        """

        if os.path.isabs(input_path):
            return input_path
        
        #? os.sep ? See : https://docs.python.org/3/library/os.html#os.sep ('/' or '\\')
        if os.sep in input_path or '/' in input_path:
            return os.path.join(os.getcwd(), input_path) #? os.getcwd() Return a string representing the current working directory.

        else : 
            return os.path.join(DEFAULT_DIR, input_path)
    
    @staticmethod
    def load_json(file_path: str) -> Union[Dict, list] or None:
        """
        Loads data from a JSON file. 
        """

        resolved_file_path = JSONLoader._resolve_path(file_path)
        try: 
            with open(resolved_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError :
            logging.error("The file doen't exist!")
            return None

    @staticmethod
    def save_json(file_path: str, data) -> bool:
        """
        Well, it saves a JSON file into a specified path

        Returns : 
        True (Save sucessful)
        False (Failed)
        """
        
        # Check if the diectory doesn't exist, if it doesn't create it if permissions allows
        directory = os.path.dirname(os.path.abspath(file_path)) #! Get absolute path to check for existance of directory
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                return False

        try:
            # Use 'w' mode for writing/overwriting the file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"Successfully saved data to: {os.path.abspath(file_path)}")
            return True
        except Exception as e :
            logging.error(e)