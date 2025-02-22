from flask import jsonify, request, current_app, render_template, redirect
from app.main import bp
from app.util.email import send_contact_form_email
# app/models.py

# app/models.py

SERVICES = [
    {
        'id': 1,
        'name': 'Gel Manicure',
        'description': 'Classic gel manicure with your choice of color',
        'price': 55,
        'duration': '30-60min',
        'category': 'basic',
        'featured': True,
        'image': 'two_hands_flowery_gold_pink.jpg'
    },
    {
        'id': 2,
        'name': 'Hard Gel Overlay',
        'description': 'Protective hard gel overlay for natural nail strength',
        'price': 75,
        'duration': '90min',
        'category': 'overlay',
        'featured': True
    },
    {
        'id': 10,
        'name': 'Apres Soft Gel',
        'description': 'Soft gel extensions using Apres system',
        'price': 70,
        'duration': '60min',
        'category': 'extensions',
        'featured': True
    },
    {
        'id': 3,
        'name': 'Hard Gel Overlay Refill',
        'description': 'Maintenance service for existing hard gel overlay',
        'price': 65,
        'duration': '60min',
        'category': 'refill'
    },
    {
        'id': 4,
        'name': 'Gel X Short',
        'description': 'Short length nail extensions using Gel X system',
        'price': 80,
        'duration': '90-120min',
        'category': 'extensions'
    },
    {
        'id': 5,
        'name': 'Gel X Short Refill',
        'description': 'Maintenance for short Gel X extensions',
        'price': 75,
        'duration': '60min',
        'category': 'refill'
    },
    {
        'id': 6,
        'name': 'Gel X Medium',
        'description': 'Medium length nail extensions using Gel X system',
        'price': 90,
        'duration': '90-120min',
        'category': 'extensions'
    },
    {
        'id': 7,
        'name': 'Gel X Medium Refill',
        'description': 'Maintenance for medium Gel X extensions',
        'price': 85,
        'duration': '60min',
        'category': 'refill'
    },
    {
        'id': 8,
        'name': 'Gel X Long',
        'description': 'Long length nail extensions using Gel X system',
        'price': 100,
        'duration': '90-120min',
        'category': 'extensions'
    },
    {
        'id': 9,
        'name': 'Gel X Long Refill',
        'description': 'Maintenance for long Gel X extensions',
        'price': 95,
        'duration': '90min',
        'category': 'refill'
    },
    {
        'id': 11,
        'name': 'Apres Soft Gel Refill',
        'description': 'Maintenance for Apres soft gel extensions',
        'price': 60,
        'duration': '60min',
        'category': 'refill'
    },
]

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html', services=SERVICES)

@bp.route('/services', methods=['GET'])
def services():
    return render_template('services.html', services=SERVICES)

@bp.route('/gallery', methods=['GET'])
def gallery():
    return render_template('gallery.html')

@bp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@bp.route('/book', methods=['GET'])
def book():
    return redirect('https://cal.com/cookies-palette')

@bp.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No form data received")
            
        current_app.logger.info(f"Received contact form submission for {data.get('firstName')} {data.get('lastName')}")
        
        if send_contact_form_email(data):
            return jsonify({
                "success": True,
                "message": "Thank you for your message. We'll be in touch soon!"
            }), 200
        else:
            raise Exception("Failed to send email")
            
    except Exception as e:
        current_app.logger.error(f"Contact form submission error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "There was an error submitting your message. Please try again later."
        }), 500
