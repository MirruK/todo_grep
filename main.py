import sys
import os
from functools import reduce
from dataclasses import dataclass

IGNORED: list[str] = [".git"]

@dataclass
class TodoData():
    text: str = ""
    priority: int = 1
    file_of_origin: str = ""
    line_number: int = 0

    # TODO: implement
    # def __repr__(self):
    #     pass


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

def parse_priority(todo_obj: TodoData, file, file_buffer: list[str]) -> int:
    # TODO: implement parsing priority for a todo. Eg. TODO(2) has priority 2
    return 0

def parse_todo(todo_obj: TodoData, line_num: int, file, buffer: list[str], file_buffer: list[str]) -> int:
    token = "TODO"
    text = ""
    ind = 0
    todo_obj.line_number = line_num
    c = 'T'
    while(c == token[ind]):
        if(ind == len(token)-1):
            if(parse_priority(todo_obj, file, file_buffer) == 1):
                return 1
            c = readchar(file, file_buffer)
            while(c != '\n'):
                if(c == ''):
                    return 2
                text += c
                c = readchar(file, file_buffer)
            todo_obj.text = text
            return 0
        c = readchar(file, file_buffer)
        ind += 1
    while(len(buffer)):
        file_buffer.append(buffer.pop())
    return 3


def grep_todo(file_name: str) -> list[TodoData]:
    with open(file_name, 'r') as file:
        """
            Step 1. Find start of possible token
            Step 2. Parse token
                If full token -> consume input and parse additional tokens
                    If newline break from process and start from step 1. after newline
                Else if incomplete token -> push consumed chars onto buffer and goto step 1
        """
        c = 0
        line_num = 1
        buffer: list[str] = []
        todos: list[TodoData] = []
        file_buffer: list[str] = []
        todo_obj = TodoData(file_of_origin=file_name)
        
        while(c != ''):
            c = readchar(file, file_buffer)
            while(c != 'T'):
                if(c == ''): return todos
                c = readchar(file, buffer)
                if(c == ''): return todos
                if(c == '\n'):
                    line_num += 1
            result = parse_todo(todo_obj, line_num, file, buffer, file_buffer)
            match result:
                case 0:
                    # Indicates successful parsing of token
                    todos.append(todo_obj)
                    todo_obj = TodoData()
                case 1:
                    # Indicates EOF was found with incomplete token
                    return todos
                case 2:
                    # Indicates EOF was found with complete token
                    todos.append(todo_obj)
                    return todos
                case 3:
                    # indicates failed parsing
                    todo_obj = TodoData(file_of_origin=file_name)
    return todos


def compile_todos(todos: list[TodoData]):
    # TODO: Implement compile_todos function
    # TODO: Allow writing to file as well as writing to stdout
    for todo in todos:
        print(todo)


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
    #todo_tokens = filter(lambda x: x != '', todo_tokens)
    # Step 4
    compile_todos(todo_tokens)


main()
