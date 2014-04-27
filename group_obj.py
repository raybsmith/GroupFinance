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
            print "\n\ncomment:", comment, "\n\n"
            raise Exception("payer(s) must be a string or dictionary")
        if split and type(split) != dict:
            print "\n\ncomment:", comment, "\n\n"
            raise Exception("split must be a dictionary")
        if (split and invlvd) or (not split and not invlvd):
            print "\n\ncomment:", comment, "\n\n"
            raise Exception("must specify EITHER split or list of involved")
        if invlvd and type(invlvd) not in [str, list]:
            print "\n\ncomment:", comment, "\n\n"
            raise Exception("invlvd must either  be 'all' or list of names")
        # Basic input checks for total transaction amount
        if type(payers) == dict:
            payed_total = sum(payers.values())
            if total and abs(payed_total - total) > 1e-3:
                print "\n\ncomment:", comment, "\n\n"
                raise Exception("Payed total doesn't match transaction total")
            total = payed_total
            if split and abs(payed_total - sum(split.values())) > 1e-3:
                print "\n\ncomment:", comment, "\n\n"
                raise Exception("Payed total doesn't match split total")
        if split:
            split_total = sum(split.values())
            if total and abs(split_total - total) > 1e-3:
                print "\n\ncomment:", comment, "\n\n"
                raise Exception("Split total doesn't match transaction total")
            total = split_total
        if not total:
            print "\n\ncomment:", comment, "\n\n"
            raise Exception("Total amount must be specified somehow!")

        # First deal with the payer and make it a dictionary of
        # payers.
        if type(payers) == str:
            payers = {payers : total}
        # Check payers to make sure they're actually people in
        # the group
        for payer in payers.iterkeys():
            if payer not in self.names:
                print "group names:", self.names
                print "payer:", payer
                print "comment:", comment
                raise Exception("The above transaction involves" +
                        " payer(s) who aren't in the group")

        # Now if a full split was given, store it.
        if split:
            # Run a check to make sure they're all actually
            # people in the group
            for person in split.iterkeys():
                if person not in self.names:
                    print "group names:", self.names
                    print "split:", split
                    print "comment:", comment
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
        for person in split.iterkeys():
            if person not in self.names:
                print "group names:", self.names
                print "split:", split
                print "comment:", comment
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

    def add_transaction(self, payers, split):
        """
        Add a transaction to the current paymat -- note that the
        payers are owed by the split members (which may include
        the payers).
        * payers -- dict {str:float} -- dictionary of payers,
            amounts.
        * split -- dict {str:float} -- the people involved in the
            transaction, names, amounts.
        """
        # Figure out how much every person in the party owes/is
        # owed for this transaction.
        ind_contrs = np.zeros(self.N)
        for name in self.names:
            name_ind = self.indices[name]
            if name in payers.keys():
                ind_contrs[name_ind] += payers[name]
            if name in split.keys():
                ind_contrs[name_ind] -= split[name]
        # Indices of those owed and those owing.
        owed_inds = np.nonzero(ind_contrs > 0)
        owing_inds = np.nonzero(ind_contrs < 0)
        # Sanity check. Total owed should be neg of total owing:
        total_owed = sum(ind_contrs[owed_inds])
        total_owing = sum(ind_contrs[owing_inds])
        if abs(total_owed + total_owing) > 1e-3:
            print "Payers:", payers
            print "Split:", split
            raise Exception("Something wrong with transaction.")
        # Figure out the ratios in which the people who are owed
        # should be paid.
        owed_ratios = np.zeros(self.N)
        for owed in owed_inds:
            owed_ratios[owed] = ind_contrs[owed]/float(total_owed)
        # Sanity check. Total owed ratios should sum to one.
        if abs(sum(owed_ratios) - 1) > 1e-3:
            print "Error info:", sum(owed_ratios)
            print "Payers:", payers
            print "Split:", split
            raise Exception("Error in transaction assignment.")
        # Now, assign transactions to a payment matrix such that
        # everyone will be square from this transaction.
        for owing in owing_inds:
            debt = -ind_contrs[owing]
            for owed in owed_inds:
                self.paymat[owing, owed] += debt*owed_ratios[owed]
        return

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
        # Set up numpy printing options
        np.set_printoptions(precision=3, suppress=True)
        # First, generate an unsimplified payment matrix from the
        # list of transactions.
        # First, make the matrix to be filled in.
        self.paymat = np.array( np.zeros((self.N,self.N)) )
        # Populate it with the saved transactions.
        for transaction in self.transactions:
            self.add_transaction(
                    transaction["payers"],
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

        # Get rid of multi-multi-payments (A and B both pay C
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
                            adj = self.paymat[debtor2, shared1]
                            self.paymat[debtor1, shared1] += adj
                            self.paymat[debtor1, shared2] -= adj
                            self.paymat[debtor2, shared1] = 0
                            self.paymat[debtor2, shared2] += adj
                        elif min_flag == 3:
                            adj = self.paymat[debtor2, shared2]
                            self.paymat[debtor1, shared1] -= adj
                            self.paymat[debtor1, shared2] += adj
                            self.paymat[debtor2, shared1] += adj
                            self.paymat[debtor2, shared2] = 0
            count += 1
        if count == max_count:
            # Do we want to do anything here?
            pass

        # Systematically go through and eliminate all chains.
        # Consider each debtor.
        for debtor in xrange(self.N):
            # Look at the people they may owe money to -- their
            # creditors.
            for creditor in xrange(self.N):
                # If debtor owes creditor and creditor owes other
                # people money.
                # List of people creditor could owe to.
                creditors_creditors = [i for i in xrange(self.N)
                        if i != creditor]
                creditors_total_debt = np.sum(self.paymat[creditor,
                    creditors_creditors])
                if (self.paymat[debtor, creditor]
                        and creditors_total_debt > 0):
                    debt1 = self.paymat[debtor, creditor]
                    # If the creditor owes (in total) less than
                    # the debtor owes him/her, cancel all the
                    # creditor's debt to his/her creditors.
                    if creditors_total_debt < debt1:
                        # The debtor will owe the creditor the
                        # original amount less the sum of the
                        # creditor's debts.
                        self.paymat[debtor, creditor] \
                                -= creditors_total_debt
                        # Have debtor pick up the creditor's
                        # debts.
                        for creditors_creditor in \
                                creditors_creditors:
                            # Debter picks up creditor's debt.
                            self.paymat[debtor, creditors_creditor] += \
                                    self.paymat[creditor, creditors_creditor]
                            # Creditor is no longer in debt.
                            self.paymat[creditor, creditors_creditor] = 0
                    # Else, cancel as much as can be canceled,
                    # because the creditor owes more than the
                    # debtor owes the creditor.
                    else:
                        creditors_creditor = 0
                        # Don't deal with lingering
                        # self-payments.
                        if creditors_creditor == creditor:
                            creditors_creditor += 1
                        while self.paymat[debtor, creditor] > 0:
                            # Useful to have these abbreviated:
                            debt1 = self.paymat[debtor, creditor]
                            debt2 = self.paymat[creditor,
                                    creditors_creditor]
                            # If the amount owed to creditor is
                            # more than creditor's current debt in
                            # consideration, have the debtor absorb
                            # the whole thing.
                            if debt1 > debt2:
                                # Debter owes creditor less.
                                self.paymat[debtor, creditor] -= debt2
                                # Debter picks up creditor's debt.
                                self.paymat[debtor,
                                        creditors_creditor] += debt2
                                # Creditor is no longer in debt.
                                self.paymat[creditor,
                                        creditors_creditor] = 0
                            # Otherwise, debtor will just pick up
                            # part of it.
                            else:
                                # Creditor owes less by amount debtor
                                # owed creditor.
                                self.paymat[creditor,
                                        creditors_creditor] -= debt1
                                # Debter picks up as much
                                # of creditor's debt as he owed
                                # creditor.
                                self.paymat[debtor,
                                        creditors_creditor] += debt1
                                # Debter no longer owes creditor.
                                self.paymat[debtor, creditor] = 0
                            # Increment the person we're looking at
                            # creditor owing.
                            creditors_creditor += 1

        # Eliminate self-pays
        for person in xrange(self.N):
            self.paymat[person, person] = 0

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
        # We'll accept a change of less than a penny or so in
        # total balance for an individual.
        tol = 1e-3
        for person in xrange(self.N):
            if abs(balances_init[person] - \
                    balances_final[person]) > tol:
                raise Exception("Simplify() script changed the " +
                    "individual balances. There's a problem " +
                    "with the algorithm.")
        for debtor in xrange(self.N):
            for creditor in xrange(self.N):
                debt = self.paymat[debtor, creditor]
                if debt:
                    # Find names corresponding to debtor,
                    # creditor indices.
                    for (name, indx) in self.indices.iteritems():
                        if indx == debtor:
                            dname = name
                        elif indx == creditor:
                            cname = name
                    print ("{debtor_name} owes {creditor_name} "
                            "${debtval:.2f}").format(debtor_name=dname,
                            creditor_name=cname, debtval=debt)

