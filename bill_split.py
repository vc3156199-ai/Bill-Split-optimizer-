<!DOCTYPE html>
<html>
<head>
    <title>Bill Split Optimizer</title>
    <link rel="stylesheet"
          href="{{ url_for('static', filename='style.css') }}">
</head>

<body>

<div class="container">

    <h1>💰 Bill Split Optimizer</h1>
    <p class="subtitle">Split your expenses easily</p>

    <div class="box">

        <h2>Add Expense</h2>

        <form method="POST">

            <div id="expenses">

                <div class="expense">
                    <input type="text"
                           name="name"
                           placeholder="Person name"
                           required>

                    <input type="number"
                           name="amount"
                           placeholder="Amount"
                           required>

                    <button type="button"
                            onclick="removeExpense(this)">
                        ✕
                    </button>
                </div>

            </div>

            <button type="button"
                    class="add"
                    onclick="addExpense()">
                + Add Expense
            </button>

            <button type="submit"
                    class="calculate">
                Calculate Split
            </button>

        </form>

    </div>


    {% if result %}

    <div class="summary">

        <div>
            <span>Total Bill</span>
            <b>₹{{ "%.2f"|format(result.total) }}</b>
        </div>

        <div>
            <span>People</span>
            <b>{{ result.expenses|length }}</b>
        </div>

        <div>
            <span>Each Person</span>
            <b>₹{{ "%.2f"|format(result.share) }}</b>
        </div>

    </div>


    <div class="box">

        <h2>Settlement</h2>

        <table>

            <tr>
                <th>Person</th>
                <th>Paid</th>
                <th>Balance</th>
            </tr>

            {% for person in result.expenses %}

            <tr>
                <td>{{ person.name }}</td>

                <td>
                    ₹{{ "%.2f"|format(person.amount) }}
                </td>

                <td>
                    {% if person.balance > 0 %}
                        <span class="receive">
                            Gets ₹{{ "%.2f"|format(person.balance) }}
                        </span>
                    {% elif person.balance < 0 %}
                        <span class="owe">
                            Pays ₹{{ "%.2f"|format(person.balance|abs) }}
                        </span>
                    {% else %}
                        Settled
                    {% endif %}
                </td>
            </tr>

            {% endfor %}

        </table>

    </div>

    {% endif %}

</div>


<script>

function addExpense() {

    let div = document.createElement("div");

    div.className = "expense";

    div.innerHTML = `
        <input type="text"
               name="name"
               placeholder="Person name"
               required>

        <input type="number"
               name="amount"
               placeholder="Amount"
               required>

        <button type="button"
                onclick="removeExpense(this)">
            ✕
        </button>
    `;

    document.getElementById("expenses").appendChild(div);
}


function removeExpense(button) {

    let rows = document.querySelectorAll(".expense");

    if (rows.length > 1) {
        button.parentElement.remove();
    }

}

</script>

</body>
</html>
