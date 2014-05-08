class Group:
    """
    This defines a class that will keep track of a group's
    finances, easily modifiable based on who spends how much with
    any given subset of the group. It has methods to add
    expenses, figure out simple overall-repayment plans, etc.
    """

    def __init__(self, names):
        """
        Set up the basic things we'll need to keep track of.
        * names -- array,strings -- the names of the people in
            the group.
        """
        # Names should be an array of strings.
        self.names = names
        # Store a list of transactions. This will be a list of
        # dictionaries.
        self.transactions = []

    def store_new_transaction(self, payers, split=None, invlvd=None,
            total=None, comment="None"):
        """
        Stores a new transaction in which the payer(s) purchased
        something for a group of people.
        * payers -- either a name (string) or a dictionary of
            names/amounts of people who paid.
        * split -- optional dictionary -- list of people who owe
            for the transaction and how much they owe.
        * invlvd -- list,strings -- if split not defined, then
            assume an even split between all these people
            involved.
        * total -- float -- if split not defined, the total for
            the transaction to be split evenly.
        """

        # Basic input checks for types, sufficiency
        if type(payers) not in [dict, str]:
            print("\n\ncomment:", comment, "\n\n")
            raise Exception("payer(s) must be a string or dictionary")
        if split and type(split) != dict:
            print("\n\ncomment:", comment, "\n\n")
            raise Exception("split must be a dictionary")
        if (split and invlvd) or (not split and not invlvd):
            print("\n\ncomment:", comment, "\n\n")
            raise Exception("must specify EITHER split or list of involved")
        if invlvd and type(invlvd) not in [str, list]:
            print("\n\ncomment:", comment, "\n\n")
            raise Exception("invlvd must either  be 'all' or list of names")
        # Basic input checks for total transaction amount
        if type(payers) == dict:
            paid_total = sum(payers.values())
            if total and abs(paid_total - total) > 1e-3:
                print("\n\ncomment:", comment, "\n\n")
                raise Exception("Paid total doesn't match transaction total")
            total = paid_total
            if split and abs(paid_total - sum(split.values())) > 1e-3:
                print("\n\ncomment:", comment, "\n\n")
                raise Exception("Paid total doesn't match split total")
        if split:
            split_total = sum(split.values())
            if total and abs(split_total - total) > 1e-3:
                print("\n\ncomment:", comment, "\n\n")
                raise Exception("Split total doesn't match transaction total")
            total = split_total
        if not total:
            print("\n\ncomment:", comment, "\n\n")
            raise Exception("Total amount must be specified somehow!")

        # First deal with the payer and make it a dictionary of
        # payers.
        if type(payers) == str:
            payers = {payers : total}
        # Check payers to make sure they're actually people in
        # the group
        for payer in payers:
            if payer not in self.names:
                print("group names:", self.names)
                print("payer:", payer)
                print("comment:", comment)
                raise Exception("The above transaction involves" +
                        " payer(s) who aren't in the group")

        # Now if a full split was given, store it.
        if split:
            # Run a check to make sure they're all actually
            # people in the group
            for person in split:
                if person not in self.names:
                    print("group names:", self.names)
                    print("split:", split)
                    print("comment:", comment)
                    raise Exception("The above transaction involves"
                            +" people in the split who aren't in"
                            +" the group")
            # Now, store the transaction and be done with it.
            new_transaction = {
                    "payers" : payers,
                    "split" : split,
                    "comment" : comment}
            self.transactions.append(new_transaction)
            return

        # It's not a defined split. In that case we need both an
        # involved list and a total.
        # Convert a couple of accepted "involved" shorthand
        # notations to lists of names.
        if invlvd == "all":
            invlvd = self.names
        elif invlvd == "all others":
            invlvd = [name for name in self.names if name not in
                    payers.keys()]
        # We have all the information we need to make an even
        # split, denoted by the fact that we were given a list
        # of involved people and a transaction total.
        # Note that if the payers were involved, they will simply
        # end up owing themselves which works out fine.
        debt_per_person = total/float(len(invlvd))
        # Form the split -- that's how we'll store it.
        split = {}
        for person in invlvd:
            split[person] = debt_per_person
        # Run a check to make sure they're all actually
        # people in the group
        for person in split:
            if person not in self.names:
                print("group names:", self.names)
                print("split:", split)
                print("comment:", comment)
                raise Exception("The above transaction involves"
                        +" people in the split who aren't in"
                        +" the group")
        new_transaction = {
                "payers" : payers,
                "split" : split,
                "comment" : comment}
        self.transactions.append(new_transaction)
        return

    def get_persons_total_debt(self, name):
        """
        Returns the total debt a person has in the group. Returns
        a positive value if the person net owes money and a
        negative value if they're net owed money.
        """
        total_debt = 0
        # Loop through all the transactions. Add debt where the
        # person is in the split, remove it where the person made
        # a payment.
        for transaction in self.transactions:
            if name in transaction["payers"].keys():
                total_debt -= transaction["payers"][name]
            if name in transaction["split"].keys():
                total_debt += transaction["split"][name]
        return total_debt

    def simplify(self, bank=None):
        """
        This function takes the current list of transactions and
        reduces them to a simplified set of payments to be made to
        square the group. Generally for N people in a group, this will
        reduce to N-1 (or fewer) balancing transactions.
        """
        # Make a list of total payments debts and credits per
        # person initially. This will verify the simplification
        # process didn't actually change anything.
        balances = []
        baldict = {}
        for name in self.names:
            debt = self.get_persons_total_debt(name)
            balances.append((name, -debt))
            baldict[name] = -debt
        if bank:
            if bank not in baldict:
                raise Exception("Bank person must be in group")
            for person in self.names:
                if person != bank:
                    if baldict[person] > 0:
                        print (("{bank} owes {creditor} "
                            "${val:.2f}").format(bank=bank,
                                creditor=person, val=baldict[person]))
                    else:
                        print (("{debtor} owes {bank} "
                            "${val:.2f}").format(bank=bank,
                                debtor=person, val=abs(baldict[person])))
        else:
            balances.sort(key=lambda person: person[1], reverse=True)
            names_sorted = [balances[i][0] for i in range(len(balances))]
            balances_sorted = [balances[i][1] for i in range(len(balances))]
            if abs(sum(balances_sorted)) > 1e-4:
                print(sum(balances_sorted))
                raise Exception("Waat? credits/debts don't balance!")
            for creditor_indx, name in enumerate(names_sorted):
                creditor = names_sorted[creditor_indx]
                # Start from person issuing most credit
                while abs(balances_sorted[creditor_indx]) > 1e-3:
                    # Work our way up from the back of line to find the
                    # last person still in debt
                    tmplist = [j for
                        j, x in enumerate(reversed(balances_sorted))
                        if abs(x) > 1e-3]
                    debtor_indx = len(self.names)  - next((j for
                        j, x in enumerate(reversed(balances_sorted))
                        if abs(x) > 1e-3), None) - 1
                    debtor = names_sorted[debtor_indx]
                    creditor_bal = balances_sorted[creditor_indx]
                    debtor_bal = balances_sorted[debtor_indx]
                    transvalue = min(creditor_bal, abs(debtor_bal))
                    balances_sorted[creditor_indx] -= transvalue
                    balances_sorted[debtor_indx] += transvalue
                    print (("{debtor_name} owes {creditor_name} "
                            "${debtval:.2f}").format(debtor_name=debtor,
                            creditor_name=creditor, debtval=transvalue))
