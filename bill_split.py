import re


class BillSplitter:
    def __init__(self, people, expenses):
        self.people = people
        self.expenses = expenses
        self.paid = {p: 0 for p in people}

        for payer, description, amount in expenses:
            self.paid[payer] += amount

    def share(self):
        return sum(self.paid.values()) / len(self.people)

    def balance(self):
        s = self.share()
        return {p: round(self.paid[p] - s, 2) for p in self.people}

    def summary(self):
        b = self.balance()
        s = self.share()

        return [
            (p, round(self.paid[p], 2), round(s, 2), b[p],
             "Receive" if b[p] > 0 else "Pay" if b[p] < 0 else "Settled")
            for p in self.people
        ]

    def settlements(self):
        b = self.balance()

        debtors = [[p, -v] for p, v in b.items() if v < 0]
        creditors = [[p, v] for p, v in b.items() if v > 0]

        result = []
        i = j = 0

        while i < len(debtors) and j < len(creditors):
            amount = round(min(debtors[i][1], creditors[j][1]), 2)

            result.append(
                (debtors[i][0], creditors[j][0], amount)
            )

            debtors[i][1] -= amount
            creditors[j][1] -= amount

            if debtors[i][1] <= 0.01:
                i += 1

            if creditors[j][1] <= 0.01:
                j += 1

        return result


def valid_name(name):
    return bool(re.match(r"^[A-Za-z ]+$", name))


def valid_amount(amount):
    try:
        return float(amount) > 0
    except ValueError:
        return False


def save_expense(expense):
    with open("data/expenses.txt", "a") as f:
        f.write(" | ".join(map(str, expense)) + "\n")
