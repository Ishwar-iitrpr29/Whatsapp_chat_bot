"""
WhatsApp Cloud API Service module.
Handles all interactions with the Meta WhatsApp Cloud API.
"""

import requests
import os
import config  # Import module to access dynamic RECEIVER_NUMBER


def get_headers():
    """Get authorization headers for API requests."""
    return {
        "Authorization": f"Bearer {config.ACCESS_TOKEN}",
    }


def send_template_message(template_name="hello_world", language_code="en_US"):
    """
    Send a template message to initiate the chat.
    
    Args:
        template_name: Name of the approved template (default: hello_world)
        language_code: Language code for the template (default: en_US)
    
    Returns:
        dict: API response
    """
    url = f"{config.BASE_URL}/{config.PHONE_NUMBER_ID}/messages"
    
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": config.RECEIVER_NUMBER,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            }
        }
    }
    
    print(f"[WHATSAPP] Sending template message '{template_name}' to {config.RECEIVER_NUMBER}...")
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if response.status_code == 200:
        message_id = result.get("messages", [{}])[0].get("id", "N/A")
        print(f"[WHATSAPP] Template message sent successfully!")
        print(f"[WHATSAPP] Message ID: {message_id}")
    else:
        print(f"[WHATSAPP] Error sending template message: {result}")
    
    return result


def send_pdf_template_message(media_id, template_name="pdf_sender", language_code="en", filename="document.pdf"):
    """
    Send a template message with PDF document header to initiate chat.
    
    This function sends a pre-approved template that includes a PDF document
    in the header. This allows sending PDFs to users WITHOUT:
    - Needing a prior reply from the recipient
    - Waiting for the 24-hour messaging window
    
    The template must be pre-approved in WhatsApp Manager with a document header.
    
    Args:
        media_id: Media ID of the uploaded PDF (from upload_pdf function)
        template_name: Name of the approved template (default: pdf_sender)
        language_code: Language code for the template (default: en)
        filename: Display name for the PDF document
    
    Returns:
        dict: API response
    """
    url = f"{config.BASE_URL}/{config.PHONE_NUMBER_ID}/messages"
    
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": config.RECEIVER_NUMBER,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "document",
                            "document": {
                                "id": media_id,
                                "filename": filename
                            }
                        }
                    ]
                }
            ]
        }
    }
    
    print(f"[WHATSAPP] Sending PDF template '{template_name}' to {config.RECEIVER_NUMBER}...")
    print(f"[WHATSAPP] This initiates a conversation WITHOUT requiring prior reply!")
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if response.status_code == 200:
        message_id = result.get("messages", [{}])[0].get("id", "N/A")
        print(f"[WHATSAPP] PDF template message sent successfully!")
        print(f"[WHATSAPP] Message ID: {message_id}")
    else:
        print(f"[WHATSAPP] Error sending PDF template: {result}")
    
    return result


def send_pdf_template_with_link(pdf_url, template_name="pdf_sender", language_code="en", filename="document.pdf"):
    """
    Send a template message with PDF document header using a public URL.
    
    Alternative to send_pdf_template_message - uses a public URL instead of 
    uploading the PDF first. The URL must be publicly accessible.
    
    Args:
        pdf_url: Public URL of the PDF document
        template_name: Name of the approved template (default: pdf_sender)
        language_code: Language code for the template (default: en)
        filename: Display name for the PDF document
    
    Returns:
        dict: API response
    """
    url = f"{config.BASE_URL}/{config.PHONE_NUMBER_ID}/messages"
    
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": config.RECEIVER_NUMBER,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": language_code
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "document",
                            "document": {
                                "link": pdf_url,
                                "filename": filename
                            }
                        }
                    ]
                }
            ]
        }
    }
    
    print(f"[WHATSAPP] Sending PDF template '{template_name}' with URL to {config.RECEIVER_NUMBER}...")
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if response.status_code == 200:
        message_id = result.get("messages", [{}])[0].get("id", "N/A")
        print(f"[WHATSAPP] PDF template message sent successfully!")
        print(f"[WHATSAPP] Message ID: {message_id}")
    else:
        print(f"[WHATSAPP] Error sending PDF template: {result}")
    
    return result


def upload_pdf(pdf_path):
    """
    Upload a PDF file to WhatsApp servers.
    
    Args:
        pdf_path: Full path to the PDF file
    
    Returns:
        str: Media ID of the uploaded file, or None if failed
    """
    url = f"{config.BASE_URL}/{config.PHONE_NUMBER_ID}/media"
    
    headers = get_headers()
    
    # Read the file and prepare for upload
    filename = os.path.basename(pdf_path)
    
    with open(pdf_path, "rb") as pdf_file:
        files = {
            "file": (filename, pdf_file, "application/pdf")
        }
        data = {
            "messaging_product": "whatsapp",
            "type": "application/pdf"
        }
        
        print(f"[WHATSAPP] Uploading PDF: {filename}...")
        
        response = requests.post(url, headers=headers, files=files, data=data)
        result = response.json()
    
    if response.status_code == 200:
        media_id = result.get("id")
        print(f"[WHATSAPP] PDF uploaded successfully!")
        print(f"[WHATSAPP] Media ID: {media_id}")
        return media_id
    else:
        print(f"[WHATSAPP] Error uploading PDF: {result}")
        return None


def send_document(media_id, filename="document.pdf", caption=None):
    """
    Send an uploaded document to the receiver.
    
    Args:
        media_id: Media ID from the upload response
        filename: Display name for the document
        caption: Optional caption for the document
    
    Returns:
        dict: API response
    """
    url = f"{config.BASE_URL}/{config.PHONE_NUMBER_ID}/messages"
    
    headers = get_headers()
    headers["Content-Type"] = "application/json"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": config.RECEIVER_NUMBER,
        "type": "document",
        "document": {
            "id": media_id,
            "filename": filename
        }
    }
    
    if caption:
        payload["document"]["caption"] = caption
    
    print(f"[WHATSAPP] Sending document to {config.RECEIVER_NUMBER}...")
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    
    if response.status_code == 200:
        message_id = result.get("messages", [{}])[0].get("id", "N/A")
        print(f"[WHATSAPP] Document sent successfully!")
        print(f"[WHATSAPP] Message ID: {message_id}")
    else:
        print(f"[WHATSAPP] Error sending document: {result}")
    
    return result


if __name__ == "__main__":
    # Test the service functions
    print("WhatsApp Service Module - Test Mode")
    print("Use main.py to run the full workflow.")
