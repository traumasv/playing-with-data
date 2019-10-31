# tabletools.py
class LabledList:
    def __init__(self, data=None, index=None):
        if index == None:
            self.index = [i for i in range(data.length)]
        else:
            self.index = index
        self.values = data
    
    def __getitem__(self, key_list):
        keys = []
        values = []
        #if key_list is another LabeledList
        if isinstance(key_list, LabledList):
            #if the values are boolean
            if isinstance(key_list.values[0], bool):
                for i in range(len(key_list.values)):
                    if key_list.values[i] == True:
                        keys.append(self.index[i])
                        values.append(self.values[i])
            #if the values are not boolean
            else:
                #use the values to key retrieve items
                for key in key_list.values:
                    for i in range(len(self.index)):
                        if self.index[i] == key:
                            keys.append(self.index[i])
                            values.append(self.values[i])
        #if key_list is a list of values
        if isinstance(key_list, list):
            #if the values are boolean
            if isinstance(key_list[0], bool):
                for i in range(len(key_list)):
                    if key_list[i] == True:
                        keys.append(self.index[i])
                        values.append(self.values[i])
            #if the values are not boolean
            else:
                for key in key_list:
                    for i in range(len(self.index)):
                        if self.index[i] == key:
                            keys.append(self.index[i])
                            values.append(self.values[i])

        #if key_list is a single value
        else:
            for i in range(len(self.index)):
                if self.index[i] == key_list:
                    keys.append(self.index[i])
                    values.append(self.values[i])
            #if none is found
            if len(keys) < 1:
                return None
            #if one is found
            if len(keys) == 1:
                return values[0]
            #else, create a labledlist down below

        return LabledList(values, keys)
    
    def __str__(self):
        #padd the string so that it is fitted to the maximum length character of the entire value/index
        longest = 0
        for i in range(len(self.index)):
            length1 = len(str(self.values[i]))
            length2 = len(str(self.index[i]))
            if  length1 > longest:
                longest = length1
            if length2 > longest:
                longest = length2
        string = ''
        for i in range(len(self.index)):
            index = self.index[i]
            ind =' {:>{longest}} '.format(str(index), longest=longest)
            if isinstance(self.values[i], bool):
                val = ' {:>{longest}} '.format(str(self.values[i]), longest=longest)
            else:
                val = ' {:>{longest}} '.format(str(self.values[i]), longest=longest)
            string += (ind + val + "\n")
        return string

    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        for value in self.values:
            yield value
    
    def __eq__(self, scalar):
        values = [x == scalar for x in self.values]
        return LabledList(values, self.index)
    
    def __ne__(self,scalar):
        values = [x != scalar for x in self.values]
        return LabledList(values, self.index)
    
    def __gt__(self, scalar):
        values = [x > scalar for x in self.values]
        return LabledList(values, self.index)
    
    def __lt__(self, scalar):
        values = [x < scalar for x in self.values]
        return LabledList(values, self.index)

    def map(self, f):
        values = [f(x) for x in self.values]
        return LabledList(values, self.index)

class Table:
    def __init__(self, data, index=None, columns=None):
        self.values = data
        if index == None:
            self.index = [x for x in range(len(data))]
        if columns == None:
            self.columns = [x for x in range(len(data[0]))]
        if index != None:
            self.index = index
        if columns != None:
            self.columns = columns
    
    def __str__(self):
        new_line = lambda x : x + '\n'
        longest = 0
        for i in range(len(self.values)):
            for j in range(len(self.columns)):
                length = len(str(self.values[i][j]))
                if length > longest:
                    longest = length
        #longest length of integer is found
        string = ' '*longest
        for col in self.columns:
            string += ' {:>{longest}} '.format(str(col), longest=longest)
        string = new_line(string)
        for i in range(len(self.values)):
            string += ' {:>{longest}} '.format(str(self.index[i]), longest=longest)
            for j in range(len(self.values[0])):
                string += ' {:>{longest}} '.format(str(self.values[i][j]), longest=longest)
            string = new_line(string)
        return string

    def __repr__(self):
        return str(self)

    def __getitem__(self, col_list):
        table = []
        col_nums = []
        if isinstance(col_list, LabledList):
            #if the values list contains boolean values
            if isinstance(col_list.values[0], bool):
                col_nums = [x for x in range(len(self.columns))]
                for i in range(len(self.values)):
                    if col_list.values[i] == True:
                        table.append(self.values[i])
            #if values list contains non-boolean
            else:
                #get the index of the columns that match with the cols listed in col_list
                for col in col_list.values:
                    for i in range(len(self.columns)):
                        if self.columns[i] == col:
                            col_nums.append(i)
                
                #add the columns to the table
                for i in range(len(self.values)):
                    row = []
                    for j in range(len(self.columns)):
                        if j in col_nums:
                            row.append(self.values[i][j])
                    table.append(row)

        #if the col_list is a list
        if isinstance(col_list, list):
            #if the col_list contains booleans
            if isinstance(col_list[0], bool):
                col_nums = [x for x in range(len(self.columns))]
                for i in range(len(self.values)):
                    if col_list[i] == True:
                        table.append(self.values[i])

            #if col_list doesn't contain booleans
            else:
                for col in col_list:
                    for i in range(len(self.columns)):
                        if self.columns[i] == col:
                            col_nums.append(i)
                
                #add the columns to the table
                for i in range(len(self.values)):
                    row = []
                    for j in range(len(self.columns)):
                        if j in col_nums:
                            row.append(self.values[i][j])
                    table.append(row)
        #if col_list is a single value            
        if isinstance(col_list, str) | isinstance(col_list, int):
            for i in range(len(self.columns)):
                if self.columns[i] == col_list:
                    col_nums.append(i)
            
            #add the columns to the table
            for i in range(len(self.values)):
                row = []
                for j in range(len(self.columns)):
                    if j in col_nums:
                        row.append(self.values[i][j])
                table.append(row)
                    
        #if nothing was found
        if len(table) == 0:
            return None

        #if there are only one column, return a LabeledList
        if len(table[0]) == 1:
            return LabledList([row[0] for row in table], self.index)
        #if there are more than one columns, return a table
        if len(table[0]) > 1:
            return Table(table, self.index, [self.columns[i] for i in col_nums])
    
    def head(self, n):
        return Table(self.values[:n], self.index[:n], self.columns)
    
    def tail(self, n):
        return Table(self.values[len(self.values) - n:], self.index[len(self.values) - n:], self.columns)
    
    def shape(self):
        return (len(self.index), len(self.columns))
    
def read_csv(fn):
    table = []
    with open(fn, "r") as data:
        header = next(data).split(',')
        header[-1] = header[-1].strip()
        for line in data:
            cols = line.strip().split(',')
            table.append(cols)
        for i in range(len(table)):
            for j in range(len(header)):
                try:
                    table[i][j] = float(table[i][j])
                except:
                    pass

        return Table(table, None, header)