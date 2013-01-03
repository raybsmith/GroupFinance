import group_obj

test_num = 2

if test_num == 1:
    newgroup = group_obj.Group(names=["r", "m", "c", "g", "p"])
    # m loaned $40 to r.
    newgroup.store_new_transaction("m", "even", others="r", total=40,
            payer_incl=False)
    # c bought a group dinner for all for $70.
    newgroup.store_new_transaction("c", "even", others="ALL", total=70,
            payer_incl=True)
    # g loaned the group $15 cash to xxx.
    newgroup.store_new_transaction("g", "even", others="ALL", total=15,
            payer_incl=False)
    # r paid for $20 lunch for g, r, and p.
    newgroup.store_new_transaction("r", "even", others=["g", "p"],
            total=20, payer_incl=True)

elif test_num == 2:
    skigroup = group_obj.Group(names=["b", "a", "r", "k", "s"])
    # Alex drove Alex, Ben, Ray, Kevin.
    skigroup.store_new_transaction("a", \
            invlvd=["b", "a", "r", "k"], total=42.9, \
            comment="A drove BARK")
    # Ben bought Kevin's bus ticket.
    skigroup.store_new_transaction("b", \
            invlvd=["k"], total=26, \
            comment="B bought K's bus ticket")
    # Ben bought Ray's day pass.
    skigroup.store_new_transaction("b", \
            invlvd=["r"], total=85, \
            comment="B bought R's day pass")
    # Ray bought groceries.
    skigroup.store_new_transaction("r", \
            invlvd="all", total=69.46, \
            comment="R bought groceries for all")
    # Ray paid for appetizers at Applebees.
    skigroup.store_new_transaction("r", \
            invlvd="all", total=9, \
            comment="R paid for appetizers at Applebees")
    # Ray bought lunch at Frank Pepe's.
    skigroup.store_new_transaction("r", \
            invlvd=["b", "a", "r", "k"], total=21.96, \
            comment="R bought lunch at Frank Pepe's")
    # Alex paid for the tip at Frank Pepe's.
    skigroup.store_new_transaction("a", \
            invlvd=["b", "a", "r", "k"], total=5, \
            comment="A paid for tip at Frank Pepe's")
    for transaction in skigroup.transactions:
        print transaction
    skigroup.simplify()
