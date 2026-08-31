from flask import Flask, render_template, request
from bill_split import BillSplitter, valid_name, valid_amount, save_expense

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():

    try:
        people = [
            p.strip()
            for p in request.form["people"].split(",")
            if valid_name(p.strip())
        ]

        if len(people) < 2:
            return render_template(
                "index.html",
                error="Enter at least 2 valid names."
            )

        descriptions = request.form.getlist("description")
        payers = request.form.getlist("payer")
        amounts = request.form.getlist("amount")

        expenses = []

        for i in range(len(payers)):

            if payers[i] in people and valid_amount(amounts[i]):

                expense = (
                    payers[i],
                    descriptions[i],
                    float(amounts[i])
                )

                expenses.append(expense)
                save_expense(expense)

        if not expenses:
            return render_template(
                "index.html",
                error="Enter at least one valid expense."
            )

        bill = BillSplitter(people, expenses)

        return render_template(
            "index.html",
            people=people,
            total=round(sum(bill.paid.values()), 2),
            share=round(bill.share(), 2),
            summary=bill.summary(),
            settlements=bill.settlements()
        )

    except Exception:
        return render_template(
            "index.html",
            error="Please check your input."
        )


if __name__ == "__main__":
    app.run(debug=True)
