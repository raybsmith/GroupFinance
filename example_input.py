import group_obj

test_num = 4

if test_num == 1:
    PSgroup = group_obj.Group(names=["r", "yu", "d", "j",
        "yo", "lu", "li", "z"])
    # R's total group expenses.
    PSgroup.store_new_transaction("r",
            invlvd="all", total=198.13,
            comment="Ray's total group expenses")
    # Zach's total group expenses.
    PSgroup.store_new_transaction("z",
            invlvd="all", total=153.25,
            comment="Zach's total group expenses")
    # Yuqing's total group expenses.
    PSgroup.store_new_transaction("yu",
            invlvd="all", total=16,
            comment="Yuqing's total group expenses")
    # David's total group expenses.
    PSgroup.store_new_transaction("d",
            invlvd="all", total=220.43,
            comment="David's total group expenses")
    # Joel's total group expenses.
    PSgroup.store_new_transaction("j",
            invlvd="all", total=324.90,
            comment="Joel's total group expenses")
    # Lucas owe's Ray from cash loaned during Hull.
    PSgroup.store_new_transaction("r",
            invlvd=["lu"], total=32,
            comment="Lucas borrowed cash from Ray during Hull.")
    # Ray owes Zach from uhaul.
    PSgroup.store_new_transaction("z",
            invlvd=["r"], total=18,
            comment="Zach paid for Ray+Zach shared Uhaul.")
#    for transaction in PSgroup.transactions:
#        print transaction
    PSgroup.simplify()

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

elif test_num == 3:
    aptgroup = group_obj.Group(names=["b", "a", "r", "k"])
    # Ray got paid back for Lea's furniture -- owes back to rest
    aptgroup.store_new_transaction("r", \
            invlvd=["b", "a", "r"], total=-48.39, \
            comment="R paid back for Lea's bed")
    aptgroup.simplify()

elif test_num == 4:
    roomies = group_obj.Group(names=["ra", "b", "re", "m", "j"])
    # Michael owes Ray $56
    roomies.store_new_transaction("ra", invlvd=["m"], total=56,
            comment="Michael still owes Ray $56 from other")
    # Ray spent $115.63 on groceries and a group dinner
    roomies.store_new_transaction("ra", invlvd="all",
            total=115.63, comment="Ray paid $12.82 for groceries"
            + " and $102.81 for Mellow Mushroom")
    # Jack spent $77 on groceries
    roomies.store_new_transaction("j", invlvd="all", total=77,
            comment="Jack paid $77 on groceries")
    # Jack bought dinner for Ray, Reid, Michael, ~$15 each
    roomies.store_new_transaction("j", invlvd=["ra", "m", "re", "j"],
            total=15*4, comment="Approximate transaction: "+
            "Jack bought dinner for us at Vintner")
    for transaction in roomies.transactions:
        print transaction
    roomies.simplify()
