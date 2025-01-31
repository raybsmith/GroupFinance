INTRO
=====
GroupFinance is a Python program to help deal with money and finances
in a group. This includes tracking individuals' expenses, so that at
the end, you can properly balance. This program also simplifies the
final result to the smallest number of transactions to balance
everyone. This can be done either keeping transaction amounts small or
having one person act as "bank".

QUICK START
===========
To use GroupFinance, you will need Python installed.
To begin, first create a transaction file based on the example file.

    cp exapmle_input.py myGroupFin.py

This file will include a list of names of the people in the group.
Then, add transactions to the file. Finally, to see a simplified way
to square up the group, simply run the file

    python myGroupFin.py

EXAMPLE
=======
Here's an example of what a very simple transactions file might look
like. For more detail about options, check out the example_input.py
file.

```python
import group_obj

# Weekend trip

names = ["Jon", "Sue", "Joe"]
group = group_obj.Group(names)

# Jon covered everyone's tickets to the game
group.store_new_transaction("Jon",
        invlvd="all", total=75,
        comment="Cheap tickets to the baseball game")

# Sue paid for lunch with just her and Joe
group.store_new_transaction("Sue",
        invlvd=["Sue", "Joe"], total=42.5,
        comment="Sue and Joe's lunch Friday")

# Joe covered dinner the second night, but Sue didn't have drinks,
# so her part was only $15.50, whereas Joe's and Jon's are both $30.
group.store_new_transaction("Joe",
        split={"Joe" : 30,
               "Jon" : 30,
               "Sue" : 15.50},
        comment="Dinner Friday")

# Figure out easiest repayment:
group.simplify()
```

the output to the example file above is simply:

    Sue owes Jon $19.25
    Joe owes Jon $0.75

