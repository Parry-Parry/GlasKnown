from config import PREFIX


class Post:
    def __init__(self, data, current):
        self.post_id = current
        self.data = ''
        self.prev_id = 0

        for line in data:
            if PREFIX in line:
                tmp_id = line.split('_')[-1]
                if tmp_id != current:
                    self.prev_id = tmp_id
            else:
                self.data += line + ' '

