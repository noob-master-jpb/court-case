from flask import Flask, jsonify, request, send_from_directory, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import *
import json
from functions import *


clist = json.load(open('clist.json', 'r'))['list']

app = Flask(__name__, static_folder='frontend/public', static_url_path='/static')

app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'


migrate = Migrate(app,db)
db.init_app(app)
# with app.app_context():
#     db.create_all()

    
@app.route("/")
def base():
    return render_template('app.html')

@app.route("/<path:path>")
def spa_routing(path):
    try:
        return send_from_directory('frontend/public', path)
    except:
        return render_template('index.html') 

@app.get("/type_list")
def hello():
    if not clist:
        return jsonify({"error": "No case types available"}), 404
    if type(clist) is not list:
        return jsonify({"error": "Invalid case types data"}), 500
    return jsonify(clist), 200

@app.post("/data")
def get_data():
    
    request_data = request.json

    case_type = request_data.get('case_type')
    case_number = request_data.get('case_number')
    case_year = request_data.get('case_year')
    
    if not case_type or not case_number or not case_year:
        return jsonify({"error": "Missing case type, number, or year"}), 400
    

    try:
        query = Query(
            case_type=case_type,
            case_number=case_number,
            case_year=case_year
        )
        db.session.add(query)
        db.session.commit()
        query_id = query.id
    except Exception as e:
        print(f"Error saving query to database: {e}")
        query_id = None

    data = order_extractor(
        user_case_type=case_type,
        user_case_number=case_number,
        user_case_year=case_year
    )
    try:
        case = Case(
                query_id = query_id,
                case_type = case_type,
                case_number = case_number,
                case_year = case_year,
                status = data.get('status'),
                filing_date = data.get('filing_date'),
                next_date = data.get('next_date'),
                last_date = data.get('last_date'),
                petitioner = data.get('petitioner'),
                respondent = data.get('respondent'),
                order_link = data.get('order_link'),
                orders = data.get('orders')
        )
        db.session.add(case)
        db.session.commit()
    except Exception as e:
        print(f"Error saving case to database: {e}")
    
    return jsonify(data)

@app.post("/download_pdf")
def download_pdf():
    """Generate and download PDF directly without saving to disk"""
    try:
        request_data = request.json
        
        # Extract case data (same as /data endpoint)
        pdf_data = request_data
        print(f"Received PDF data: {request_data}")
        if not pdf_data:
            return jsonify({"error": "No data found for the given case"}), 404
        
        # Generate PDF as bytes (without saving to disk)
        pdf_bytes = pdf_generator(pdf_data, save_to_disk=False)
        
        if not pdf_bytes:
            return jsonify({"error": "Failed to generate PDF"}), 500
        
        # Generate filename
        filename = get_pdf_filename(pdf_data)
        
        # Return PDF as downloadable response
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'application/pdf'
            }
        )
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({"error": "Failed to generate PDF"}), 500

if __name__ == "__main__":
    app.run(debug=True,port=8080,host="0.0.0.0")
