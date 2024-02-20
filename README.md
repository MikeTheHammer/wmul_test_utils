# WMUL-FM Test Untilities

These are utilities that help with testing WMUL-FM's other python modules.

1. `make_namedtuple` creates one-off named tuples for concisely passing data from the fixture method to the test 
methods.

2. `generate_true_false_matrix_from_named_tuple` creates a list of true and false values, and a list of corresponding 
ids, to be passed into a pytest test fixture.

3. `generate_true_false_matrix_from_list_of_strings` is a convenience function. If you give it a string name, and a 
list of strings, it will create a named tuple from those and then call `generate_true_false_matrix_from_named_tuple`.

4. `generate_combination_matrix_from_dataclass` When given a dataclass (the class, not an instance), whose fields are 
all either boolean or enums, it will return two lists. The first list will contain instances of the dataclass covering 
all possible values of the fields. The second list will be the test_ids of those instances. These are indended to be
passed to a pytest fixture.

5. `assert_has_only_these_calls` receives a `unittest.mock` object and asserts that it has been called with the 
specified calls and only the specified calls. The counts are compared and then the `mock_calls` list is checked for 
the calls.

6. `assert_lists_contain_same_items` asserts that every item in list one is also in list2 and vice-versa, in any order.

## make_namedtuple(class_name, **fields)
`class_name`: The name of the tuple class. Same as `namedtuple(class_name=)`.

`fields`: A keyword dictionary of field names and values. The names are the same as `namedtuple(field_names=)`.

`returns` A namedtuple of type `class_name`, with `field_names` corresponding to the keys of the fields dictionary and field values corresponding to the values of the fields dictionary.

```
enterprise = make_namedtuple("Starship", name="U.S.S. Enterprise", registry_number="NCC-1701")
```

is the same as

```
starship_tuple = namedtuple("Starship", ["name", "registry_number"])
enterprise = starship_tuple("U.S.S. Enterprise", "NCC-1701")
```

This is useful when you want to make a one-off namedtuple. It can be used to pass data concisely from a testing fixture to the test methods.

## generate_true_false_matrix_from_namedtuple(input_namedtuple)
`input_namedtuple` A named tuple whose fields will be used to generate the True False matrix.

`returns` Two lists: true_false_matrix and test_ids. The True-False matrix is a list of the namedtuples that is of size len(input_tuple) and with the fields set to every combination of True and False. The list of ids is a list of strings that describe the corresponding tuples.

Given: `input_tuple = namedtuple("burger_toppings", ["with_cheese", "with_ketchup", "with_mustard"])`

`true_false_matrix` will be:  
```
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
```

and `test_ids` will be:
```
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
```

Note that true_false_matrix is a list of namedtuples and test_ids is a list of the string representations of those same namedtuples.

## generate_true_false_matrix_from_list_of_strings(name, input_strings):
A convenience function. It takes a string name and a list of strings, and 
returns the true-false matrix built from those values.

```
generate_true_false_matrix_from_list_of_strings(
    "burger_toppings",
    ["with_cheese", "with_ketchup", "with_mustard"]
)
```

is the equivalent of

```
burger_toppings = namedtuple(
    "burger_toppings", 
    ["with_cheese", "with_ketchup", "with_mustard"]
)
generate_true_false_matrix_from_namedtuple(burger_toppings)
```

## generate_combination_matrix_from_dataclass(input_dataclass: dataclasses.dataclass) -> list:
When given a dataclass (the class, not an instance), whose fields are all either boolean or enums, it will return 
two lists. The first list will contain instances of the dataclass covering all possible values of the fields. 
The second list will be the test_ids of those instances. If the dataclass provides a .test_id(self) function, 
that function will be used to generate the test_ids. Otherwise, the dataclass's \_\_str__(self) function will be used.

Function will generate up to a maximum of 1,000,000 instances. That limit was chosen arbitrarily and may be 
changed with testing.

`input_dataclass` A dataclass (not an instance), whose fields are all either boolean or enums.  
`returns` Two lists: dataclass_matrix and test_ids. dataclass_matrix is the list of instances of input_dataclass 
             covering all possible values of the fields. test_ids is the list of strings that describe those instances.   
`raises TypeError` If input_dataclass is not a dataclass or is an instance of a dataclass.   
`raises TypeError` If any of the fields of the dataclass are not a subclass of either bool or Enum.  
`raises ValueError` If the total number of possible values excees 1,000,000.

Given:
```
class Colors(Enum):
    BROWN = 0
    BLACK = 1
    RED = 2

@dataclass
class Car:
    runs: bool
    color: Colors
        
    def test_id(self):
        return f"Car(runs={self.runs}, color={self.color})"

```


`dataclass_matrix` will be:
```
[
    Car(runs=True, color=Colors.BLACK),
    Car(runs=True, color=Colors.BROWN),
    Car(runs=True, color=Colors.RED),
    Car(runs=False, color=Colors.BLACK),
    Car(runs=False, color=Colors.BROWN),
    Car(runs=False, color=Colors.RED)
]
```

`test_ids` will be:
```
[
    "Car(runs=True, color=Colors.BLACK)",
    "Car(runs=True, color=Colors.BROWN)",
    "Car(runs=True, color=Colors.RED)",
    "Car(runs=False, color=Colors.BLACK)",
    "Car(runs=False, color=Colors.BROWN)",
    "Car(runs=False, color=Colors.RED)"
]
```


## assert_has_only_these_calls(mock, calls, any_order=False)
`mock` a `unittest.mock` object.

`calls` a list of calls.

If `any_order` is False (the default) then the calls must be
sequential. 

If `any_order` is True then the calls can be in any order, but
they must all appear in `mock_calls`.

assert the mock has been called with the specified calls and only
the specified calls. The counts are compared and then `assert_has_calls` is called.

This is the natural continuation of `assert_called_once_with` and is based on that method.


## assert_lists_contain_same_items(list1, list2)
Asserts that every item in list one is also in list2 and vice-versa, in any order. If they have to be in the same
order, use list1 == list2.

`list1` The first list to compare.  
`list2` The second list to compare.  
`raises AssertionError` If any item in one list is not also in the other list.   
