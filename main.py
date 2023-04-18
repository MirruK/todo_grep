import sys
import os
from functools import reduce

TOKENS: dict = {"TODO:" : 0}
IGNORED: list[str] = [".git"]

def recursive_get_files(dir: str, file_list: list[str]) -> None:
    for ignored in IGNORED:
        if(ignored in dir):
            return
    for file in os.listdir(dir):
        file = os.path.join(dir, file)
        if os.path.isdir(file):
            recursive_get_files(file, file_list)
        elif (os.path.isfile(file)): file_list.append(file)

def fetch_files() -> list[str]:
    if(len(sys.argv) < 2):
        raise ValueError("Brotha', you have to give me some files")
    input_files = []
    i = 1
    while(i < len(sys.argv)):
        if(os.path.isdir(sys.argv[i])): 
            recursive_get_files(sys.argv[i], input_files) 
        elif(os.path.isfile(sys.argv[i])): input_files.append(sys.argv[i])
        else: print(f"Argument #{i}: Invalid file/directory supplied")
        i += 1
    assert len(input_files) > 0, "Something dun goofed"
    return input_files

def readchar(f, buf: list[str]) -> str:
    if(len(buf) > 0):
        return buf.pop()
    try:
        c = f.read(1)
    except:
        c = ''
    return c

def grep_todo(file_name: str) -> list[str]:
    with open(file_name, 'r') as file:
        c = 0
        ind = 0
        found = False
        buffer = []
        todos: list[str] = []
        file_buffer = []
        token = "TODO:"
        while(c != ''):
            if(found):
                c = readchar(file, file_buffer)
                # If TODO-token is found read until newline
                while(c != '\n'):
                    if(c == ''): break
                    buffer.append(c)
                    c = readchar(file, file_buffer)
                # Append the line as a string to the list of found todos
                todos.append("".join(buffer)) 
                buffer.clear()
                found = False
            else:
                c = readchar(file, file_buffer)
            # If we find start of TODO-token:
            while(c == token[ind]):
                buffer.append(c)
                if(len(buffer) >= len(token)):
                    found = True
                    break
                c = readchar(file, file_buffer)
                ind += 1
            ind = 0
            # Empty the buffer into the file_buffer
            # to cover the case of a partial token being found
            while(len(buffer)):
                file_buffer.append(buffer.pop())
    return todos

def compile_todos(todos: list[str]):
    pass

def main():
    """
    Flow of program:
        1. Fetch filenames from cmd arguments
        2. Grep files for valid TODO-tokens
        3. Collect said tokens
        4. Generate output from tokens
    """
    # Step 1
    todo_files = fetch_files()
    # Step 2
    todo_tokens = map(grep_todo, todo_files)
    # Step 3
    todo_tokens = reduce(lambda x,y: x + y, todo_tokens)
    todo_tokens = filter(lambda x: x != '', todo_tokens)
    # Step 4
    # compile_todos(todo_tokens)
    print("Found Files:")
    print(todo_files)
    print("TODOs found:")
    for token in list(todo_tokens):
        print(token)


main()
