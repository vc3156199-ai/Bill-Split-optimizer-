from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def calculate_total(amounts):
    total = 0

    for amount in amounts:
        total = total + amount

    return total


def calculate_balances(names, amounts):
    total = calculate_total(amounts)

    if len(names) == 0:
        return 0, 0, {}

    fair_share = total / len(names)

    balances = {}

    for i in range(len(names)):
        balances[names[i]] = amounts[i] - fair_share

    return total, fair_share, balances


def optimize_split(balances):

    debtors = []
    creditors = []

    for name in balances:

        if balances[name] < -0.01:
            debtors.append([name, -balances[name]])

        elif balances[name] > 0.01:
            creditors.append([name, balances[name]])

    settlements = []

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):

        debtor = debtors[i]
        creditor = creditors[j]

        amount = min(debtor[1], creditor[1])

        settlements.append(
            debtor[0]
            + " pays Rs. "
            + str(round(amount, 2))
            + " to "
            + creditor[0]
        )

        debtor[1] = debtor[1] - amount
        creditor[1] = creditor[1] - amount

        if debtor[1] <= 0.01:
            i = i + 1

        if creditor[1] <= 0.01:
            j = j + 1

    return settlements


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        names = [
            name.strip()
            for name in request.form.getlist("name")
            if name.strip()
        ]

        amounts = []

        for value in request.form.getlist("amount"):

            try:
                amounts.append(float(value))

            except ValueError:
                return redirect("/")

        if len(names) == 0 or len(names) != len(amounts):
            return redirect("/")

        total, fair_share, balances = calculate_balances(
            names,
            amounts
        )

        settlements = optimize_split(balances)

        return render_template(
            "index.html",
            total=total,
            fair_share=fair_share,
            balances=balances,
            settlements=settlements
        )

    # Default values for the first page load
    return render_template(
        "index.html",
        total=0,
        fair_share=0,
        balances={},
        settlements=[]
    )


if __name__ == "__main__":
    app.run(debug=True)
        elif balances[name] > 0:
            creditors.append([name, balances[name]])

    settlements = []

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):

        debtor = debtors[i]
        creditor = creditors[j]

        amount = min(debtor[1], creditor[1])

        settlements.append(
            debtor[0] + " pays Rs. " +
            str(round(amount, 2)) +
            " to " + creditor[0]
        )

        debtor[1] = debtor[1] - amount
        creditor[1] = creditor[1] - amount

        if debtor[1] <= 0.01:
            i = i + 1

        if creditor[1] <= 0.01:
            j = j + 1

    return settlements


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        names = request.form.getlist("name")

        amounts = []

        for value in request.form.getlist("amount"):

            try:
                amounts.append(float(value))

            except:
                return redirect("/")

        total, fair_share, balances = calculate_balances(
            names, amounts
        )

        settlements = optimize_split(balances)

        return render_template(
            "index.html",
            total=total,
            fair_share=fair_share,
            balances=balances,
            settlements=settlements
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
