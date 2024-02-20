"""
@Author = 'Michael Stanley'

These are utilities that help with testing.

make_namedtuple creates one-off named tuples for concisely passing data from 
the fixture method to the test methods.

generate_true_false_matrix_from_named_tuple creates a list of true and false 
values, and a list of corresponding ids,
to be passed into a test fixture.

generate_true_false_matrix_from_list_of_strings is a convenience function
It takes a string name and a list of strings, and returns the true-false matrix
built from those values. 

assert_has_only_these_calls asserts that the mock has been called with the 
specified calls and only the specified calls. 

============ Change Log ============
01/17/2023 = Added generate_true_false_matrix_from_list_of_strings

01/11/2023 = Added assert_has_only_these_calls

10/01/2020 = Created.

============ License ============
Copyright (C) 2020, 2023-2024 Michael Stanley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
__version__ = "0.3.1"

from collections import namedtuple


def make_namedtuple(class_name, **fields):
    """
    :param class_name: The name of the tuple class. Same as namedtuple(class_name=).
    :param fields: A keyword dictionary of field names and values. The names are the same as namedtuple(field_names=)
    :return: A namedtuple of type class_name, with field_names corresponding to the keys of the fields dictionary and
    field values corresponding to the values of the fields dictionary.

    enterprise = make_namedtuple("Starship", name="U.S.S. Enterprise", registry_number="NCC-1701")

    is the same as

    starship_tuple = namedtuple("Starship", ["name", "registry_number"])
    enterprise = starship_tuple("U.S.S. Enterprise", "NCC-1701")

    This is useful when you want to make a one-off namedtuple. It can be used to pass data concisely from a testing
    fixture to the test methods.
    """
    return namedtuple(class_name, fields)(*fields.values())


def generate_true_false_matrix_from_namedtuple(input_namedtuple):
    """
    :param input_namedtuple: A named tuple whose fields will be used to generate the True False matrix.
    :return: Two lists: true_false_matrix and test_ids. The True-False matrix is a list of the namedtuples
    that is of size len(input_tuple) and with the fields set to every combination of True and False.
    The list of ids is a list of strings that describe the corresponding tuples.

    Given: input_tuple = namedtuple("burger_toppings", ["with_cheese", "with_ketchup", "with_mustard"])

    true_false_matrix will be:
    [
        burger_toppings(with_cheese=False, with_ketchup=False, with_mustard=False),
        burger_toppings(with_cheese=True,  with_ketchup=False, with_mustard=False),
        burger_toppings(with_cheese=False, with_ketchup=True,  with_mustard=False),
        burger_toppings(with_cheese=True,  with_ketchup=True,  with_mustard=False),
        burger_toppings(with_cheese=False, with_ketchup=False, with_mustard=True),
        burger_toppings(with_cheese=True,  with_ketchup=False, with_mustard=True),
        burger_toppings(with_cheese=False, with_ketchup=True,  with_mustard=True),
        burger_toppings(with_cheese=True,  with_ketchup=True,  with_mustard=True)
    ]

    and test_ids will be:
    [
        'burger_toppings(with_cheese=False, with_ketchup=False, with_mustard=False)',
        'burger_toppings(with_cheese=True,  with_ketchup=False, with_mustard=False)',
        'burger_toppings(with_cheese=False, with_ketchup=True,  with_mustard=False)',
        'burger_toppings(with_cheese=True,  with_ketchup=True,  with_mustard=False)',
        'burger_toppings(with_cheese=False, with_ketchup=False, with_mustard=True)',
        'burger_toppings(with_cheese=True,  with_ketchup=False, with_mustard=True)',
        'burger_toppings(with_cheese=False, with_ketchup=True,  with_mustard=True)',
        'burger_toppings(with_cheese=True,  with_ketchup=True,  with_mustard=True)'
    ]

    Note that true_false_matrix is a list of namedtuples and test_ids is the list of the string representations of
    those same namedtuples.

    Inline comments are based upon the burger_toppings named tuple.
    """
    number_of_fields = len(input_namedtuple._fields)
    
    if number_of_fields < 1:
        raise ValueError("The named tuple passed in must have at least one field.")

    powers_of_two = {2**i: i for i in range(number_of_fields)}
    '''
    Creates a dictionary where the powers of two are mapped to their exponents for the exponents from
    0 to <number_of_fields
    E.G. given number_of_fields = 3, then powers_of_two = {1: 0, 2: 1, 4: 2}
    '''

    these_field_values = [False for i in range(number_of_fields)]
    '''
    Creates a list of False values for each field in the namedtuple.
    This list will be used and manipulated to create instances of the namedtuple .
    '''

    true_false_matrix = []
    test_ids = []

    for i in range(1, 2**number_of_fields + 1):
        this_combination = input_namedtuple._make(these_field_values)
        '''
        Make an instance of the namedtuple using the current value of these_field_values. 
        '''

        true_false_matrix.append(this_combination)
        test_ids.append(str(this_combination))

        for this_power_of_two, corresponding_index in powers_of_two.items():
            if i % this_power_of_two == 0:
                these_field_values[corresponding_index] = not these_field_values[corresponding_index]
        '''
        This for loop goes through the powers_of_two generated above. When it finds one that divided evenly 
        into the current value of i, it flips the value in the corresponding index in these_field_values.
        This means that the first value in these_field_values will be flipped every iteration, 
        the second value will be flipped every other iteration, the third value will be flipped every 
        fourth iteration, etc.
        '''

    return true_false_matrix, test_ids


def generate_true_false_matrix_from_list_of_strings(name, input_strings):
    """
    A convenience function. It takes a string name and a list of strings, and 
    returns the true-false matrix built from those values.
    
    generate_true_false_matrix_from_list_of_strings(
        "burger_toppings", 
        ["with_cheese", "with_ketchup", "with_mustard"]
    )

    is the equivalent of

    burger_toppings = namedtuple(
        "burger_toppings", 
        ["with_cheese", "with_ketchup", "with_mustard"]
    )
    generate_true_false_matrix_from_namedtuple(burger_toppings)
    """
    named_tuple_for_generating = namedtuple(name, input_strings)
    return generate_true_false_matrix_from_namedtuple(named_tuple_for_generating)


def assert_has_only_these_calls(mock, calls, any_order=False):
    """
    assert the mock has been called with the specified calls and only
    the specified calls. The counts are compared and then the 
    `mock_calls` list is checked for the calls.

    If `any_order` is False (the default) then the calls must be
    sequential. 
    
    If `any_order` is True then the calls can be in any order, but
    they must all appear in `mock_calls`.

    This is the natural continuation of `assert_called_once_with` and is based 
    on that method.
    """

    provided_call_count = len(calls)

    if not mock.call_count == provided_call_count:
        msg = f"Expected {mock._mock_name or 'mock'} to be called " \
              f" {provided_call_count} times. Called {mock.call_count} " \
              f"times.{mock._calls_repr()}"
        raise AssertionError(msg)
    return mock.assert_has_calls(calls, any_order)


def assert_lists_contain_same_items(list1, list2):
    """
    Asserts that every item in list one is also in list2 and vice-versa, in any order. If they have to be in the same
    order, use list1 == list2.

    :param list1: The first list to compare.
    :param list2: The second list to compare.
    :raises AssertionError: If any item in one list is not also in the other list. 
    """
    for item in list1:
        assert item in list2
    for item in list2:
        assert item in list1
