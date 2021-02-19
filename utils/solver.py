import numpy as np

def text_correction(matrix):  
    m = matrix
    m = m.split('\n')[:-1]
    for i in range(len(m)):
        m[i] = m[i].split()
        for j in range(len(m[i])):
            if (m[i][j].find('c') != -1 or m[i][j].find('C') != -1 or
                m[i][j].find('i') != -1 or m[i][j].find('t') != -1 or
                m[i][j].find('1') != -1 or m[i][j].find('W') != -1 or
                m[i][j].find('w') != -1 or m[i][j].find('©') != -1):
                m[i][j]= "1C"

            if (m[i][j].find('€') != -1 or m[i][j].find('9') != -1 or
                m[i][j].find('E') != -1 or m[i][j].find('e') != -1 or
                m[i][j].find('o') != -1):
                m[i][j]= "E9"

            if (m[i][j].find('B') != -1 or m[i][j].find('D') != -1 or
                m[i][j].find('O') != -1 or m[i][j].find('0') != -1):
                m[i][j]= "BD"

            if (m[i][j].find('5') != -1 or m[i][j].find('§') != -1 or
                m[i][j].find('S') != -1 or m[i][j].find('6') != -1):
                m[i][j]= "55"
    return m

def visit(m,visited,cursor,row, buffer, sequence, seq_index):
    if row == True:
        nv = sequence[seq_index] in m[cursor["x"]]
        if nv == True:
            where = np.where(m[cursor["x"]] == sequence[seq_index])[0]
        else:
            where = []
        for i in where:        
            if visited[cursor["x"]][i] == 0:               
                cursor["y"] = i
                buffer["simbols"].append(m[cursor["x"]][cursor["y"]])
                buffer["path"].append((cursor["x"],cursor["y"]))
                visited[cursor["x"]][cursor["y"]] = 1
                seq_index += 1
                row = False
                return visited, cursor, row, buffer, seq_index
         # If all neighbors visited
        if seq_index > 1:
            # Then go back to the last position
            buffer["simbols"].pop()
            buffer["path"].pop()
            cursor["x"] = buffer["path"][-1][0]
            cursor["y"] = buffer["path"][-1][1]
            seq_index -= 1
            row = False
            return visited, cursor, row, buffer, seq_index

        elif seq_index == 1:
            where = np.where(m[cursor["x"]] == sequence[seq_index-1])[0]
            # Visiting the not visited neighbors
            for i in where:
                if visited[cursor["x"]][i] == 0:               
                    cursor["y"] = i
                    buffer["simbols"].append(m[cursor["x"]][cursor["y"]])
                    buffer["path"].append((cursor["x"],cursor["y"]))
                    visited[cursor["x"]][cursor["y"]] = 1
                    # Do not upgrade seq_index
                    row = False
                    return visited, cursor, row, buffer, seq_index
            # If no neighbor avaliable go back
            buffer["simbols"].pop()
            buffer["path"].pop()
            cursor["x"] = buffer["path"][-1][0]
            cursor["y"] = buffer["path"][-1][1]
            #seq_index -= 1
            row = False
            return visited, cursor, row, buffer, seq_index

        elif seq_index == 0:
            for i in range(len(m[cursor["x"]])):
                if visited[cursor["x"]][i] == 0:
                    cursor["y"] = i
                    buffer["simbols"].append(m[cursor["x"]][cursor["y"]])
                    buffer["path"].append((cursor["x"],cursor["y"]))
                    visited[cursor["x"]][cursor["y"]] = 1
                    row = False
                    return visited, cursor, row, buffer, seq_index

        else:
            # OK, that sequence dont exist on the matrix
            print("ERROR")
    else:
        nv = sequence[seq_index] in m[:,cursor["y"]]
        if nv == True:
            where = np.where(m[:, cursor["y"]] == sequence[seq_index])[0]
        else:
            where = []
        for i in where:
            if visited[i][cursor["y"]] == 0:
                cursor["x"] = i
                buffer["simbols"].append(m[cursor["x"]][cursor["y"]])
                buffer["path"].append((cursor["x"],cursor["y"]))
                visited[cursor["x"]][cursor["y"]] = 1
                seq_index += 1
                row = True
                return visited, cursor, row, buffer, seq_index
        # If all neighbors visited
        if seq_index > 1:
            # Then go back to the last position
            buffer["simbols"].pop()
            buffer["path"].pop()
            cursor["x"] = buffer["path"][-1][0]
            #cursor["y"] = buffer["path"][-1][1]
            seq_index -= 1
            row = True
            return visited, cursor, row, buffer, seq_index

        elif seq_index == 1:
            where = np.where(m[:, cursor["y"]] == sequence[seq_index-1])[0]
            # Visiting the not visited neighbors
            for i in where:
                if visited[i][cursor["y"]] == 0:               
                    cursor["x"] = i
                    buffer["simbols"].append(m[cursor["x"]][cursor["y"]])
                    buffer["path"].append((cursor["x"],cursor["y"]))
                    visited[cursor["x"]][cursor["y"]] = 1
                    # Do not upgrade seq_index
                    row = True
                    return visited, cursor, row, buffer, seq_index
            # If no neighbor avaliable go back
            buffer["simbols"].pop()
            buffer["path"].pop()
            #cursor["x"] = buffer["path"][-1][0]
            #cursor["y"] = buffer["path"][-1][1]
            seq_index -= 1
            row = True
            return visited, cursor, row, buffer, seq_index

        elif seq_index == 0:
            for i in range(len(m[:,cursor["y"]])):
                 if visited[i][cursor["y"]] == 0:
                    cursor["x"] = i
                    buffer["simbols"].append(m[cursor["x"]][cursor["y"]])
                    buffer["path"].append((cursor["x"],cursor["y"]))
                    visited[cursor["x"]][cursor["y"]] = 1
                    row = True
                    return visited, cursor, row, buffer, seq_index

        else:
            # OK, that sequence dont exist on the matrix
            print("ERROR")

def solver(matrix, sequence):
    '''
    Solves one sequence
    ''' 
    BUFFER_SIZE = 6
    seq_index = 0
    visited = np.array(matrix)
    visited = np.zeros(visited.shape)
    row = True
    cursor = {"x": 0, "y": 0}
    buffer = {"simbols":[],"path":[]}
    while len(buffer['path']) <= BUFFER_SIZE and seq_index < len(sequence):
        visited, cursor, row, buffer, seq_index = visit(matrix, visited, cursor, row, buffer, sequence, seq_index)
    print(f'sequence: {buffer["simbols"]}')
    print(f'path: {buffer["path"]}')
    return buffer["path"]



if __name__ == "__main__":
    matrix = np.array([["7A", "BD", "55", "55", "1C", "1C"],
                       ["7A", "1C", "55", "E9", "1C", "7A"],
                       ["7A", "7A", "1C", "7A", "55", "E9"],
                       ["1C", "7A", "BD", "1C", "BD", "1C"],
                       ["BD", "E9", "1C", "7A", "1C", "7A"]])
    sequence = ["55", "7A" ,"55"]
    solver(matrix, sequence)


