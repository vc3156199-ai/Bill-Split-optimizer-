from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        names = request.form.getlist("name")
        amounts = request.form.getlist("amount")

        expenses = []
        total = 0

        for name, amount in zip(names, amounts):
            if name and amount:
                amount = float(amount)
                expenses.append({
                    "name": name,
                    "amount": amount
                })
                total += amount

        if expenses:
            share = total / len(expenses)

            for person in expenses:
                person["balance"] = person["amount"] - share

            result = {
                "expenses": expenses,
                "total": total,
                "share": share
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
