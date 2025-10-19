# Save this file as make_cover.py
#
# --- FONT REQUIREMENT ---
# 1. Download IBM Plex Serif: https://fonts.google.com/specimen/IBM+Plex+Serif
# 2. Place "IBMPlexSerif-Regular.ttf" and "IBMPlexSerif-Bold.ttf"
#    in the SAME FOLDER as this script.
# -------------------------

import sys
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Spacer

# --- 0. Register Custom Font ---
FONT_REGULAR_FILE = "IBMPlexSerif-Regular.ttf"
FONT_BOLD_FILE = "IBMPlexSerif-Bold.ttf"
FONT_REGULAR_NAME = "IBMPlexSerif"
FONT_BOLD_NAME = "IBMPlexSerif-Bold"

try:
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir == "": # Fix for running in interactive interpreters
        script_dir = os.getcwd()
        
    font_regular_path = os.path.join(script_dir, FONT_REGULAR_FILE)
    font_bold_path = os.path.join(script_dir, FONT_BOLD_FILE)

    pdfmetrics.registerFont(TTFont(FONT_REGULAR_NAME, font_regular_path))
    pdfmetrics.registerFont(TTFont(FONT_BOLD_NAME, font_bold_path))
    addMapping(FONT_REGULAR_NAME, 1, 0, FONT_BOLD_NAME) # Map bold
    
    print("INFO: IBM Plex Serif font loaded successfully.")
    DEFAULT_FONT = FONT_REGULAR_NAME
    DEFAULT_FONT_BOLD = FONT_BOLD_NAME
except Exception as e:
    print(f"\n--- FONT WARNING ---")
    print(f"Could not load IBM Plex Serif font. (Error: {e})")
    print(f"Make sure '{FONT_REGULAR_FILE}' and '{FONT_BOLD_FILE}' are in the same folder as this script.")
    print("Falling back to 'Times-Roman'.\n")
    DEFAULT_FONT = "Times-Roman"
    DEFAULT_FONT_BOLD = "Times-Bold"


# --- 1. Define Page Constants ---
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 25 * mm
RIGHT_MARGIN = 10 * mm
TOP_MARGIN = 10 * mm
BOTTOM_MARGIN = 10 * mm
PADDING = 5 * mm

# Calculate the content area boundaries
CONTENT_LEFT = LEFT_MARGIN + PADDING
CONTENT_RIGHT = PAGE_WIDTH - RIGHT_MARGIN - PADDING
CONTENT_TOP = PAGE_HEIGHT - TOP_MARGIN - PADDING
CONTENT_BOTTOM = BOTTOM_MARGIN + PADDING
CONTENT_MIDDLE_X = (CONTENT_LEFT + CONTENT_RIGHT) / 2


# --- 2. The "Input Section" ---
def get_user_input():
    """Collects all information from the user via the terminal."""
    print("--- Lab Report Cover Page Maker ---")
    print("Please enter the details below (press Enter to use the default value):\n")

    def get_input(prompt, default):
        """Helper to ask a question with a default value."""
        user_value = input(f"{prompt} [{default}]: ").rstrip()
        return user_value if user_value else default

    data = {}
    data['experimentNo'] = get_input("Experiment No", "01")
    
    #
    # >>>>> THIS IS THE MULTI-LINE INPUT FOR SUBJECT NAME <<<<<
    #
    print("\nSubject Name (type one line at a time, type 'done' when finished):")
    subject_lines = []
    default_subject_line1 = "COMPUTER TECHNOLOGY"
    default_subject_line2 = "AND NETWORKING"
    
    # Ask for line 1
    line = input(f"Subject Line 1 [{default_subject_line1}]: ").rstrip()
    if not line: line = default_subject_line1
    subject_lines.append(line)
    
    # Ask for line 2
    line = input(f"Subject Line 2 [{default_subject_line2}]: ").rstrip()
    if not line: line = default_subject_line2
    subject_lines.append(line)

    # Ask for subsequent lines
    i = 3
    while True:
        prompt_text = f"Subject Line {i} [done]: "
        line = input(prompt_text).rstrip()
        if line.lower() == 'done' or line == '':
            break
        if line: # Only append if it's not empty
            subject_lines.append(line)
        i += 1
    
    data['subjectName'] = "\n".join(subject_lines) # Store with newlines
    #
    # >>>>> END OF SUBJECT NAME INPUT SECTION <<<<<
    #
    
    print("") # Add a space
    data['subjectCode'] = get_input("Subject Code", "EN1211")
    
    #
    # --- Multi-line Topic Input ---
    #
    print("\nTopic (type one line at a time, type 'done' when finished):")
    topic_lines = []
    default_topic_line1 = "TOPIC 1"
    default_topic_line2 = "TOPIC 2"
    
    line = input(f"Topic Line 1 [{default_topic_line1}]: ").rstrip()
    if not line: line = default_topic_line1
    topic_lines.append(line)
    
    line = input(f"Topic Line 2 [{default_topic_line2}]: ").rstrip()
    if not line: line = default_topic_line2
    topic_lines.append(line)

    i = 3
    while True:
        prompt_text = f"Topic Line {i} [done]: "
        line = input(prompt_text).rstrip()
        if line.lower() == 'done' or line == '':
            break
        topic_lines.append(line)
        i += 1
    
    data['topic'] = "\n".join(topic_lines) # Store topic with newlines
    #
    # --- End of Topic Input ---
    #

    print("") # Add a space
    data['instructor'] = get_input("Instructor", "MRS.A.K.LIYANAGE")
    data['group'] = get_input("Group", "G07")
    
    print("\nGroup Members (type one per line, type 'done' when finished):")
    group_members = []
    default_members = ["COL/EE/2324/F/205", "COL/EE/2324/F/206", "COL/EE/2324/F/207"]
    i = 0
    while True:
        if i < len(default_members):
            prompt_text = f"Member {i+1} [{default_members[i]}]: "
            member = input(prompt_text).rstrip()
            if not member: member = default_members[i]
        else:
            prompt_text = f"Member {i+1} [done]: "
            member = input(prompt_text).rstrip()
            if member.lower() == 'done' or member == '': break
        
        if member and member.lower() != 'done':
            group_members.append(member)
        i += 1
        
    data['groupMembers'] = "\n".join(group_members)

    print("\n--- Student Details ---")
    data['name'] = get_input("Your Name", "W.M.S.J. WANASINGHE")
    data['regNo'] = get_input("Your Reg No", "COL/EE/2324/F/000")
    data['course'] = get_input("Course", "HNDEEE")
    data['dateInstr'] = get_input("Date of Instruction", "03.03.2025")
    data['dateSub'] = get_input("Date of Submission", "24.03.2025")

    # Convert all data to uppercase
    for key, value in data.items():
        data[key] = value.upper()
        
    print("\nData collection complete. Generating PDF...")
    return data

# --- 3. The "Generate PDF" Function ---
def create_cover_page(data):
    """Creates the PDF file with the specified layout."""
    
    output_filename = "Lab_Report_Cover.pdf"
    try:
        c = canvas.Canvas(output_filename, pagesize=A4)
        c.setFont(DEFAULT_FONT, 10) 

        # --- Draw the Outer Border ---
        border_width = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
        border_height = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
        c.rect(LEFT_MARGIN, BOTTOM_MARGIN, border_width, border_height)

        # --- 1. Top-Right Section (Aligned to Middle) ---
        
        c.setFont(DEFAULT_FONT_BOLD, 23.33) # Approx 5mm
        line_height = 10 * mm
        y_pos = CONTENT_TOP - (line_height / 2)
        
        c.drawString(CONTENT_MIDDLE_X, y_pos, f"EXPERIMENT NO : {data['experimentNo']}")
        y_pos -= line_height
        
        #
        # >>>>> THIS IS THE MULTI-LINE DRAWING FOR SUBJECT NAME <<<<<
        #
        # Split the subject name by the newlines entered by the user
        subject_lines = data['subjectName'].split('\n')
        
        # Draw each line manually
        for line in subject_lines:
            c.drawString(CONTENT_MIDDLE_X, y_pos, line)
            y_pos -= line_height
        #
        # >>>>> END OF SUBJECT NAME DRAWING SECTION <<<<<
        #
        
        c.drawString(CONTENT_MIDDLE_X, y_pos, data['subjectCode'])

      # --- 2. Middle Section (Topic) ---
        styles = getSampleStyleSheet()
        
        topic_style = ParagraphStyle(
            name='Topic',
            parent=styles['Normal'],
            fontName=DEFAULT_FONT_BOLD,
            fontSize=32.66,
            leading=44,          # This controls the gap BETWEEN lines
            alignment=TA_CENTER,
            
            underlineWidth=1,
            underlineColor="#000000",  # Corrected: #00000000 is invisible
            underlineOffset = -1.5 * mm
        ) 
        
        
        
        # Replace python's newline \n with HTML's line break <br/>
        topic_with_breaks = data['topic'].replace('\n', '<br/>')
        
        topic_text = f"<u>{topic_with_breaks}</u>"
        topic_paragraph = Paragraph(topic_text, topic_style)
        
        topic_width = CONTENT_RIGHT - CONTENT_LEFT
        topic_height = 100 * mm 
        
        w, h = topic_paragraph.wrapOn(c, topic_width, topic_height)
        y_topic_bottom = (PAGE_HEIGHT / 2) - (h / 2)
        
        topic_paragraph.drawOn(c, CONTENT_LEFT, y_topic_bottom) # Draw from bottom-left

        # --- 3. Left Section (Instructor/Group) ---
        y_pos = y_topic_bottom - (5 ) # 5mm gap below topic
        c.setFont(DEFAULT_FONT, 14) # Approx 3mm
        line_height_small = 15 
        label_width = 143.33
        
        y_pos -= line_height_small
        c.drawString(CONTENT_LEFT, y_pos, "INSTRUCTED BY")
        c.drawString(CONTENT_LEFT + label_width, y_pos, f": {data['instructor']}")
        
        y_pos -= line_height_small
        c.drawString(CONTENT_LEFT, y_pos, "GROUP")
        c.drawString(CONTENT_LEFT + label_width, y_pos, f": {data['group']}")
        
        y_pos -= line_height_small
        c.drawString(CONTENT_LEFT, y_pos, "GROUP MEMBERS")
        members = data['groupMembers'].split('\n')
        member_y_start = y_pos
        for i, member in enumerate(members):
            indent_x = CONTENT_LEFT + label_width
            if i > 0:
                indent_x += (10)
            c.drawString(indent_x, member_y_start - (i * line_height_small), f": {member}" if i == 0 else member)

        # --- 4. Bottom-Right Section (Aligned to Middle) ---
        y_pos_start = CONTENT_BOTTOM + (5 * line_height_small)
        y_pos = y_pos_start
        label_width = 30 * mm
        value_gap = 2 * mm
        label_x = CONTENT_MIDDLE_X
        value_x = label_x + label_width + value_gap
        
        c.setFont(DEFAULT_FONT, 14)
        
        c.drawString(label_x, y_pos, "NAME")
        c.drawString(value_x, y_pos, f": {data['name']}")
        y_pos -= line_height_small

        c.drawString(label_x, y_pos, "REG NO")
        c.drawString(value_x, y_pos, f": {data['regNo']}")
        y_pos -= line_height_small

        c.drawString(label_x, y_pos, "COURSE")
        c.drawString(value_x, y_pos, f": {data['course']}")
        y_pos -= line_height_small
        
        c.drawString(label_x, y_pos, "DATE OF INS")
        c.drawString(value_x, y_pos, f": {data['dateInstr']}")
        y_pos -= line_height_small
        
        c.drawString(label_x, y_pos, "DATE OF SUB")
        c.drawString(value_x, y_pos, f": {data['dateSub']}")

        # --- Save the PDF ---
        c.save()
        
        print(f"\nSuccessfully downloaded '{output_filename}'!")
        print(f"File saved in: {os.path.abspath(output_filename)}")
    
    except PermissionError:
        print(f"\n--- ERROR ---")
        print(f"Could not save '{output_filename}'.")
        print("Please close the file if it's open in a PDF viewer and try again.")
    except Exception as e:
        print(f"\nAn error occurred while creating the PDF:")
        print(f"ERROR: {e}")

# --- 4. Main Execution ---
if __name__ == "__main__":
    try:
        user_data = get_user_input()
        create_cover_page(user_data)
    except KeyboardInterrupt:
        print("\n\nPDF generation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        
    input("\nPress Enter to exit.")