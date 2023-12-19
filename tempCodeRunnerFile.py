from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract data from form
        margin_percentage = float(request.form.get('margin_percentage'))
        hectares = int(request.form.get('hectares'))
        fields = int(request.form.get('fields'))
        pack_type = request.form.get('pack_type')
        years = int(request.form.get('years'))

        # Calculate prices and other details
        prices = calculate_prices(hectares, fields, pack_type, years)
        grower_price = prices['total_price']
        reseller_price = grower_price * (1 + margin_percentage / 100)
        days_required = calculate_days_required(fields, hectares)

        return render_template('result.html', grower_price=grower_price, reseller_price=reseller_price, days_required=days_required)

    return render_template('index.html')

def calculate_prices(hectares, fields, pack_type, years):
    pack_prices = {
        'PACK-STANDARD': 34,
        'PACK-CARBONE': 49,
        'PACK-PREMIUM': 63,
        'PACK-PREMIUM-CARBONE': 70
    }
    base_price_per_hectare = pack_prices[pack_type]

    # Cost for hectares and fields
    initial_cost = (base_price_per_hectare * hectares) + (250 * fields)

    # Subscription cost
    subscription_cost = 9 * hectares * min(years, 3) + 3 * hectares * max(years - 3, 0)

    total_price = initial_cost + subscription_cost

    return {'total_price': total_price}


def calculate_days_required(fields, hectares):
    max_hectares_per_day = 40
    max_charge_per_day = 1000
    days_by_hectares = hectares / max_hectares_per_day
    days_by_charge = fields * 250 / max_charge_per_day
    days_required = max(days_by_hectares, days_by_charge)
    return round(days_required, 2)

if __name__ == '__main__':
    app.run(debug=True)
