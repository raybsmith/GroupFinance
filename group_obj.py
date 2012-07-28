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
        self.paymat = np.array( np.zeros((self.N,self.N)) )
        # Store a list of transactions. This will be a dictionary of 
        self.transactions = []

    def store_new_transaction(self, payer, others, total, split):
        new_transaction = {
                "payer" : payer,
                "others" : others,
                "total" : total,
                "split" : split }
        self.transactions.append(new_transaction)

    def add_transaction(self, payer, others, total, split):
        """
        Add a transaction to the current paymat -- note that the
        payer is owed by the others in the group.
        * Payee -- string -- name of person that payed for this
            transaction
        * others -- string/array, strings -- if "ALL", then everyone is
            involved, otherwise, names of people involved
        * total -- float -- total amount
        * split -- string/array, floats -- if "even", split costs
            evenly, if an array of floats, then the array should
            sum to the total and be an array of how much each
            person owes (zeros for people not involved).
        """
        # Numerical indices for the payer and others
        payer = self.indices[payer]
        if others == "ALL":
            # Everyone's involved in this transaction
            others = self.indices.values()
        else:
            # Divide only among the people involved
            others = [self.indices[other] for other in others]
        # Vector of the debts
        debts = np.array( np.zeros((self.N)) )
        # If this bill is split evenly among those involved
        if split == "even":
            per_person = float(total)/(len(others) + 1)
            for person in others:
                debts[person] = per_person
        # If this bill is split unevenly
        else:
            for person in others:
                debts[person] = split[person]
        # Adjust the payment array.
        # The debt array represents debts owed to the payer.
        self.paymat[:, payer] += debts

    def add_person(self, new_name, old_debt = None):
        """
        Adds someone to the payment array. 
        * old_debt -- array,floats -- the amounts this person owes
            to the others
        """
        # TODO -- make add/remove person carry out a simplify,
        # regenerate the list of transactions from the simplified
        # paymat, and thus maintain all the "data" in
        # self.transactions.
        # Optional -- functionality to add/remove multiple people
        # at the same time?

        # Extra person -- add to the total.
        self.N += 1
        # Add this person to the list of people-indices
        # dictionary.
        self.indices[new_name] = self.N
        # This is the stored numerical index for the new person.
        new_name = self.N
        # Make space in paymat.
        self.paymat = np.hstack([self.paymat,
            np.zeros((self.N, 1))])
        self.paymat = np.vstack([self.paymat,
            np.zeros((1, self.N+1))])
        # If they had outstanding debts coming in, add those.
        if old_debt is not None:
            self.paymat[new_name, :] += old_debt

    def remove_person(self, leaving, debt_forgiven, debt_even,
            debt_absorber=None):
        """
        Removes a person from the payment array.
        * leaving -- string -- the name of the person to be removed.
        * debt_forgiven -- logical -- True to forgive debt this
            person owed, False otherwise.
        * debt_even -- logical -- True to distribute this person's
            debt evenly across the group, False otherwise.
        * debt_absorber -- string -- name of the person to absorb
            the debt of the person leaving.
        """
        # Make sure we have something to do.
        if not debt_forgiven and not debt_even \
                and not debt_absorber:
            raise Exception("Can't remove someone without " +
                    "instructions on how to do so.")
        # Numerical indices.
        # Get the person's number.
        leavingnum = self.indices[leaving]
        # Remove that person from the indices
        del self.indices[leaving]
        leaving = leavingnum
        # Index of the person to absorb the debt.
        if debt_absorber is not None:
            debt_absorber = self.indices[debt_absorber]
        # We have one fewer person.
        self.N -= 1
        # If the debt from this person is simply being forgiven.
        if debt_forgiven:
            # We'll just end up deleting these entries from the
            # paymat.
            pass
        # If the debt is being divided evenly.
        elif debt_even:
            # How much leaving person owed to each person.
            debts = self.paymat[leaving, :]
            # Divide this up evenly by the remaining people
            added_to_each = debts/self.N
            for person in xrange(self.N):
                self.paymat[person, :] += added_to_each
        # If one person is absorbing the debt.
        else:
            debts = self.paymat[leaving, :]
            self.paymat[debt_absorber, :] += debts
        # In any case, they no longer need entries in paymat.
        np.delete(self.paymat, leaving, axis=0)
        np.delete(self.paymat, leaving, axis=1)
        # TODO -- Option for them to simply buy out. Run a
        # simplify (or not), have them pay their entire debt to
        # a given person (anyone), then fix up the transactions
        # accordingly.

#    def generate_paymat(self):
#        """
#        Generate a paymatrix with the current transaction
#        list.
#        """
#        for transaction in self.transactions
#            self.add_transaction(
#                    transaction["payer"],
#                    transaction["others"],
#                    transaction["total"],
#                    transaction["split"])

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

#        # First, generate an unsimplified payment matrix from the
#        # list of transactions.
#        for transaction in self.transactions:
#            self.add_transaction(
#                    transaction["payer"],
#                    transaction["others"],
#                    transaction["total"],
#                    transaction["split"])

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

