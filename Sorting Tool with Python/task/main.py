import argparse
from collections import Counter


class NoArgValueException(Exception):
    pass


parser = argparse.ArgumentParser(description="This program prints info based on the datatype and the data you provide")
parser.add_argument("-dataType", "--dataType", choices=["long", "line", "word"], default="long", nargs="?")
# parser.add_argument("-sortIntegers", "--sortIntegers", action="store_true")
parser.add_argument("-sortingType", "--sortingType", choices=["natural", "byCount"], default="natural", nargs="?")
parser.add_argument("-inputFile", "--inputFile", type=str, nargs="?")
parser.add_argument("-outputFile", "--outputFile", type=str, nargs="?")

data_dict = {'long': 'number', 'word': 'word', 'line': 'line'}


def process_input_console(data_type):
    user_inputs = []
    while True:
        try:
            match data_type:
                case 'long' | 'word':
                    user_inputs += input().split()
                case 'line':
                    user_inputs.append(input())
        except EOFError:
            break
    return user_inputs


def process_input_file(file, data_type):
    user_inputs = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                match data_type:
                    case 'long' | 'word':
                        user_inputs += line.split()
                    case 'line':
                        user_inputs.append(line)
            except EOFError:
                f.close()
                break
    f.close()
    return user_inputs


def process_output(data_type, sorting_type, user_inputs_as_datatype, file=None):
    nl = '\n'
    if file:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(f'Total {data_dict[data_type]}s: {len(user_inputs_as_datatype)}.\n')
            match sorting_type:
                case 'natural':
                    if data_type in ['long', 'word']:
                        f.write(f'Sorted data: {" ".join(map(str, sorted(user_inputs_as_datatype)))}\n')
                    else:
                        f.write(f'Sorted data:\n{nl.join(map(str, sorted(user_inputs_as_datatype)))}')
                        f.write('\n')
                case 'byCount':
                    number_counter = Counter(sorted(user_inputs_as_datatype, reverse=True))
                    for number in reversed(number_counter.most_common()):
                        f.write(
                            f'{number[0]}: {number[1]} time(s), {int(number[1] / len(user_inputs_as_datatype) * 100)}%.\n')
            f.close()
    else:
        print(f'Total {data_dict[data_type]}s: {len(user_inputs_as_datatype)}.')
        match sorting_type:
            case 'natural':
                if data_type in ['long', 'word']:
                    print(f'Sorted data: {" ".join(map(str, sorted(user_inputs_as_datatype)))}')
                else:
                    print(f'Sorted data:\n{nl.join(map(str, sorted(user_inputs_as_datatype)))}')
            case 'byCount':
                number_counter = Counter(sorted(user_inputs_as_datatype, reverse=True))
                for number in reversed(number_counter.most_common()):
                    print(
                        f'{number[0]}: {number[1]} time(s), {int(number[1] / len(user_inputs_as_datatype) * 100)}%.')


def process_sorting():
    args, unknown = parser.parse_known_args()
    for unknown_argument in unknown:
        print(f'"{unknown_argument}" is not a valid parameter. It will be skipped.')
    if not args.sortingType:
        raise NoArgValueException("No sorting type defined!")
    if not args.dataType:
        raise NoArgValueException("No data type defined!")

    user_inputs = process_input_file(args.inputFile, args.dataType) if args.inputFile else process_input_console(
        args.dataType)

    match args.dataType:
        case 'long':
            for inp in user_inputs:
                if not inp.lstrip('-').isdigit():
                    print(f'"{inp}" is not a long. It will be skipped.')
            user_inputs_as_datatype = [int(inp) for inp in user_inputs if inp.lstrip('-').isdigit()]
            process_output(args.dataType, args.sortingType, user_inputs_as_datatype, args.outputFile)

        case 'word':
            user_inputs_as_datatype = [str(inp) for inp in user_inputs]
            process_output(args.dataType, args.sortingType, user_inputs_as_datatype, args.outputFile)

        case 'line':
            user_inputs_as_datatype = user_inputs
            process_output(args.dataType, args.sortingType, user_inputs_as_datatype, args.outputFile)


try:
    process_sorting()
except NoArgValueException as e:
    print(e.args[0])
