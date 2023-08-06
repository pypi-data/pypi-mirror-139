# -*- coding: utf-8 -*-
# Package for easy working with files.
# File with class for files to professional working with files.
import os

class File:
    def __init__(self, path: str, encoding: str = "utf-8", new: bool = False) -> None:
        self.__path = path
        self.__encoding = encoding
        if new:
            self.write("", "w")
        elif not os.path.isfile(path):
            raise FileNotFoundError("File doesn't exist!")


    def write(self, content: str, mod: str) -> int:
        with open(self.__path, mod, encoding = self.__encoding) as file:
            return file.write(content)


    def add(self, content: str) -> int:
        with open(self.__path, "a", encoding = self.__encoding) as file:
            return file.write(content)


    def rewrite(self, content: str) -> int:
        with open(self.__path, "w", encoding = self.__encoding) as file:
            return file.write(content)


    def read(self) -> str:
        with open(self.__path, "r", encoding = self.__encoding) as file:
            return file.read()

        
    def readLine(self, number_of_line: int) -> str:
        return self.split("\n")[number_of_line]


    def rename(self, new_name: str) -> None:
        os.rename(self.__path, new_name)
        len_ = len(self.__path.split('/'))
        if len_ == 1:
            self.__path = new_name
        else:
            self.__path = self.__path.rsplit('/', maxsplit = 1)[0] + '/' + new_name


    def getName(self) -> str:
        return self.__path.rsplit("/")[0]

    def getExtension(self) -> str:
        return self.__path.rsplit(".")[0]

    def getPath(self) -> str:
        return self.__path

    def getEncoding(self) -> str:
        return self.__encoding

    def getSize(self) -> int:
        return os.path.getsize(self.__path)


    def remove(self) -> None:
        os.remove(self.__path)
        del self


    def split(self, key: str) -> list:
        content = self.read()
        return content.split(key)

    
    def rsplit(self, key: str) -> list:
        content = self.read()
        return content.rsplit(key)


    def __contains__(self, key) -> bool:
        content = self.read()
        return key in content


    def __eq__(self, __o) -> bool:
        if not isinstance(__o, File): raise TypeError("Can compare only File objects.")
        with open(self.__path, "r", encoding = self.__encoding) as file_1, open(__o.getPath(), "r", encoding = __o.getEncoding()) as file_2:
            file_1_content = file_1.read()
            file_2_content = file_2.read()
            return file_1_content == file_2_content

    
    def __ne__(self, __o: object) -> bool:
        if not isinstance(__o, File): raise TypeError("Can compare only File objects.")
        with open(self.__path, "r", encoding = self.__encoding) as file_1, open(__o.getPath(), "r", encoding = __o.getEncoding()) as file_2:
            file_1_content = file_1.read()
            file_2_content = file_2.read()
            return file_1_content != file_2_content


    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, File): raise TypeError("Can compare only File objects.")
        size_1 = self.getSize()
        size_2 = __o.getSize()
        return size_1 < size_2


    def __gt__(self, __o: object) -> bool:
        if not isinstance(__o, File): raise TypeError("Can compare only File objects.")
        size_1 = self.getSize()
        size_2 = __o.getSize()
        return size_1 > size_2


    def __le__(self, __o: object) -> bool:
        if not isinstance(__o, File): raise TypeError("Can compare only File objects.")
        size_1 = self.getSize()
        size_2 = __o.getSize()
        return size_1 <= size_2


    def __ge__(self, __o: object) -> bool:
        if not isinstance(__o, File): raise TypeError("Can compare only File objects.")
        size_1 = self.getSize()
        size_2 = __o.getSize()
        return size_1 >= size_2

if __name__ == '__main__':
    raise Exception("Can't run as main program.")