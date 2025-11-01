# FILE: app.py
# (Located inside the 'api' folder - VERCEL VERSION)
#
# --- THIS FILE IS NOW FIXED ---

from flask import Flask, request, send_file
import sys
import os

# --- THIS IS THE KEY FIX ---
# I have removed ".py" from the import.
# This is the correct Python syntax.
try:
    from make_cover_lib import create_cover_page
except ImportError as e:
    # This print statement will go to Vercel logs if it fails
    print(f"CRITICAL Error: Could not import 'make_cover_lib'. {e}")
    print("Make sure 'make_cover_lib.py' is in the 'api' folder.")
    sys.exit(1)
# --- END OF FIX ---


# Initialize the Flask app
# Vercel will find this 'app' object
app = Flask(__name__)


# --- Vercel Serverless Function ---
# Your vercel.json will route '/generate' requests here
@app.route('/generate', methods=['POST'])
def generate_pdf():
    """ This is the route that receives the form data. """
    try:
        # 1. Get data from the HTML form
        data = request.form.to_dict()
        
        # --- NEW LOGIC: Get the report type ---
        report_type = data.get('report_type', 'lab')
        
        if 'report_type' in data:
            data.pop('report_type')
        # --- END OF NEW LOGIC ---

        # 2. Convert all remaining data to uppercase
        for key, value in data.items():
            data[key] = value.upper()

        # 3. Call your Python function to generate the PDF
        # This function finds the .ttf files because its path logic is correct
        pdf_buffer = create_cover_page(data, report_type)

        # --- NEW LOGIC: Change download name based on type ---
        if report_type == 'assignment':
            download_filename = "Assignment_Cover.pdf"
        else:
            download_filename = "Lab_Report_Cover.pdf"
        # --- END OF NEW LOGIC ---

        # 4. Send the generated PDF back to the browser as a download
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=download_filename, 
            mimetype="application/pdf"
        )
        
    except Exception as e:
        # Print a helpful error message to the Vercel logs
        print(f"--- FUNCTION CRASHED ---")
        print(f"An error occurred: {e}")
        # This will show us if the font files are in the same folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Working directory: {current_dir}")
        print(f"Files in directory: {os.listdir(current_dir)}")
        return str(e), 500

#
# NOTE: The "if __name__ == '__main__':" block and the
# @app.route('/') are removed. Vercel handles static
# routing via 'vercel.json' and does not run 'app.run()'.
#
