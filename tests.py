# tests.py
from functions.get_file_content import get_file_content

def test():
    print("=====Content of main.py=====")
    print(get_file_content("calculator", "main.py"))
    print("==========\n")

    print("=====Content of pkg/calculator.py=====")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("==========\n")

    print("=====Content of /bin/cat=====")
    print(get_file_content("calculator", "/bin/cat"))
    print("==========\n")

    print("=====Content of pkg/does_not_exist.py=====")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print("==========\n")



if __name__ == "__main__":
    test()