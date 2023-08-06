import logging
import os
from typing import List

import jmespath
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound

from detect_languages.languages import name_type_extensions


class DetectLanguages:
    def __init__(self, debug: bool = False, path: str = ".", language_types: List[str] = None, exclude_dirs: List[str] = None, exclude_dirs_recursively: bool = False) -> None:
        """
        The function takes in a path to a directory and analyzes the files in that directory.

        Args:
          debug (bool): If True, the logging level will be set to DEBUG. Otherwise, it will be set to None.
        Defaults to False
          path (str): The path to the directory to analyze. Defaults to .
          language_types (List[str]): A list of language types to include in the analysis.
          exclude_dirs (List[str]): A list of directories to exclude from the analysis.
          exclude_dirs_recursively (bool): If True, then exclude directories recursively. Defaults to False
        """
        if language_types is None:
            language_types = ["programming", "prose", "data", "markup"]
        if exclude_dirs is None:
            exclude_dirs = []
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG if debug else None)
        self.__language_types = []
        self.__language_types.extend(language_types)
        self.__exclude_dirs = [".git"]
        self.__exclude_dirs.extend(exclude_dirs)
        self.__exclude_dirs_recursively = exclude_dirs_recursively
        self.__analysis = {}
        self.__total_files_size = 0
        self.main_language = None
        self.all_languages = []
        self.__language_types_extensions = []
        self.__run_analysis(path)

    def __run_analysis(self, path: str) -> None:
        """
        Detects the language of the files in the given path and returns the main language and all the
        detected languages

        Args:
          path (str): The path to the directory that contains the files to be analyzed.
        """
        logging.debug("Detecting languages...")
        logging.debug(f"Language types: {self.__language_types}")
        self.__filter_language_types()
        self.__filter_exclude_dirs(path)
        self.__percentage_calculation()
        if len(self.__analysis.keys()) == 0:
            logging.debug("Not detected languages")
            return
        self.main_language = max(self.__analysis.items(), key=lambda a: self.__analysis[a[0]]["size"])[0]
        logging.debug(f"Detected main language: {self.main_language}")
        self.all_languages = dict(sorted(self.__analysis.items(), key=lambda kv: float(kv[1]["percentage"]), reverse=True))
        logging.debug(f"Detected languages: {list(self.all_languages.keys())}")

    def __filter_language_types(self) -> None:
        """
        * Filter the language types by the ones we want to use
        """
        for language_type in self.__language_types:
            extensions = jmespath.search(f"[?type=='{language_type}'].extensions[]", name_type_extensions())
            self.__language_types_extensions.extend(extensions)

    def __is_in_language_types(self, language: str) -> bool:
        """
        Given a language, return True if the language is in the language_types list

        Args:
          language (str): The language to check.

        Returns:
          The boolean value.
        """
        language_type = jmespath.search(f"[?name=='{language}'].type | [0]", name_type_extensions())
        return language_type in self.__language_types

    def __guess_file_language(self, file: str) -> str:
        """
        Guess the language of a file
        
        Args:
          file (str): The file to be analyzed.
        
        Returns:
          The language of the file.
        """
        try:
            with open(file, "r", encoding="utf-8") as reader:
                file_content = reader.read()
                try:
                    language = guess_lexer_for_filename(file, file_content, stripnl=False).__class__.name
                except ClassNotFound as ex:
                    logging.debug(ex)
                    return
                return language
        except UnicodeDecodeError:
            logging.debug(f"'{file}' is not a text file.")
            return

    def __filter_exclude_dirs(self, path: str) -> None:
        """
        Iterate through all files in the given path and check if the file is a valid file.
        
        Args:
          path (str): The path to the directory you want to search.
        """
        root, subdirs, files = next(os.walk(path))
        for filename in files:
            file = os.path.join(root, filename)
            _, file_extension = os.path.splitext(file)
            file_size = os.path.getsize(file)
            if file_size == 0:
                continue
            self.__check_file(file, file_extension, file_size)
        for subdir in subdirs:
            if subdir not in self.__exclude_dirs:
                subdir_path = os.path.join(root, subdir)
                if not self.__exclude_dirs_recursively:
                    self.__find_files(subdir_path)
                else:
                    self.__filter_exclude_dirs(subdir_path)

    def __find_files(self, subdir_path: str) -> None:
        """
        Find all files in the specified directory and subdirectories.
        
        Args:
          subdir_path (str): The path to the directory that contains the files to be checked.
        """
        for root, _, files in os.walk(subdir_path):
            for filename in files:
                file = os.path.join(root, filename)
                _, file_extension = os.path.splitext(file)
                file_size = os.path.getsize(file)
                if file_size == 0:
                    continue
                self.__check_file(file, file_extension, file_size)

    def __check_file(self, file: str, file_extension: str, file_size: int) -> None:
        """
        Check if the file extension is in the language types extensions. If not, guess the language type of
        the file. 
        If the language type is not in the language types, return. 
        If the language type is in the language types, add the file size to the total size of the language
        type.
        
        Args:
          file (str): The file to check.
          file_extension (str): The file extension of the file.
          file_size (int): The size of the file in bytes.
        """
        if not file_extension or file_extension in self.__language_types_extensions:
            language = self.__guess_file_language(file)
            logging.debug(f"file: '{file}', language: '{language}', size: {file_size}")
            if not language:
                return
            if language == "Text only":
                return
            if not self.__is_in_language_types(language):
                logging.debug(f"'{language}' language type is not in language types {self.__language_types}")
                return
            self.__add_file_size_and_total_files_size(language, file_size)

    def __add_file_size_and_total_files_size(self, language: str, size: int) -> None:
        """
        Add the size of the file to the size of the language in the analysis and add the size of the file to
        the total size of all files
        
        Args:
          language (str): The language of the file.
          size (int): The size of the file in bytes.
        """
        if language in self.__analysis:
            self.__analysis[language]["size"] += size
        else:
            self.__analysis[language] = {"size": size}
        self.__total_files_size += size

    def __percentage_calculation(self) -> None:
        """
        Calculate the percentage of each language in the directory
        """
        for language in self.__analysis.keys():
            self.__analysis[language]["percentage"] = round(((self.__analysis[language]["size"] / self.__total_files_size) * 100), 2)
