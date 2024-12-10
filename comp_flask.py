from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mobilepricetracker",
    port="3306"
)

# Default route for homepage
@app.route('/', methods=['GET'])
def index():
    return render_template('comp.html')

# Route to search for mobiles
@app.route('/search_mobiles', methods=['POST'])
def search_mobiles():
    data = request.get_json()
    search_query = data.get('search_query', '').lower()

    cursor = conn.cursor(dictionary=True)
    sql_query = "SELECT title, price FROM Mobiles WHERE title LIKE %s"
    cursor.execute(sql_query, ('%' + search_query + '%',))
    mobile_data = cursor.fetchall()
    cursor.close()

    # Format the data for the dropdown
    mobiles = []
    for mobile in mobile_data:
        mobiles.append({
            'name': mobile['title'],
            'price': mobile['price']
        })

    return jsonify({'mobiles': mobiles})

# Route to compare selected mobiles
@app.route('/compare_mobiles', methods=['POST'])
def compare_mobiles():
    data = request.get_json()
    mobile1_title = data.get('mobile1')
    mobile2_title = data.get('mobile2')

    cursor = conn.cursor(dictionary=True)
    sql_query = """
        SELECT title, redirect_link, platform_name, price, rating, delivery_time, image_url, new_refurbished 
        FROM Mobiles 
        WHERE title IN (%s, %s)
    """
    cursor.execute(sql_query, (mobile1_title, mobile2_title))
    comparison_data = cursor.fetchall()
    cursor.close()

    # Format the data for comparison
    comparison = {}
    for mobile in comparison_data:
        comparison[mobile['title']] = {
            'price': mobile['price'],
            'platform': mobile['platform_name'],
            'link': mobile['redirect_link'],
            'image': mobile['image_url'],
            'condition': mobile['new_refurbished'],
            'rating': mobile['rating'],
            'delivery_time': mobile['delivery_time']
        }

    return jsonify({
        'mobile1': comparison.get(mobile1_title),
        'mobile2': comparison.get(mobile2_title)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5003)

