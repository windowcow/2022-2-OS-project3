import tabulate as tb
import pandas as pd
from prettytable import PrettyTable


EMPTY = '-'

def get_file_contents(input_file_name):
    """ 파일의 이름을 받아서 각 줄을 list로 반환하는 함수 """

    f = open(input_file_name, 'r')
    file_contents = f.readlines()
    f.close()
    
    return file_contents

def get_NMWK(file_contents):
    return map(int, file_contents[0].split("  "))

def get_page_reference_string(file_contents):
    return file_contents[1].replace(" ", "")

def print_inputs(N, M, W, K, page_reference_string):
    print("N: " + str(N))
    print("M: " + str(M))
    print("W: " + str(W))
    print("K: " + str(K))
    
    print("page_reference_string: ", page_reference_string)
    return 0

def transpose_2D_list(list_2D):
    return list(map(list, zip(*list_2D)))

def print_table(time, page_reference_string, memory_state, page_fault):
    # table = [["Time", *time],
    #         ["Ref. string", *page_reference_string], 
    #         ["Memory state", *memory_state],
    #         ["Page fault", *page_fault]]
    
    # print(tb.tabulate(table, tablefmt="fancy_grid"))
    myTable = PrettyTable()
    myTable.field_names = ["Time", *time]
    myTable.add_row(["Ref. string", *page_reference_string])
    transposed_list = transpose_2D_list(memory_state)
    memory_state_number = len(transposed_list)
    for i in range(memory_state_number):
        myTable.add_row(["Memory state " + str(i), *transposed_list[i]])
    myTable.add_row(["Page fault", *page_fault])
    print(myTable)



def get_index_of_victim_in_current_memory_state_LRU(current_memory_state, page_reference_string, time):
    # 참고로 여기의 current_memory_state에는 EMPTY가 없다.
    def find_last_index(string, ch):
        last_index = -1
        while True:
            index = string.find(ch, last_index + 1)
            if index == -1:
                return last_index
            last_index = index
    latest_reference_time = [find_last_index(page_reference_string[:time], current_memory_state[i]) for i in range(len(current_memory_state))]
    # latest_reference_time = [page_reference_string.find(current_memory_state[i], time + 1) for i in range(len(current_memory_state))]
    result_index = latest_reference_time.index(min(latest_reference_time))
    # if -1 not in latest_reference_time:
    #     result_index = latest_reference_time.index(max(latest_reference_time))
    # else:
    #     result_index = latest_reference_time.index(-1)
    return result_index

def get_index_of_victim_in_current_memory_state_LFU(current_memory_state, page_reference_string, time):
    # 참고로 여기의 current_memory_state에는 EMPTY가 없다.
    #reference time에는 규칙이 들어감 이게 가장 크거나 작은 인덱스가 victim이 됨
    def find_last_index(string, ch):
        last_index = -1
        while True:
            index = string.find(ch, last_index + 1)
            if index == -1:
                return last_index
            last_index = index
    reference_count = [(i, page_reference_string[:time].count(current_memory_state[i])) for i in range(len(current_memory_state))]
    min_count = min(reference_count, key=lambda x: x[1])
    candidate = [i for i in reference_count if i[1] == min_count[1]]
    last_occur = [(i[0], find_last_index(page_reference_string[:time], current_memory_state[i[0]]))for i in candidate] #i는 (index, count)
    result = min(last_occur, key=lambda x: x[1])
    
    print(result)
    return result[0]

def get_index_of_victim_in_current_memory_state_MIN(current_memory_state, page_reference_string, time):
    # 참고로 여기의 current_memory_state에는 EMPTY가 없다.
    reference_time = [page_reference_string.find(current_memory_state[i], time + 1) for i in range(len(current_memory_state))]
    result_index = reference_time.index(max(reference_time))
    if -1 not in reference_time:
        result_index = reference_time.index(max(reference_time))
    else:
        result_index = reference_time.index(-1)
    return result_index

def get_result_MIN(M: int, page_reference_string: str):
    def get_index_of_victim_in_current_memory_state_MIN(current_memory_state, page_reference_string, time):
        # 참고로 여기의 current_memory_state에는 EMPTY가 없다.
        reference_time = [page_reference_string.find(current_memory_state[i], time + 1) for i in range(len(current_memory_state))]
        result_index = reference_time.index(max(reference_time))
        if -1 not in reference_time:
            result_index = reference_time.index(max(reference_time))
        else:
            result_index = reference_time.index(-1)
        return result_index
    def make_empty_memory_state(M: int):
        return [EMPTY for _ in range(M)]
    
    
    current_memory_state = make_empty_memory_state(M)
    
    for time in range(len(page_reference_string)):
        current_requested_page_frame = page_reference_string[time]
        print(time, ":", current_memory_state)
        
        if current_requested_page_frame in current_memory_state: # page fault가 아닌 경우
            pass
        else: # page fault인 경우
            page_fault[time] = "F"
            if EMPTY in current_memory_state:
                current_memory_state[current_memory_state.index(EMPTY)] = current_requested_page_frame
            else:
                victim_page_frame_index = get_index_of_victim_in_current_memory_state_MIN(current_memory_state, page_reference_string, time)
                current_memory_state[victim_page_frame_index] = current_requested_page_frame
                print("victim_page_frame_index: ", victim_page_frame_index)
        memory_state.append(current_memory_state.copy())

def get_result_LRU(M: int, page_reference_string: str):
    def make_empty_memory_state(M: int):
        return [EMPTY for _ in range(M)]
    
    
    current_memory_state = make_empty_memory_state(M)
    
    for time in range(len(page_reference_string)):
        current_requested_page_frame = page_reference_string[time]
        print(time, ":", current_memory_state)
        
        if current_requested_page_frame in current_memory_state: # page fault가 아닌 경우
            pass
        else: # page fault인 경우
            page_fault[time] = "F"
            if EMPTY in current_memory_state:
                current_memory_state[current_memory_state.index(EMPTY)] = current_requested_page_frame
            else:
                victim_page_frame_index = get_index_of_victim_in_current_memory_state_LRU(current_memory_state, page_reference_string, time)
                current_memory_state[victim_page_frame_index] = current_requested_page_frame
                print("victim_page_frame_index: ", victim_page_frame_index)
        memory_state.append(current_memory_state.copy())

def get_result_LFU(M: int, page_reference_string: str):
    def make_empty_memory_state(M: int):
        return [EMPTY for _ in range(M)]
    
    
    current_memory_state = make_empty_memory_state(M)
    
    for time in range(len(page_reference_string)):
        current_requested_page_frame = page_reference_string[time]
        print(time, ":", current_memory_state)
        
        if current_requested_page_frame in current_memory_state: # page fault가 아닌 경우
            pass
        else: # page fault인 경우
            page_fault[time] = "F"
            if EMPTY in current_memory_state:
                current_memory_state[current_memory_state.index(EMPTY)] = current_requested_page_frame
            else:
                victim_page_frame_index = get_index_of_victim_in_current_memory_state_LFU(current_memory_state, page_reference_string, time)
                current_memory_state[victim_page_frame_index] = current_requested_page_frame
                print("victim_page_frame_index: ", victim_page_frame_index)
        memory_state.append(current_memory_state.copy())

if __name__ == "__main__":
    file_contents = get_file_contents("input.txt")
    N, M, W, K = get_NMWK(file_contents)
    page_reference_string = get_page_reference_string(file_contents)
    # print_inputs(N, M, W, K, page_reference_string)
    
    time = [i for i in range(1, len(page_reference_string)+1)]
    # memory_state = [0 for i in range(len(page_reference_string))]
    memory_state = []
    page_fault = ['-' for _ in range(len(page_reference_string))]
    # print_table(time, page_reference_string, memory_state, page_fault)
    # get_result_MIN(M, page_reference_string)
    # get_result_LRU(M, page_reference_string)
    get_result_LFU(M, page_reference_string)
    print_table(time, page_reference_string, memory_state, page_fault)


