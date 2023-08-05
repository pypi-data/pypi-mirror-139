"""This is the "nesterguoqun111.py" and it provides one function call print_lol() witch prints lists that may or may not include nested lists."""
def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
