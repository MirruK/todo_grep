import sys
from functools import reduce

TOKENS: dict = {"TODO:" : 0}
EOF = '\000'

def fetch_files() -> list[str]:
    if(len(sys.argv) < 2):
        raise ValueError("Usage: TOCO file(s)\nInvalid number of arguments")
    input_files = []
    i = 1
    while(i < len(sys.argv)):
        input_files.append(sys.argv[i])
        i += 1
    assert len(input_files) > 0, "Something dun goofed"
    return input_files

def readchar(f, buf: list[str]) -> str:
    return buf.pop() if len(buf) > 0 else f.read(1)

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

def main():
    """
    Flow of program:
        1. Fetch filenames from cmd arguments
        2. Grep files for valid TODO-tokens
        3. Collect said tokens
        4. Generate output from tokens
    """
    todo_files = fetch_files()
    todo_tokens = map(grep_todo, todo_files)
    todo_tokens = reduce(lambda x,y: x + y, todo_tokens)
    todo_tokens = filter(lambda x: x != '', todo_tokens)
    print(todo_files)
    print(list(todo_tokens))


main()
