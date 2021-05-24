import time
import random


def calc_duration(func):
    def decorated():
        start_time = time.time()
        func()
        print('elapsed time is about <{}> seconds'.format(time.time() - start_time))
        return

    return decorated


@calc_duration
def long_executing_task():  # func(*args, **kwargs) ==== long_executing_task
    for index in range(3):
        print('Iteration {index}')
        time.sleep(random.random())


def suppress_errors(errors_types):
    def _decorator(func):
        def decorated(key):
            try:
                func(key)
                message = "everything is ok"
            except errors_types:
                message = "error is silented"
            return message

        return decorated

    return _decorator


@suppress_errors((
        KeyError,
        ValueError,
))
def potentially_unsafe_func(key: str):
    print(f'Get data by the key {key}')
    data = {'name': 'test', 'age': 30}
    return data[key]


def result_between(value_min, value_max):
    def _decorator(func):
        def decorated(numbers):
            assert hasattr(numbers, '__iter__'), "Argument is not iterable"
            for number in numbers:
                assert isinstance(number, (int, float)), "TypeError"
            result = func(numbers)
            assert value_min <= result <= value_max, "ValueError"
            return
        return decorated
    return _decorator


def len_more_than(s_len):
    def _decorator(func):
        def decorated(string):
            assert isinstance(string, str), "TypeError"
            result = func(string)
            assert len(result) >= s_len, "ValueError"
            return
        return decorated
    return _decorator


@result_between(0, 50)
def sum_of_values(numbers):
    return sum(numbers)


@len_more_than(10)
def show_message(message: str) -> str:
    return f'Hi, you sent: {message}'


def replace_commas(func):
    def decorated(message):
        result = func(message)
        for x in (":", ";", ".", ","):
            result = result.replace(x, ' ')

        return result

    return decorated


def words_title(func):
    def decorated(message):
        result = func(message)
        titled_parts = result.split()
        final_result = ""
        for word in titled_parts:
            if len(word) == 1:
                final_result += word + " "
                continue
            word = word[0].upper() + word[1:len(word)-1] + word[len(word)-1].upper()
            final_result += word + " "

        return final_result

    return decorated


@words_title
@replace_commas
def process_text(text: str) -> str:
    return text.replace(':', ',')


@replace_commas
@words_title
def another_process(text: str) -> str:
    return text.replace(':', ',')


if __name__ == '__main__':
    long_executing_task()  # print "elapsed time is about <> seconds"
    print(potentially_unsafe_func('name'))  # everything is ok
    print(potentially_unsafe_func('last_name'))  # error is silented
    sum_of_values((1, 3, 5, 7))  # ValueError
    show_message('Howdy, howdy my little friend')
    print(process_text('the French revolution resulted in 3 concepts: freedom,equality,fraternity'))
    print(another_process('the French revolution resulted in 3 concepts: freedom,equality,fraternity'))
