sequence1 = '(((([{}]))))'
sequence2 = '[([])((([[[]]])))]{()}'
sequence3 = '{{[()]}}'
sequence4 = '}{}'
sequence5 = '{{[(])]}}'
sequence6 = '[[{())}]'

KEY_DICT = {')': '(', '}': '{', ']': '['}


class Stack:
    def __init__(self):
        self.stack = []

    def isEmpty(self):  # проверка стека на пустоту. Метод возвращает True или False.
        if len(self.stack) == 0:
            return True
        return False

    def push(self, item):  # добавляет новый элемент на вершину стека. Метод ничего не возвращает.
        self.stack.append(item)

    def pop(self):  # удаляет верхний элемент стека. Стек изменяется. Метод возвращает верхний элемент стека
        if len(self.stack) == 0:
            return None
        removed = self.stack.pop()
        return removed

    def peek(self):  # возвращает верхний элемент стека, но не удаляет его. Стек не меняется.
        if not self.isEmpty():
            last_item = self.stack[-1]
            return last_item
        return None

    def size(self):  # возвращает количество элементов в стеке.
        return len(self.stack)


def check_balance(seq_brackets):
    s = Stack()
    for item in seq_brackets:
        if item in KEY_DICT.keys():
            if s.peek() == KEY_DICT[item]:
                s.pop()
            else:
                return False
        else:
            s.push(item)
    return s.isEmpty()


if __name__ == '__main__':
    sequence_ = input('Input brackets sequence  ')
    if check_balance(sequence_):
        print('Balanced')
    else:
        print('Not balanced')
