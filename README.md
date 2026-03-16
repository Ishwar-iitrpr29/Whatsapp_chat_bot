# WhatsApp PDF Sender

A Python project that demonstrates sending WhatsApp messages and PDF documents using the Meta WhatsApp Cloud API.

## Features

- Send template messages (hello_world) to initiate conversations
- Generate PDF documents using ReportLab
- Upload media files to WhatsApp servers
- Send PDF documents to recipients

## Project Structure

```
whatsapp_pdf_sender/
│
├── main.py              # Main entry point - runs the complete workflow
├── config.py            # Configuration and environment variables
├── pdf_generator.py     # PDF generation using reportlab
├── whatsapp_service.py  # WhatsApp Cloud API service functions
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Prerequisites

- Python 3.7+
- A Meta Developer Account with WhatsApp Business API access
- A WhatsApp Business Account
- Access Token from Meta Developer Console

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd whatsapp_pdf_sender
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Setting up ACCESS_TOKEN

The ACCESS_TOKEN is required to authenticate with the WhatsApp Cloud API.

**Option 1: Using a .env file (Recommended)**

Create a `.env` file in the project root:

```env
ACCESS_TOKEN=your_access_token_here
```

**Option 2: Environment Variable**

Set the environment variable directly:

```bash
# Windows (PowerShell):
$env:ACCESS_TOKEN="your_access_token_here"

# Windows (CMD):
set ACCESS_TOKEN=your_access_token_here

# macOS/Linux:
export ACCESS_TOKEN="your_access_token_here"
```

### Getting Your Access Token

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Navigate to your app → WhatsApp → API Setup
3. Click "Generate access token"
4. Copy the token and save it securely

> **Note:** Test tokens expire after 24 hours. For production, create a System User token.

## API Configuration

The following values are pre-configured in `config.py`:

| Setting | Value |
|---------|-------|
| WhatsApp Business Account ID | 1496762318835949 |
| Phone Number ID | 1057654137421852 |
| Test Number (Sender) | +1 555 156 0369 |
| Receiver Number | +91738510784 |
| API Version | v22.0 |

To change the receiver number, edit the `RECEIVER_NUMBER` in `config.py`.

## Usage

Run the main script:

```bash
python main.py
```

### Workflow

The script performs the following steps:

1. **Send Template Message**: Sends the "hello_world" template to initiate the chat
2. **Generate PDF**: Creates a dummy PDF file with sample content
3. **Upload PDF**: Uploads the PDF to WhatsApp's media servers
4. **Send Document**: Sends the uploaded PDF to the receiver

### Expected Output

```
============================================================
WhatsApp PDF Sender - Meta Cloud API Demo
============================================================

[STEP 0] Validating configuration...
[CONFIG] Configuration loaded successfully.

[STEP 1] Sending template message...
----------------------------------------
[WHATSAPP] Sending template message 'hello_world' to 91738510784...
[WHATSAPP] Template message sent successfully!
[WHATSAPP] Message ID: wamid.xxxx...
[SUCCESS] Template message sent!

[STEP 2] Generating dummy PDF...
----------------------------------------
[PDF] Generated PDF: /path/to/dummy.pdf
[SUCCESS] PDF generated at: /path/to/dummy.pdf

[STEP 3] Uploading PDF to WhatsApp...
----------------------------------------
[WHATSAPP] Uploading PDF: dummy.pdf...
[WHATSAPP] PDF uploaded successfully!
[WHATSAPP] Media ID: 123456789...
[SUCCESS] PDF uploaded! Media ID: 123456789...

[STEP 4] Sending PDF document...
----------------------------------------
[WHATSAPP] Sending document to 91738510784...
[WHATSAPP] Document sent successfully!
[WHATSAPP] Message ID: wamid.yyyy...
[SUCCESS] PDF delivered!

============================================================
WORKFLOW COMPLETED SUCCESSFULLY!
============================================================
```

## Troubleshooting

### Common Errors

1. **"ACCESS_TOKEN not found"**
   - Ensure you've created a `.env` file with your token
   - Or set the environment variable before running

2. **"Error sending template message"**
   - Verify the receiver number is registered with your WhatsApp Business Account
   - Check if the hello_world template is approved

3. **"Error uploading PDF"**
   - Verify your access token has the required permissions
   - Check file size (WhatsApp has a 100MB limit for documents)

4. **Permission errors**
   - Ensure your app has `whatsapp_business_messaging` permission

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `POST /{phone-number-id}/messages` | Send messages (template & document) |
| `POST /{phone-number-id}/media` | Upload media files |

## Resources

- [WhatsApp Business Cloud API Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Message Templates](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)
- [Media Messages](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages#media-messages)

## License

This project is for demonstration purposes.
