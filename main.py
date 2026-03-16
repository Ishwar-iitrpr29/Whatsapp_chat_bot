"""
WhatsApp PDF Sender - Main Application

This script sends a PDF to WhatsApp users using a template message.
Using a template message with PDF header allows initiating conversations
WITHOUT requiring a prior reply or the 24-hour messaging window.

Flow:
1. Use your PDF file (or generate a dummy one)
2. Upload the PDF to WhatsApp servers
3. Send the PDF using the "pdf_sender" template message (initiates conversation)

Usage:
    python main.py <receiver_number> [pdf_path]
    
Example:
    python main.py 917385107084 myreport.pdf
    python main.py 917385107084                   # Uses default.pdf or generates dummy
"""

import sys
import os
import time
from config import validate_config, set_receiver_number, RECEIVER_NUMBER
from pdf_generator import generate_pdf
from whatsapp_service import send_pdf_template_message, upload_pdf


def get_pdf_path():
    """
    Get PDF path from command line or use default.
    Priority:
    1. Command line argument (2nd arg)
    2. default.pdf in current directory
    3. Generate dummy.pdf
    """
    # Check for PDF path as second argument
    if len(sys.argv) > 2:
        pdf_path = sys.argv[2]
        if os.path.exists(pdf_path):
            print(f"[INFO] Using PDF from argument: {pdf_path}")
            return pdf_path
        else:
            print(f"[ERROR] PDF file not found: {pdf_path}")
            sys.exit(1)
    
    # Check for default.pdf in current directory
    default_pdf = os.path.join(os.path.dirname(__file__), "default.pdf")
    if os.path.exists(default_pdf):
        print(f"[INFO] Using default PDF: {default_pdf}")
        return default_pdf
    
    # Generate dummy PDF as fallback
    print("[INFO] No PDF specified, generating dummy PDF...")
    return generate_pdf("dummy.pdf")


def main():
    """Main application entry point."""
    print("=" * 60)
    print("WhatsApp PDF Sender - Template Message Initiator")
    print("=" * 60)
    print()
    print("NOTE: Using template message to send PDF - No 24-hour window needed!")
    print()
    
    # Check for command-line argument
    if len(sys.argv) > 1:
        receiver = set_receiver_number(sys.argv[1])
        print(f"[INFO] Using receiver number from argument: {receiver}")
    elif not RECEIVER_NUMBER:
        print("[ERROR] No receiver number provided!")
        print("Usage: python main.py <receiver_number> [pdf_path]")
        print("Example: python main.py 917385107084 myreport.pdf")
        print("\nOr set RECEIVER_NUMBER in .env file")
        sys.exit(1)
    print()
    
    # Step 0: Validate configuration
    print("[STEP 0] Validating configuration...")
    try:
        validate_config()
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    print()
    
    # Step 1: Get PDF file
    print("[STEP 1] Getting PDF file...")
    print("-" * 40)
    pdf_path = get_pdf_path()
    print(f"[SUCCESS] PDF ready: {pdf_path}")
    print()
    
    # Step 2: Upload PDF to WhatsApp servers
    print("[STEP 2] Uploading PDF to WhatsApp...")
    print("-" * 40)
    media_id = upload_pdf(pdf_path)
    
    if not media_id:
        print("[ERROR] Failed to upload PDF. Exiting...")
        sys.exit(1)
    print(f"[SUCCESS] PDF uploaded! Media ID: {media_id}")
    print()
    
    # Small delay between API calls
    time.sleep(2)
    
    # Step 3: Send PDF using template message (initiates conversation)
    print("[STEP 3] Sending PDF via template message...")
    print("-" * 40)
    print("This sends the PDF AND initiates the conversation!")
    
    # Use original filename for display
    filename = os.path.basename(pdf_path)
    template_result = send_pdf_template_message(
        media_id=media_id,
        template_name="pdf_sender",
        language_code="en",
        filename=filename
    )
    
    if "error" in template_result:
        print("[ERROR] Failed to send PDF template message.")
        print(f"Error: {template_result.get('error', {}).get('message', 'Unknown error')}")
        sys.exit(1)
    print("[SUCCESS] PDF template message sent!")
    print()
    
    # Summary
    print("=" * 60)
    print("WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Summary:")
    print("  - PDF generated: dummy.pdf")
    print(f"  - Media uploaded: {media_id}")
    print("  - Template message with PDF: Delivered")
    print()
    print("The recipient will receive your PDF immediately,")
    print("even if they haven't messaged you in the last 24 hours!")
    print()


if __name__ == "__main__":
    main()
