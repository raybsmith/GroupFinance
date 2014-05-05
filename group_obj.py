class Group:
    """
    This defines a class that will keep track of a group's
    finances, easily modifiable based on who spends how much with
    any given subset of the group. It has methods to add
    expenses, figure out simple overall-repayment plans, etc.
    The array is store as rows of people that owe to people in
    the columns. (eg if Joe corresponds to 2 and Jane to 3, then
    a 5.5 in array element (2,3) indicates that Joe owes $5.50 to
    Jane.)
    """

    def __init__(self, names):
        """
        Set up the basic things we'll need to keep track of.
        * names -- array,strings -- the names of the people in
            the group.
        """
        # Names should be an array of strings.
        self.names = names
        # How many people are we dealing with.
        self.N = len(self.names)
        if self.N < 2:
            raise Exception("Why use this for only one person?")
        self.indices = {}
        for indx in range(self.N):
            self.indices[self.names[indx]] = indx
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
            for person in split.iterkeys():
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

    def add_person(self, new_name, old_debt=None):
        """
        Adds someone to the payment array. 
        * new_name -- str -- the name of the person to add.
        * old_debt -- dict,str:float -- the names of people this
            person owes and the amounts this person owes them.
        """
        # Extra person -- add to the total.
        self.N += 1
        # Add this person to the list of people-indices
        # dictionary.
        self.indices[new_name] = self.N
        # This is the stored numerical index for the new person.
        new_ind = self.N
        # If they had outstanding debts coming in, add those as a
        # single transaction. This can be thought of as an
        # "inverse" transaction in that if it were a typical
        # transaction, they would have paid and "others" would
        # owe them, but here, they need to pay, so we'll just
        # have a negatives in our split vector.
        if old_debt is not None:
            split = {}
            for (name, amount) in old_debt.iteritems():
                split[name] = -amount
            # Now that it's set up, store this as a transaction.
            self.store_new_transaction(
                    payers = new_name,
                    split = split)

    def remove_person(self, leaving, debt_forgiven,
            debt_settled=None, debt_absorber=None):
        """
        Removes a person from the payment array.
        * leaving -- string -- the name of the person to be removed.
        * debt_forgiven -- logical -- True to forgive debt this
            person owed, False otherwise.
        //* debt_even -- logical -- True to distribute this person's
        //    debt evenly across the group, False otherwise.
        * debt_settled -- string -- supplied (evalutes to True) to
          indicate that the person is paying all his/her debts
          now to a particular person (string) who will then
          settle with the rest of the group at final
          simplification.
        * debt_absorber -- string -- name of the person to absorb
            the debt of the person leaving.
        """
        # XXX -- Fix with new payer/split transaction storage
        # method.
        # Make sure we have something to do.
        if not debt_forgiven and not debt_settled \
                and not debt_absorber:
            raise Exception("Can't remove someone without " +
                    "instructions on how to do so.")
        # Numerical indices.
        # Get the person's number.
        name = leaving
        name_ind = self.indices[name]
        # Remove that person from the indices
        del self.indices[name]
#        leaving = leavingnum
#        # Get all the transactions involving the person.
#        person_debts, person_assets = \
#                self.get_persons_transactions(name)
        # We have one fewer person.
        self.N -= 1
        # If the debt from this person is simply being forgiven.
        if debt_forgiven:
            # We'll delete entries where the person was the payer
            # ("assets")
            for asset_ind in person_assets:
                del self.transactions[asset_ind]
            # We'll set equal to zero the parts of transactions
            # where the the person was among the "others"
            # ("debts")
            for debt_ind in person_debts:
                self.transactions[debt_ind]["others"][name] = 0
        # The person is settling his/her debt now.
        elif debt_settled:
#            # Add a transaction that is the "average" inverse of
#            # all the person's current transactions. That is, if
#            # s/he owed $4 to A $4 and $6 to B, add one where A and
#            # B both owe him/her $5.
            # First, figure out how much the person owed in total.
            total_debt = self.get_persons_total_debt(name)
            # Add a transaction indicating that they paid that
            # much to some "bank" person. Note that if the total
            # debt was negative (they were actually net owed
            # money), this should still work fine.
            bank_person = debt_settled
            self.store_new_transaction(
                    payer = name,
                    split = "even",
                    others = bank_person,
                    total = total_debt,
                    payer_incl = False)
        # If one person is absorbing the debt.
        else:
            # Index of the person to absorb the debt.
            debt_absorber_ind = self.indices[debt_absorber]
            # We'll replace entries where the person was the
            # payer with the debt-absorber as the payer.
            for asset_ind in person_assets:
                self.transactions[asset_ind]["payer"] = \
                        debt_absorber
            # For entries where the person was among the
            # "others", we'll shift the leaving person's burdon
            # to the absorber in the same transaction.
            for debt_ind in person_debts:
                # How much the leaver owed
                leavers_debt = \
                        self.transactions[debt_ind]["others"][name]
                # Leaver now owes nothing on that transaction.
                self.transactions[debt_ind]["others"][name] = 0
                # And absorber picks up the tab.
                self.transactions[debt_ind]["others"][debt_absorber] \
                        += leavers_debt
        # In any case, they no longer need entries in paymat.
        np.delete(self.paymat, name, axis=0)
        np.delete(self.paymat, name, axis=1)

    def simplify(self):
        """
        This function makes a paymat and reduces it such that there
        are no 'double-owes' -- people owing each other and no
        'chain owes' -- people owing someone who owes someone
        else.
        It also will get rid of multiple people paying the same
        multiple people (e.g. John and Sue both pay Allen and
        George -- this can be reduced to three payments rather
        than four).
        """
        # Make a list of total payments debts and credits per
        # person initially. This will verify the simplification
        # process didn't actually change anything.
        balances = []
        for name in self.names:
            debt = self.get_persons_total_debt(name)
            balances.append((name, -debt))
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
                debtor_indx = self.N  - next((j for
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
