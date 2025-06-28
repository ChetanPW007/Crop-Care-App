from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from database import create_connection, create_user, verify_user  # Your helper file

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Decorator to check login status
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/crop-guides')
def crop_guides():
    crops = [
        {'id': 1, 'name': 'Wheat'},
        {'id': 2, 'name': 'Rice'},
        {'id': 3, 'name': 'Maize'},
        {'id': 4, 'name': 'Cotton'}
    ]

    guides = [
        {
            'id': 1,
            'title': 'Wheat Guide',
            'content': 'Wheat grows well in cool climate with loamy soil. Needs moderate water.',
            'price': '₹22–₹28/kg',
            'diseases': ['Rust', 'Mildew'],
            'tips': ['Use certified seeds', 'Avoid waterlogging'],
            'crop_id': 1,
            'image': 'wheat.jpg'
        },
        {
            'id': 2,
            'title': 'Rice Cultivation Tips',
            'content': 'Rice thrives in flooded fields and warm, humid conditions. Clayey soil is best suited for paddy.',
            'price': '₹30–₹40/kg',
            'diseases': ['Bacterial Leaf Blight', 'Blast', 'Sheath Rot'],
            'tips': [
                'Maintain 2–5 cm water depth during early growth.',
                'Apply nitrogen fertilizers in split doses.',
                'Remove weeds regularly to increase yield.'
            ],
            'crop_id': 2,
            'image': 'rice.jpg'
        },
        {
            'id': 3,
            'title': 'Maize Best Practices',
            'content': 'Maize prefers warm temperatures and well-drained, fertile soils rich in organic matter.',
            'price': '₹18–₹25/kg',
            'diseases': ['Downy Mildew', 'Leaf Blight', 'Rust'],
            'tips': [
                'Ensure proper spacing between plants.',
                'Use pest traps to manage stem borers.',
                'Irrigate during flowering and grain-filling stages.'
            ],
            'crop_id': 3,
            'image': 'maize.jpg'
        },
        {
            'id': 4,
            'title': 'Cotton Farming Guide',
            'content': 'Cotton requires warm weather and deep, well-drained black soil with good water retention.',
            'price': '₹55–₹65/kg (seed cotton)',
            'diseases': ['Wilt', 'Boll Rot', 'Leaf Curl Virus'],
            'tips': [
                'Avoid over-irrigation to prevent fungal infections.',
                'Apply potassium-rich fertilizers.',
                'Monitor for pest attacks, especially bollworms.'
            ],
            'crop_id': 4,
            'image': 'cotton.jpg'
        },
    {
    'id': 5,
    'title': 'Sugarcane Farming Guide',
    'content': 'Sugarcane grows best in tropical climates with plenty of sunlight and well-drained loamy soil. Requires high water but good drainage.',
    'price': '₹3000–₹3500/ton',
    'diseases': ['Red Rot', 'Smut', 'Wilt'],
    'tips': [
        'Ensure deep ploughing before planting.',
        'Irrigate regularly, especially during dry spells.',
        'Apply nitrogen and potassium-based fertilizers.'
    ],
    'crop_id': 5,
    'image': 'sugarcane.jpg'
},
{
    'id': 6,
    'title': 'Ginger Cultivation Tips',
    'content': 'Ginger prefers warm, humid climates with well-drained sandy loam soil rich in humus. Avoid water stagnation.',
    'price': '₹60–₹80/kg',
    'diseases': ['Rhizome Rot', 'Leaf Spot'],
    'tips': [
        'Use disease-free rhizomes for planting.',
        'Apply organic manure and neem cake.',
        'Ensure good shade and drainage.'
    ],
    'crop_id': 6,
    'image': 'ginger.webp'
},
{
    'id': 7,
    'title': 'Potato Farming Guide',
    'content': 'Potatoes grow best in cool climates with loose, well-drained soil. Avoid heavy clay or waterlogging.',
    'price': '₹10–₹20/kg',
    'diseases': ['Late Blight', 'Early Blight', 'Scab'],
    'tips': [
        'Use certified disease-free tubers.',
        'Apply adequate phosphorus and potassium.',
        'Practice crop rotation to reduce soil-borne diseases.'
    ],
    'crop_id': 7,
    'image': 'potato.webp'
},
{
    'id': 8,
    'title': 'Sunflower Growing Tips',
    'content': 'Sunflowers thrive in sunny conditions with well-drained soil. Ideal for oilseed production.',
    'price': '₹45–₹55/kg',
    'diseases': ['Downy Mildew', 'Rust', 'Wilt'],
    'tips': [
        'Sow seeds at proper depth and spacing.',
        'Avoid excess irrigation during flowering.',
        'Control weeds in early growth stages.'
    ],
    'crop_id': 8,
    'image': 'sunflower.webp'
},
{
    'id': 9,
    'title': 'Arecanut Cultivation Guide',
    'content': 'Arecanut palms grow well in hot, humid climates and red loamy soils. Commonly cultivated in coastal and Western Ghats regions.',
    'price': '₹400–₹600/kg (dry nuts)',
    'diseases': ['Koleroga', 'Yellow Leaf Disease'],
    'tips': [
        'Maintain regular irrigation in dry seasons.',
        'Apply lime and organic manure yearly.',
        'Prune diseased fronds regularly.'
    ],
    'crop_id': 9,
    'image': 'arecanut.jpeg'
}

    ]

    crop_id = request.args.get('crop_id', type=int)

    if crop_id:
        filtered_guides = [g for g in guides if g['crop_id'] == crop_id]
    else:
        filtered_guides = guides

    return render_template('guides.html', crops=crops, guides=filtered_guides)

@app.route('/guide/<int:guide_id>')
def guide_detail(guide_id):
    guides = [
        {
            'id': 1,
            'title': 'Wheat Guide',
            'content': 'Wheat grows well in cool climate with loamy soil. Needs moderate water.',
            'price': '₹22–₹28/kg',
            'diseases': ['Rust', 'Mildew'],
            'tips': ['Use certified seeds', 'Avoid waterlogging'],
            'crop_id': 1,
            'image': 'wheat.jpg'
        },
        {
            'id': 2,
            'title': 'Rice Cultivation Tips',
            'content': 'Rice thrives in flooded fields and warm, humid conditions. Clayey soil is best suited for paddy.',
            'price': '₹30–₹40/kg',
            'diseases': ['Bacterial Leaf Blight', 'Blast', 'Sheath Rot'],
            'tips': ['Maintain water depth', 'Apply nitrogen in splits', 'Weed regularly'],
            'crop_id': 2,
            'image': 'rice.jpg'
        },
        {
            'id': 3,
            'title': 'Maize Best Practices',
            'content': 'Maize prefers warm temperatures and well-drained, fertile soils rich in organic matter.',
            'price': '₹18–₹25/kg',
            'diseases': ['Downy Mildew', 'Leaf Blight', 'Rust'],
            'tips': ['Proper spacing', 'Use pest traps', 'Irrigate during flowering'],
            'crop_id': 3,
            'image': 'maize.jpg'
        },
        {
            'id': 4,
            'title': 'Cotton Farming Guide',
            'content': 'Cotton requires warm weather and deep, well-drained black soil with good water retention.',
            'price': '₹55–₹65/kg (seed cotton)',
            'diseases': ['Wilt', 'Boll Rot', 'Leaf Curl Virus'],
            'tips': ['Avoid over-irrigation', 'Use potassium-rich fertilizer', 'Watch for bollworms'],
            'crop_id': 4,
            'image': 'cotton.jpg'
        },
       
        {
    'id': 5,
    'title': 'Sugarcane Farming Guide',
    'content': 'Sugarcane grows best in tropical climates with well-drained, fertile loam or alluvial soil. It needs high water but good drainage.',
    'price': '₹3000–₹3500/ton',
    'diseases': ['Red Rot', 'Smut', 'Wilt'],
    'tips': ['Deep ploughing before planting', 'Timely irrigation', 'Apply nitrogen and potassium-based fertilizers'],
    'crop_id': 5,
    'image': 'sugarcane.jpg'
},
{
    'id': 6,
    'title': 'Ginger Cultivation Tips',
    'content': 'Ginger prefers warm, humid climates with well-drained sandy loam soil rich in humus. Avoid water stagnation.',
    'price': '₹60–₹80/kg',
    'diseases': ['Rhizome Rot', 'Leaf Spot'],
    'tips': ['Use disease-free rhizomes', 'Add organic manure', 'Ensure shade and drainage'],
    'crop_id': 6,
    'image': 'ginger.webp'
},
{
    'id': 7,
    'title': 'Potato Farming Guide',
    'content': 'Potatoes thrive in cool climates with loose, well-drained soil. Avoid clay-heavy or waterlogged areas.',
    'price': '₹10–₹20/kg',
    'diseases': ['Late Blight', 'Scab', 'Early Blight'],
    'tips': ['Use certified tubers', 'Ensure good drainage', 'Practice crop rotation'],
    'crop_id': 7,
    'image': 'potato.webp'
},
{
    'id': 8,
    'title': 'Sunflower Growing Tips',
    'content': 'Sunflowers grow best in full sunlight and fertile, well-drained soil. Ideal for oilseed cultivation.',
    'price': '₹45–₹55/kg',
    'diseases': ['Downy Mildew', 'Rust', 'Wilt'],
    'tips': ['Avoid water stagnation', 'Thin seedlings properly', 'Control early weeds'],
    'crop_id': 8,
    'image': 'sunflower.webp'
},
{
    'id': 9,
    'title': 'Arecanut Cultivation Guide',
    'content': 'Arecanut grows in humid, tropical regions with deep, well-drained red loamy soil. Popular in coastal India.',
    'price': '₹400–₹600/kg (dry nut)',
    'diseases': ['Koleroga', 'Yellow Leaf Disease'],
    'tips': ['Irrigate in summer', 'Apply lime annually', 'Prune affected fronds'],
    'crop_id': 9,
    'image': 'arecanut.jpeg'
}

    ]

    guide = next((g for g in guides if g['id'] == guide_id), None)
    if guide:
        return render_template('guide_detail.html', guide=guide)
    else:
        return "<h2>Guide not found</h2>", 404


@app.route('/solutions')
@login_required
def solutions():
    crops = [
        {'id': 1, 'name': 'Wheat', 'image': 'Wheat.jpg'},
        {'id': 2, 'name': 'Rice'},
        {'id': 3, 'name': 'Maize'},
        {'id': 4, 'name': 'Cotton'},
        {'id': 5, 'name': 'Sugarcane'},
        {'id': 6, 'name': 'Ginger'},
        {'id': 7, 'name': 'Arecanut'},
        {'id': 8, 'name': 'Sunflower'},
        {'id': 9, 'name': 'Potato'},
    ]

    problems = [
        {
            'id': 1,
            'crop_id': 1,
            'crop_name': 'Wheat',
            'problem': 'Rust disease',
            'solution': 'Spray recommended fungicides at early stages. Use rust-resistant wheat varieties.',
            'fertilizer': 'Apply balanced NPK (40:20:20) for healthy growth.',
            'images': ['WheatRust1.jpg', 'WheatRust2.jpg', 'WheatRust3.jpg', 'WheatRust4.jpg']
        },
        {
            'id': 2,
            'crop_id': 2,
            'crop_name': 'Rice',
            'problem': 'Leaf Blast disease',
            'solution': 'Apply protective fungicide sprays. Keep fields well-drained to avoid high humidity.',
            'fertilizer': 'Use Urea and DAP as basal and top dressing.',
            'images': ['ricedesease1.jpeg', 'ricedesease2.jpeg', 'ricedesease3.jpeg', 'riceD4.webp']
        },
        {
            'id': 3,
            'crop_id': 3,
            'crop_name': 'Maize',
            'problem': 'Gray leaf spot',
            'solution': 'Use fungicide like BAYER LAUDIS. Rotate crops and avoid dense planting.',
            'fertilizer': 'Apply NPK 120:60:40 kg/ha for best yield.',
            'images': ['corndesease1.jpg', 'corndesease2.jpg', 'corndesease3.jpg', 'corndesease4.jpg']
        },
        {
            'id': 4,
            'crop_id': 4,
            'crop_name': 'Cotton',
            'problem': 'Wilt, root rot, anthracnose, bacterial blight',
            'solution': 'Grow resistant cotton varieties. Maintain field hygiene and proper drainage.',
            'fertilizer': 'Use NPK 75:30:30 kg/ha with FYM.',
            'images': ['cottonD1.jpg', 'cottonD2.jpg', 'cottonD3.jpg', 'cottonD4.JPG']
        },
        {
            'id': 5,
            'crop_id': 5,
            'crop_name': 'Sugarcane',
            'problem': 'Rust disease',
            'solution': 'Remove affected leaves and burn them safely. Use rust-resistant cane varieties.',
            'fertilizer': 'Apply Nitrogen 150 kg/ha in split doses.',
            'images': ['sugarcaneD1.jpg', 'sugarcaneD2.jpg', 'sugarcaneD3.jpg', 'sugarcaneD4.jpg']
        },
        {
            'id': 6,
            'crop_id': 6,
            'crop_name': 'Ginger',
            'problem': 'Soft rot, bacterial wilt, leaf spot',
            'solution': 'Use well-drained soil and avoid water logging. Apply bio-fungicides regularly.',
            'fertilizer': 'Use FYM 25 tons/ha + NPK 75:50:50 kg/ha.',
            'images': ['gingerD1.jpg', 'gingerD2.jpg', 'gingerD3.jpg', 'gingerD4.jpg']
        },
        {
            'id': 7,
            'crop_id': 7,
            'crop_name': 'Arecanut',
            'problem': 'Mahali (fruit rot), Yellow Leaf Disease, Foot Rot',
            'solution': 'Improve drainage and remove infected nuts. Apply recommended fungicides timely.',
            'fertilizer': 'Apply 100g N, 40g P, 140g K per palm yearly.',
            'images': ['arecanutD1.jpg', 'arecanutD2.jpg', 'arecanutD3.jpg', 'arecanutD4.jpg']
        },
        {
            'id': 8,
            'crop_id': 8,
            'crop_name': 'Sunflower',
            'problem': 'Downy mildew, rust, stem canker, Sclerotinia wilt',
            'solution': 'Practice crop rotation and space plants well. Spray proper fungicides at early signs.',
            'fertilizer': 'Apply NPK 60:60:40 kg/ha with micronutrients.',
            'images': ['sunflowerD1.jpg', 'sunflowerD2.jpg', 'sunflowerD3.jpg', 'sunflowerD4.jpeg']
        },
        {
            'id': 9,
            'crop_id': 9,
            'crop_name': 'Potato',
            'problem': 'Late Blight, Early Blight, Black Scurf, Bacterial Wilt',
            'solution': 'Use certified seed and fungicide sprays. Remove infected plants immediately.',
            'fertilizer': 'Apply FYM + NPK 120:80:60 kg/ha in rows.',
            'images': ['potatoD1.jpg', 'potatoD2.jpg', 'potatoD3.jpg', 'potatoD4.jpg']
        }
    ]

    crop_id = request.args.get('crop_id', type=int)
    search_query = request.args.get('search_query', '').strip().lower()

    filtered_problems = problems

    if crop_id:
        filtered_problems = [p for p in filtered_problems if p['crop_id'] == crop_id]

    if search_query:
        filtered_problems = [
            p for p in filtered_problems
            if search_query in p['problem'].lower()
            or search_query in p['solution'].lower()
            or search_query in p['crop_name'].lower()
        ]

    return render_template('solutions.html', problems=filtered_problems, crops=crops)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            flash('Please fill out all fields.', 'warning')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'warning')
            return redirect(url_for('register'))

        conn = create_connection()
        user_id = create_user(conn, username, email, password)

        if user_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = create_connection()
        user = verify_user(conn, username, password)

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    conn = create_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if user is None:
        flash("User not found.", "danger")
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)


@app.route('/search')
@login_required
def search():
    query = request.args.get('query', '').strip().lower()

    # Example crop data with detailed info
    crop_data = [
        {
            'name': 'Wheat',
            'price': '₹2200 per quintal',
            'guide': 'Wheat requires moderate rainfall and well-drained loamy soil.',
            'image': 'wheat.jpg'
        },
        {
            'name': 'Rice',
            'price': '₹1800 per quintal',
            'guide': 'Rice grows well in flooded fields and clayey soils.',
            'image': 'rice.jpg'
        },
        {
            'name': 'Maize',
            'price': '₹1500 per quintal',
            'guide': 'Maize is a warm-season crop requiring good sunlight.',
            'image': 'maize.jpg'
        },
        {
            'name': 'Cotton',
            'price': '₹2500 per quintal',
            'guide': 'Cotton requires well-drained soils and moderate rainfall.',
            'image': 'cotton.jpg'
        },
        {
            'name': 'Barley',
            'price': '₹2000 per quintal',
            'guide': 'Barley grows well in cool climates and fertile soil.',
            'image': 'Barley.webp'
        },
        {
            'name': 'Sugarcane',
            'price': '₹3200 per ton',
            'guide': 'Sugarcane needs a long, warm growing season with abundant water.',
            'image': 'sugarcane.jpg'
        },
        {
            'name': 'Potato',
            'price': '₹1200 per quintal',
            'guide': 'Potatoes prefer cool climates and well-drained sandy loam soil.',
            'image': 'potato.jpg'
        },
        {
            'name': 'Onion',
            'price': '₹1400 per quintal',
            'guide': 'Onions grow well in mild weather with loose, fertile soil.',
            'image': 'onion.jpg'
        },
        {
            'name': 'Tomato',
            'price': '₹900 per quintal',
            'guide': 'Tomatoes need warm weather and well-drained, fertile soil.',
            'image': 'tomato.jpg'
        },
        {
            'name': 'Groundnut',
            'price': '₹4800 per quintal',
            'guide': 'Groundnuts require sandy loam soil and warm climate.',
            'image': 'groundnut.jpg'
        },
        {
            'name': 'Soybean',
            'price': '₹5200 per quintal',
            'guide': 'Soybean grows best in warm weather with good rainfall.',
            'image': 'soybean.jpg'
        },
        {
            'name': 'Mustard',
            'price': '₹5300 per quintal',
            'guide': 'Mustard prefers cool weather and fertile, well-drained soil.',
            'image': 'mustard.jpg'
        },
        {
            'name': 'Ginger (Seed)',
            'price': '₹8500 per quintal',
            'guide': 'Ginger thrives in warm, humid climates with loamy soil.',
            'image': 'ginger.jpg'
        },
        {
            'name': 'Arecanut',
            'price': '₹55000 per quintal',
            'guide': 'Arecanut grows well in humid tropical climates.',
            'image': 'arecanut.jpg'
        },
        {
            'name': 'Sunflower',
            'price': '₹4700 per quintal',
            'guide': 'Sunflower needs bright sun and fertile, well-drained soil.',
            'image': 'sunflower.jpg'
        }
    ]

    # Filter crops matching query substring
    results = [crop for crop in crop_data if query in crop['name'].lower()]

    if not results:
        flash('No crops found matching your search.', 'warning')

    return render_template('home.html', results=results)



from flask import render_template, request

@app.route('/market')
def market():
    # All crop prices (across locations)
    all_prices = [
        {"crop_name": "Wheat", "price": 2200, "unit": "quintal", "location": "Delhi", "date": "2025-05-28"},
        {"crop_name": "Wheat", "price": 2100, "unit": "quintal", "location": "Mumbai", "date": "2025-05-28"},
        {"crop_name": "Wheat", "price": 2150, "unit": "quintal", "location": "Chennai", "date": "2025-05-28"},
        {"crop_name": "Rice", "price": 1800, "unit": "quintal", "location": "Kolkata", "date": "2025-05-28"},
        {"crop_name": "Rice", "price": 1750, "unit": "quintal", "location": "Hyderabad", "date": "2025-05-28"},
        {"crop_name": "Maize", "price": 1650, "unit": "quintal", "location": "Bangalore", "date": "2025-05-28"},
        {"crop_name": "Maize", "price": 1620, "unit": "quintal", "location": "Ahmedabad", "date": "2025-05-28"},
        {"crop_name": "Cotton", "price": 6600, "unit": "quintal", "location": "Nagpur", "date": "2025-05-28"},
        {"crop_name": "Cotton", "price": 6800, "unit": "quintal", "location": "Indore", "date": "2025-05-28"},
        {"crop_name": "Sugarcane", "price": 3200, "unit": "ton", "location": "Pune", "date": "2025-05-28"},
        {"crop_name": "Sugarcane", "price": 3100, "unit": "ton", "location": "Kanpur", "date": "2025-05-28"},
        {"crop_name": "Potato", "price": 1200, "unit": "quintal", "location": "Agra", "date": "2025-05-28"},
        {"crop_name": "Potato", "price": 1100, "unit": "quintal", "location": "Lucknow", "date": "2025-05-28"},
        {"crop_name": "Onion", "price": 1400, "unit": "quintal", "location": "Nashik", "date": "2025-05-28"},
        {"crop_name": "Onion", "price": 1350, "unit": "quintal", "location": "Bhopal", "date": "2025-05-28"},
        {"crop_name": "Tomato", "price": 900, "unit": "quintal", "location": "Jaipur", "date": "2025-05-28"},
        {"crop_name": "Tomato", "price": 950, "unit": "quintal", "location": "Patna", "date": "2025-05-28"},
        {"crop_name": "Groundnut", "price": 4800, "unit": "quintal", "location": "Rajkot", "date": "2025-05-28"},
        {"crop_name": "Groundnut", "price": 4700, "unit": "quintal", "location": "Surat", "date": "2025-05-28"},
        {"crop_name": "Soybean", "price": 5200, "unit": "quintal", "location": "Jabalpur", "date": "2025-05-28"},
        {"crop_name": "Soybean", "price": 5150, "unit": "quintal", "location": "Aurangabad", "date": "2025-05-28"},
        {"crop_name": "Mustard", "price": 5300, "unit": "quintal", "location": "Hisar", "date": "2025-05-28"},
        {"crop_name": "Mustard", "price": 5250, "unit": "quintal", "location": "Gwalior", "date": "2025-05-28"},
        {"crop_name": "Ginger (Seed)", "price": 8500, "unit": "quintal", "location": "Shillong", "date": "2025-05-28"},
        {"crop_name": "Arecanut", "price": 55000, "unit": "quintal", "location": "Mangalore", "date": "2025-05-28"},
        {"crop_name": "Barley", "price": 1800, "unit": "quintal", "location": "Amritsar", "date": "2025-05-28"},
        {"crop_name": "Sunflower", "price": 4700, "unit": "quintal", "location": "Chandigarh", "date": "2025-05-28"},
    ]

    selected_location = request.args.get('location')
    crop_name_filter = request.args.get('crop_name')

    # Group all prices by crop
    crop_data = {}
    for entry in all_prices:
        crop = entry['crop_name']
        if crop not in crop_data:
            crop_data[crop] = []
        crop_data[crop].append(entry)

    # Build price list: one entry per crop based on selected location
    prices = []
    for crop, entries in crop_data.items():
        if crop_name_filter and crop != crop_name_filter:
            continue
        selected = selected_location if selected_location in [e['location'] for e in entries] else entries[0]['location']
        selected_entry = next((e for e in entries if e['location'] == selected), entries[0])
        prices.append(selected_entry)

    # All unique locations across all crops
    locations = sorted(set(entry['location'] for entry in all_prices))

    # All available locations per crop
    crop_locations = {crop: sorted({e['location'] for e in entries}) for crop, entries in crop_data.items()}

    # Fertilizer list
    fertilizers = [
        {"name": "Urea", "type": "Nitrogen-based", "composition": "46% Nitrogen"},
        {"name": "DAP", "type": "Phosphorus-based", "composition": "18% Nitrogen, 46% Phosphorus"},
        {"name": "MOP", "type": "Potassium-based", "composition": "60% Potassium"},
        {"name": "SSP", "type": "Phosphorus-based", "composition": "16% Phosphorus, 11% Sulphur"},
        {"name": "Ammonium Sulphate", "type": "Sulphur-based", "composition": "21% Nitrogen, 24% Sulphur"},
        {"name": "Calcium Ammonium Nitrate", "type": "Nitrogen-based", "composition": "27% Nitrogen"},
        {"name": "Zinc Sulphate", "type": "Micronutrient", "composition": "21% Zinc, 10% Sulphur"},
        {"name": "Borax", "type": "Micronutrient", "composition": "11% Boron"},
        {"name": "Neem Coated Urea", "type": "Nitrogen-based", "composition": "46% Nitrogen with neem oil"},
        {"name": "Potassium Nitrate", "type": "Multi-nutrient", "composition": "13% Nitrogen, 44% Potassium"},
    ]

    return render_template(
        'market.html',
        prices=prices,
        fertilizers=fertilizers,
        locations=locations,
        selected_location=selected_location,
        crop_locations=crop_locations
    )



if __name__ == '__main__':
    app.run(debug=True)
