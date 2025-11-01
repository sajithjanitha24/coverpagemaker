# FILE: app.py
# (Located inside the 'api' folder - VERCEL VERSION)

# We remove 'render_template' because it's no longer used
from flask import Flask, request, send_file
import sys
import os

# --- THIS IS THE KEY FIX ---
# Since 'make_cover_lib.py' is in the SAME folder as 'app.py',
# we can import it directly.
try:
    from make_cover_lib import create_cover_page
except ImportError:
    # This print statement will go to Vercel logs if it fails
    print("Error: Could not import 'make_cover_lib.py'.")
    print("Make sure 'make_cover_lib.py' and font files are in the 'api' folder.")
    sys.exit(1)
# --- END OF FIX ---


# Initialize the Flask app
# Vercel will find this 'app' object
app = Flask(__name__)


# --- Vercel Serverless Function ---
# Vercel will route all requests to '/generate' to this function
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
        print(f"Working directory: {os.getcwd()}")
        print(f"Files in directory: {os.listdir('.')}")
        return str(e), 500

#
# NOTE: The "if __name__ == '__main__':" block and the
# @app.route('/') are removed. Vercel handles static
# routing via 'vercel.json' and does not run 'app.run()'.
#