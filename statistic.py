import codecs


class Stat():
    '''
    This class is the statistic, there are this methods
        add_temp_score
            Additing number in temp_score (Using for stopping and continuing game)
        add_score
            Additing number in score
        add_max_score
            Additing number in max_score if that number bigger then past
        add_level
            Additing number in score
        plus_temp
            Summ all components in temp_score array
        rewrite_file
            This method can rewrite statistic.py file with:
                additing new statistic`s data (null = False)
                eraseing all statistics (null = True)
    '''
    def __init__(self):
        self.temp_score = []
        self.score = [1993, 1668, 2329, 3096]
        self.max_score = 3096
        self.levels = [33, 27, 35, 31]
        self.max_level = 35

    def add_temp_score(self, num):
        self.temp_score.append(num)

    def add_score(self, num):
        self.score.append(num)

    def add_max_score(self, num):
        if self.max_score < num: self.max_score = num
        self.add_score(num)
    
    def add_level(self, num):
        self.levels.append(num)
        if num > self.max_level: self.max_level = num

    def plus_temp(self):
        result = 0
        for i in self.temp_score():
            result += i
        return result

    def rewrite_file(self, null = False):

        help_flags = ['score', 'max_score', 'levels', 'max_level']
        f = codecs.open('statistic.py', 'r', 'utf-8')
        data = f.read()
        f.close()
        past_data = data
        data = data.split('\n')
        new_data = ''
        for line in data:
            temp_line = line
            temp_line = temp_line.strip(' ')
            if temp_line[0:4] == 'self':
                temp_line_2 = temp_line.split(' = ')
                temp_line_2 = temp_line_2[0].split('.')
                if temp_line_2[1] in help_flags: 
                    if temp_line_2[1] == 'score':
                        line = line.split(' = ')
                        if len(line) > 1: line = '{} = {}'.format(line[0], self.score)
                        else: line = line[0]
                    elif temp_line_2[1] == 'max_score':
                        line = line.split(' = ')
                        if len(line) > 1: line = '{} = {}'.format(line[0], self.max_score)
                        else: line = line[0]
                    elif temp_line_2[1] == 'levels':
                        line = line.split(' = ')
                        if len(line) > 1: line = '{} = {}'.format(line[0], self.levels)
                        else: line = line[0]
                    elif temp_line_2[1] == 'max_level':
                        line = line.split(' = ')
                        if len(line) > 1: line = '{} = {}'.format(line[0], self.max_level)
                        else: line = line[0]
                    print(line)
            if line != '' : new_data += line + '\n'
        if past_data != new_data:
            f = codecs.open('statistic.py', 'w', 'utf-8')
            f.write(new_data)
            f.close()
