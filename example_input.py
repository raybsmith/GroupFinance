import group_obj

# Format:
# Create group
# group = group_obj.Group(names=["list", "of", "names"])
#
# Add list of transactions, each with the following information
#
# - payer(s) as
#   Single payer
#   > 1) "Jon"
#   Multiple payers
#   > 2) {"list" : 30, "names" : 10}
#
# - who was involved as
#   Equal split among everyone in the group:
#   > 1) invlvd="all"
#   Equal split among everyone else in the group:
#   > 2) invlvd="all others"
#   Equal split among a subset of the group:
#   > 3) invlvd=["list", "of", "names"]
#   Inequal split:
#   > 4) split={"list" : 2, "of" : 3.1}
#
# - total (if neither a list of payers/totals nor a split was defined)
#   > total=35.25
#
# - comment (optional)
#
# Note, if payers is a dictionary, and a split is defined for payment,
# then the sums must be equal.
#
# Finally, call the simplify method, either without an argument (to
# distribute transactions among the group and keep amounts small) or
# with a person's name as argument, so s/he will act as the "bank" for
# everyone.

ExmplGroup = group_obj.Group(names=["Jon", "Sue", "Joe", "Beth", "Jane"])
# Jon's total shared group expenses, to be shared equally among
# everyone (including Jon).
ExmplGroup.store_new_transaction("Jon",
        invlvd="all", total=198.13,
        comment="Jon's total group expenses")
# Sue owes Beth from cash loan.
ExmplGroup.store_new_transaction("Beth",
        invlvd=["Sue"], total=32,
        comment="Beth loaned Sue money")
# Joe and Sue paid for a dinner with Joe, Sue, and Jane.
ExmplGroup.store_new_transaction({"Joe" : 20, "Sue" : 35},
        invlvd=["Joe", "Sue", "Jane"],
        comment="Dinner out on Friday")
# Jane and Beth paid for a dinner with Jane, Beth, and Jon; Jon got
# dessert
ExmplGroup.store_new_transaction({"Jane" : 15, "Beth" : 25},
        split={"Jane" : 10, "Beth" : 10, "Jon" : 20},
        comment="Dinner out on Saturday")
# Jane loaned the rest of the group money for show tickets
ExmplGroup.store_new_transaction("Jane",
        invlvd="all others", total=55,
        comment="Dinner out on Saturday")

# Print balancing lists of transactions
# Distributing transactions
ExmplGroup.simplify()
print
# With Jane as "bank"
ExmplGroup.simplify("Jane")
print
# With Jon as "bank"
ExmplGroup.simplify("Jon")
