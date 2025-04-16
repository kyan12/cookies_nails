from datetime import datetime
from flask import jsonify, request, current_app, render_template, redirect, abort
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

# Categories for service filtering
CATEGORIES = {
    'basic': 'Basic Services',
    'overlay': 'Gel Overlays',
    'extensions': 'Nail Extensions',
    'refill': 'Maintenance & Refills'
}

def get_page_data():
    """Common data for all pages"""
    return {
        'year': datetime.now().year,
        'business_hours': {
            'Tuesday': '10:00 AM - 7:00 PM',
            'Wednesday': '10:00 AM - 7:00 PM',
            'Thursday': '10:00 AM - 7:00 PM',
            'Friday': '10:00 AM - 7:00 PM',
            'Saturday': '10:00 AM - 7:00 PM',
            'Sunday': 'Closed',
            'Monday': 'Closed'
        },
        'social_links': {
            'instagram': 'https://instagram.com/cookies_palette'
        }
    }

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    featured_services = [s for s in SERVICES if s.get('featured', False)]
    context = {
        **get_page_data(),
        'services': featured_services,
        'meta_description': "Cookie's Palette - Premium nail art and design services in Middle Village, Queens. Specializing in custom gel art, 3D designs, and elegant nail applications.",
        'og_title': "Cookie's Palette - Premium Nail Art & Design",
        'og_description': "Experience premium nail art services at Cookie's Palette in Middle Village, Queens. Custom designs, gel applications, and 3D nail art.",
        'og_image': '/static/images/hero-nails2.jpg'
    }
    return render_template('index.html', **context)

@bp.route('/services', methods=['GET'])
def services():
    category = request.args.get('category', None)
    if category and category not in CATEGORIES:
        abort(404)
        
    filtered_services = SERVICES
    if category:
        filtered_services = [s for s in SERVICES if s['category'] == category]
        
    context = {
        **get_page_data(),
        'services': filtered_services,
        'categories': CATEGORIES,
        'current_category': category,
        'meta_description': "Explore our premium nail services including gel manicures, extensions, and custom nail art designs. View pricing and book your appointment today.",
        'og_title': "Services - Cookie's Palette",
        'og_description': "Premium nail services in Middle Village, Queens. Gel manicures, extensions, and custom designs.",
        'og_image': '/static/images/nail_design_01.jpg'
    }
    return render_template('services.html', **context)

@bp.route('/gallery', methods=['GET'])
def gallery():
    context = {
        **get_page_data(),
        'meta_description': "View our gallery of stunning nail art designs. From simple elegance to elaborate 3D art, see what Cookie's Palette can create for you.",
        'og_title': "Gallery - Cookie's Palette",
        'og_description': "Browse our collection of stunning nail art designs and get inspired for your next nail transformation.",
        'og_image': '/static/images/two_hands_flowery_gold_pink.jpg'
    }
    return render_template('gallery.html', **context)

@bp.route('/about', methods=['GET'])
def about():
    context = {
        **get_page_data(),
        'meta_description': "Meet Cookie, the artist behind Cookie's Palette. Learn about our commitment to quality and creativity in nail artistry.",
        'og_title': "About - Cookie's Palette",
        'og_description': "Learn about Cookie's Palette, your premium nail art studio in Middle Village, Queens.",
        'og_image': '/static/images/two_hands_flowery_gold_pink.jpg'
    }
    return render_template('about.html', **context)

@bp.route('/book', methods=['GET'])
def book():
    return redirect('https://cal.com/cookies-palette')

@bp.route('/submit_contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No form data received")
        
        required_fields = ['firstName', 'lastName', 'email', 'message']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
            
        current_app.logger.info(f"Received contact form submission for {data.get('firstName')} {data.get('lastName')}")
        
        if send_contact_form_email(data):
            return jsonify({
                "success": True,
                "message": "Thank you for your message. We'll be in touch soon!"
            }), 200
        else:
            raise Exception("Failed to send email")
            
    except ValueError as e:
        current_app.logger.error(f"Contact form validation error: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"Contact form submission error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "There was an error submitting your message. Please try again later."
        }), 500

@bp.errorhandler(404)
def not_found_error(error):
    context = {
        **get_page_data(),
        'meta_description': "Page not found - Cookie's Palette",
        'og_title': "404 - Page Not Found",
        'og_description': "The requested page could not be found.",
        'og_image': '/static/images/hero-nails2.jpg'
    }
    return render_template('errors/404.html', **context), 404

@bp.errorhandler(500)
def internal_error(error):
    context = {
        **get_page_data(),
        'meta_description': "Server error - Cookie's Palette",
        'og_title': "500 - Server Error",
        'og_description': "An internal server error occurred.",
        'og_image': '/static/images/hero-nails2.jpg'
    }
    return render_template('errors/500.html', **context), 500
