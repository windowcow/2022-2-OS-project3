import tabulate as tb
import pandas as pd


def get_file_contents(input_file_name):
    """ 파일의 이름을 받아서 각 줄을 list로 반환하는 함수 """

    f = open(input_file_name, 'r')
    file_contents = f.readlines()
    f.close()
    
    return file_contents

def get_NMWK(file_contents):
    return map(int, file_contents[0].split("  "))

def get_page_reference_string(file_contents):
    return list(map(int, file_contents[1].split(" ")))

def print_inputs(N, M, W, K, page_reference_string):
    print("N: " + str(N))
    print("M: " + str(M))
    print("W: " + str(W))
    print("K: " + str(K))
    
    print("page_reference_string: ", page_reference_string)
    return 0

def print_table(time, page_reference_string, memory_state, page_fault):
    table = [
        ["Time", *time],
        ["Ref. string", *page_reference_string], 
        ["Memory state", *memory_state],
        ["Page fault", *page_fault]
        ]
    print(tb.tabulate(table, tablefmt="fancy_grid"))

def get_index_of_victim_in_current_memory_state(current_memory_state, page_reference_string, time):
    
    pass

def get_result(M: int, page_reference_string: str):
    def make_empty_memory_state(M: int):
        return [-1 for _ in range(M)]
    
    
    current_memory_state = make_empty_memory_state(M)
    
    for time in range(len(page_reference_string)):
        current_requested_page_frame = page_reference_string[time]
        
        if current_requested_page_frame in current_memory_state: # page fault가 아닌 경우
            continue
        else: # page fault인 경우
            victim_page_frame_index = get_index_of_victim_in_current_memory_state(current_memory_state, page_reference_string, time)


git branch -M main
git remote add origin https://github.com/windowcow/2022-2-OS-project3.git
git push -u origin main









if __name__ == "__main__":
    file_contents = get_file_contents("input.txt")
    N, M, W, K = get_NMWK(file_contents)
    page_reference_string = get_page_reference_string(file_contents)
    # print_inputs(N, M, W, K, page_reference_string)
    
    
    
    
    time = [i for i in range(1, len(page_reference_string)+1)]
    memory_state = [0 for i in range(len(page_reference_string))]
    page_fault = [0 for i in range(len(page_reference_string))]
    print_table(time, page_reference_string, memory_state, page_fault)


