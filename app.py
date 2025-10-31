# FILE: app.py
# This is the simple version for running in your browser.

from flask import Flask, render_template, request, send_file
import sys

# Import the function from your other file
try:
    from make_cover_lib import create_cover_page
except ImportError:
    print("Error: Could not import 'make_cover_lib.py'.")
    print("Make sure it is in the same folder as app.py.")
    sys.exit(1)

# Initialize the Flask app
app = Flask(__name__)

# --- Your Flask Routes (Unchanged) ---
@app.route('/')
def index():
    """ This is the route for the home page. """
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_pdf():
    """ This is the route that receives the form data. """
    try:
        # 1. Get data from the HTML form
        data = request.form.to_dict()
        
        # --- NEW LOGIC: Get the report type ---
        # Get the 'report_type' from the form. Default to 'lab' if not found.
        report_type = data.get('report_type', 'lab')
        
        # Remove it from the main data dict so it doesn't get processed
        if 'report_type' in data:
            data.pop('report_type')
        # --- END OF NEW LOGIC ---

        # 2. Convert all remaining data to uppercase
        for key, value in data.items():
            data[key] = value.upper()

        # 3. Call your Python function to generate the PDF
        #    We must now pass the 'report_type' to it.
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
            download_name=download_filename,  # Use the new variable
            mimetype="application/pdf"
        )
        
    except Exception as e:
        # Print a helpful error message to the console if something goes wrong
        print(f"An error occurred: {e}")
        return str(e), 500

if __name__ == '__main__':
    # Run the web server
    print("--- Starting Flask server ---")
    print("Open this URL in your web browser: http://127.0.0.1:5000")
    print("Press CTRL+C in this terminal to stop the server.")
    app.run(debug=True, host='127.0.0.1', port=5000)