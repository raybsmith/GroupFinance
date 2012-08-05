import numpy as np

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
        for indx in xrange(self.N):
            self.indices[self.names[indx]] = indx
        # Store a list of transactions. This will be a dictionary of 
        self.transactions = []

    def store_new_transaction(self, payer, split, others=None,
            total=None, payer_incl=None):
        # Run some checks to make sure it's a sane transaction.
        if split != "even":
            # If we were given a total, that's
            # overspecification.
            if total is not None:
                raise Exception("We shouldn't have defined a split-" +
                        "vector and a total.")
        else:
            # If it's an even split, but we don't have
            # information about who's involved and the total
            # amount, we can't use it.
            if others is None or total is None or payer_incl is None:
                raise Exception("For an even split, we " +
                        "need the total, the others, " +
                        "and whether or not the payer " +
                        "was involved.")
        new_transaction = {
                "payer" : payer,
                "split" : split,
                "others" : others,
                "total" : total,
                "payer_incl" : payer_incl }
        self.transactions.append(new_transaction)

    def get_persons_transactions(self, name):
        person_debts = []
        person_assets = []
        for transaction_ind in xrange(len(self.transactions)):
            transaction = self.transactions[transaction_ind]
            # If the person payed, it's an asset; people owe
            # him/her money.
            if transaction["payer"] == name:
                person_assets.append(transaction_ind)
            # If the person was involved as an "other", they
            # "owe" for the transaction.
            elif name in transaction["others"]:
                person_debts.append(transaction_ind)
        return person_debts, person_assets

    def get_persons_total_debt(self, name):
        """
        Returns the total debt a person has in the group. Returns
        a positive value if the person net owes money and a
        negative value if they're net owed money.
        """
        
        person_debts, person_assets = \
                self.get_persons_transactions(name)
        total_debt = 0
        # First loop through all the transactions in which
        # they were they payer.
        for asset_ind in person_assets:
            transaction = self.transactions[asset_ind]
            # If it was an even split, we have the total.
            if split == "even":
                # If the payer was involved, they're not owed
                # the total.
                if transaction["payer_incl"]:
                    num_others = len(transaction["others"])
                    total_debt -= transaction["total"] * \
                            (num_others/(num_others + 1))
                # Otherwise, they're owed the whole amount.
                else:
                    total_debt -= transaction["total"]
            # It wasn't an even split. They're just owed the
            # sum of the split.
            else:
                total_debt -= sum(split)
        # Now all the ones in which they were involved but not
        # the payer.
        for debt_ind in person_debts:
            transaction = self.transactions[debt_ind]
            # If it's an even split and they were involved
            if split == "even":
                # Again, need to figure out if payer was
                # involved.
                num_others = len(transaction["others"])
                if transaction["payer_incl"]:
                    total_debt += transaction["total"] / \
                            (num_others + 1)
                # Otherwise, just the others were involved.
                else:
                    total_debt += transaction["total"] / \
                            num_others
            # It wasn't an even split. They just owe exactly
            # what split says they owe.
            else:
                name_ind = self.indices[name]
                total_debt += split[name_ind]
        return total_debt

    def add_person(self, new_name, old_debt=None):
        """
        Adds someone to the payment array. 
        * old_debt -- dict,str:float -- the names of people this
        * person owes and the amounts this person owes them.
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
        # have a negative total or split vector.
        if old_debt is not None:
            # The vector of how much the person owes people
            debts_vec = np.zeros((self.N))
            for (other, amount) in old_debt.items():
                # The index of the person the new person owes.
                other_ind = self.indices[other]
                # Setting the debt vector by index.
                split[other_ind] = old_debt[other]
            # Now that it's set up, store this as a transaction.
            self.store_new_transaction(
                    payer = new_name,
                    split = -debts_vec)

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
        # Get all the transactions involving the person.
        person_debts, person_assets = \
                self.get_persons_transactions(name)
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

    def add_transaction(self, payer, split, others=None,
            total=None, payer_incl=None):
        """
        Add a transaction to the current paymat -- note that the
        payer is owed by the others in the group.
        * Payee -- string -- name of person that payed for this
            transaction
        * split -- string/array, floats -- if "even", split costs
            evenly, if an array of floats, then the array should
            sum to the total and be an array of how much each
            person owes (zeros for people ).
        * others -- string/array, strings -- if "ALL", then everyone is
            involved, otherwise, names of people involved
        * total -- float -- total amount
        * payer_incl -- bool -- whether or not the payer was
            involved in this evenly divided transaction.
        """
        # Numerical index of the payer
        payer_ind = self.indices[payer_ind]
        # If we have a fully defined split, that's all we need.
        if split != "even":
            # We were simply given what people owe the payer. How
            # nice and easy.
            self.paymat[:, payer] += split
        # Otherwise, it's an even split among "others".
        else:
            # Numerical indices for the others
            if others == "ALL":
                # Everyone's involved in this transaction
                others_ind = self.indices.values()
            else:
                # Divide only among the people involved
                others_ind = [self.indices[other] for other in others]
            # Split the bill is split evenly among those involved
            # If the payer participated, they owe a smaller
            # amount.
            if payer_incl:
                per_person = float(total)/(len(others_ind) + 1)
            # Otherwise, they owe just among the others.
            else:
                per_person = float(total)/len(others_ind)
            for person_ind in others_ind:
                # Adjust the payment array so that each person in
                # the group now owes the payer the per_person
                # amount more.
                self.paymat[person_ind, payer] += per_person

    def generate_paymat(self):
        """
        Generate a paymatrix with the current transaction
        list.
        """
        # First, make the matrix to be filled in.
        self.paymat = np.array( np.zeros((self.N,self.N)) )
        # Populate it with the saved transactions.
        for transaction in self.transactions:
            self.add_transaction(
                    transaction["payer"],
                    transaction["others"],
                    transaction["total"],
                    transaction["split"])

    def simplify(self):
        """
        This function takes paymat and reduces it such that there
        are no 'double-owes' -- people owing each other and no
        'chain owes' -- people owing someone who owes someone
        else.
        It also will get rid of multiple people paying the same
        multiple people (e.g. John and Sue both pay Allen and
        George -- this can be reduced to three payments rather
        than four).
        """

        # First, generate an unsimplified payment matrix from the
        # list of transactions.
        for transaction in self.transactions:
            self.add_transaction(
                    transaction["payer"],
                    transaction["others"],
                    transaction["total"],
                    transaction["split"])

        # Make a list of total payments debts and credits per
        # person initially. This will verify the simplification
        # process didn't actually change anything.
        balances_init = np.array( np.zeros((self.N)) )
        for debtor in xrange(self.N):
            balances_init[debtor] -= \
                    np.sum(self.paymat[debtor, :])
        for creditor in xrange(self.N):
            balances_init[creditor] += \
                    np.sum(self.paymat[:, creditor])

        # Systematically go through and eliminate all chains.
        # Consider each debtor.
        for debtor in xrange(self.N):
            # Look at the people they may owe money to -- their
            # creditors.
            for creditor in xrange(self.N):
                # If debtor owes creditor and creditor owes other
                # people money.
                if self.paymat[debtor, creditor] \
                        and \
                        np.sum(self.paymat[creditor, :]) > 0:
                    debt1 = self.paymat[debtor, creditor]
                    # If the creditor owes (in total) less than
                    # the debtor owes him/her, cancel all the
                    # creditor's debt.
                    if np.sum(self.paymat[creditor, :]) < debt1:
                        # The debtor will owe the creditor the
                        # original amount
                        # less the sum of the creditor's debts.
                        self.paymat[debtor, creditor] \
                                -= np.sum(self.paymat[creditor, :])
                        # Have debtor pick up the creditor's
                        # debts.
                        for creditors_creditor in xrange(self.N):
                            debt2 = self.paymat[creditor,\
                                    creditors_creditor]
                            # Debter picks up creditor's debt.
                            self.paymat[debtor, creditors_creditor] += debt2
                            # Creditor is no longer in debt.
                            self.paymat[creditor, creditors_creditor] = 0
                    # Else, cancel as much as can be canceled.
                    else:
                        creditors_creditor = 0
                        while self.paymat[debtor, creditor] > 0:
                            # Useful to have these abbreviated:
                            debt1 = self.paymat[debtor, creditor]
                            debt2 = self.paymat[creditor,\
                                    creditors_creditor]
                            # If the amount owed to creditor is
                            # more than creditor's current debt in
                            # consideration, have the debtor absorb
                            # the whole thing.
                            if self.paymat[debtor, creditor] > debt2:
                                # Debter owes creditor less.
                                self.paymat[debtor, creditor] -= debt2
                                # Debter picks up creditor's debt.
                                self.paymat[debtor,\
                                        creditors_creditor] += debt2
                                # Creditor is no longer in debt.
                                self.paymat[creditor,\
                                        creditors_creditor] = 0
                            # Otherwise, debtor will just pick up
                            # part of it.
                            else:
                                # Creditor owes less by amount debtor
                                # owed creditor.
                                self.paymat[creditor,\
                                        creditors_creditor] -= debt1
                                # Debter picks up as much
                                # of creditor's debt as he owed
                                # creditor.
                                self.paymat[debtor,\
                                        creditors_creditor] += debt1
                                # Debter no longer owes creditor.
                                self.paymat[debtor, creditor] = 0
                            # Increment the person we're looking at
                            # creditor owing.
                            creditors_creditor += 1

        # Now get rid of multi-multi-payments (A and B both pay C
        # and D).
        multis_present = 1
        count = 1
        max_count = 100
        while multis_present and count < max_count:
            # Assume the previous loop took care of the last one.
            multis_present = 0
            for debtor1 in xrange(self.N):
                # This debtor's creditors.
                creditors1 = np.nonzero(self.paymat[debtor1, :])[0]
                # Check to see if this debtor shares 2 creditors with
                # any subsequent debtor. If so, then it can be
                # simplified.
                for debtor2 in xrange(self.N):
                    # Not concerned if debtor shares creditors
                    # with self.
                    if debtor2 == debtor1:
                        continue # with the next debtor
                    # This debtor's creditors.
                    creditors2 = np.nonzero(self.paymat[debtor2, :])[0]
                    # Generate a list of shared creditors?
                    shared = np.intersect1d(creditors1,
                            creditors2)
                    # If there are at least 2 shared.
                    if len(shared) >= 2:
                        # There are still multi's around.
                        multis_present = 1
                        # Deal with the first 2 shared creditors.
                        shared1 = shared[0]
                        shared2 = shared[1]
                        # Find the lowest debt in the 'rectangle'.
                        min_flag = np.argmin( np.array([
                                self.paymat[debtor1, shared1],
                                self.paymat[debtor1, shared2],
                                self.paymat[debtor2, shared1],
                                self.paymat[debtor2, shared2]]) )
#                        print "PRE-paymat:"
#                        print self.paymat
                        # Get rid of one of them
                        if min_flag == 0:
                            adj = self.paymat[debtor1, shared1]
                            self.paymat[debtor1, shared1] = 0
                            self.paymat[debtor1, shared2] += adj
                            self.paymat[debtor2, shared1] += adj
                            self.paymat[debtor2, shared2] -= adj
                        elif min_flag == 1:
                            adj = self.paymat[debtor1, shared2]
                            self.paymat[debtor1, shared1] += adj
                            self.paymat[debtor1, shared2] = 0
                            self.paymat[debtor2, shared1] -= adj
                            self.paymat[debtor2, shared2] += adj
                        elif min_flag == 2:
                            adj = self.paymat[debtor1, shared2]
                            self.paymat[debtor1, shared1] += adj
                            self.paymat[debtor1, shared2] -= adj
                            self.paymat[debtor2, shared1] = 0
                            self.paymat[debtor2, shared2] += adj
                        elif min_flag == 3:
                            adj = self.paymat[debtor1, shared2]
                            self.paymat[debtor1, shared1] -= adj
                            self.paymat[debtor1, shared2] += adj
                            self.paymat[debtor2, shared1] += adj
                            self.paymat[debtor2, shared2] = 0
#                        print "POST-paymat:"
#                        print self.paymat
            count += 1
        if count == max_count:
            print "Ahh, iteration-max!"

        # The final list of balances. A person's total received
        # payments - debts should be the same before and after
        # simplification.
        balances_final = np.array( np.zeros((self.N)) )
        for debtor in xrange(self.N):
            balances_final[debtor] -= \
                    np.sum(self.paymat[debtor, :])
        for creditor in xrange(self.N):
            balances_final[creditor] += \
                    np.sum(self.paymat[:, creditor])
        print "Initial / final personal balances [$]:"
        for person in self.names:
            balance_i = balances_init[self.indices[person]]
            balance_f = balances_final[self.indices[person]]
            print "%s:  %5.2f / %5.2f" %(person, balance_i, balance_f)
        # We'll accept a change of less than a penny or so in
        # total balance for an individual.
        tol = 1e-3
        for person in xrange(self.N):
            if abs(balances_init[person] - \
                    balances_final[person]) > tol:
                raise Exception("Simplify() script changed the " +
                    "individual balances. There's a problem " +
                    "with the algorithm.")

