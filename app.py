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
    
    print(request_data)
    
    
    
    data = order_extractor(
        user_case_type=request_data.get('case_type'),
        user_case_number=request_data.get('case_number'),
        user_case_year=request_data.get('case_year')
    )
    
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
