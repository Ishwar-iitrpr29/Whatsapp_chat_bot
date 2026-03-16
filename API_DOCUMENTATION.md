  # WhatsApp Cloud API - Documentation

## Project Overview

This project demonstrates sending WhatsApp messages and PDF documents using the **Meta WhatsApp Cloud API**.

---

## Account Information

| Field | Value |
|-------|-------|
| WhatsApp Business Account ID | `1496762318835949` |
| Phone Number ID | `1057654137421852` |
| Test Sender Number | `+1 555 156 0369` |
| Receiver Number | Passed via command line or `.env` file |
| API Version | `v22.0` |

---

## APIs Used

### 1. Send Template Message with PDF Header API (Recommended)

**Endpoint:**
```
POST https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages
```

**Purpose:** Send template message with PDF document as header. This allows sending PDFs **without requiring** a prior reply or 24-hour window!

**Headers:**
```
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "917385107084",
  "type": "template",
  "template": {
    "name": "pdf_sender",
    "language": {
      "code": "en"
    },
    "components": [
      {
        "type": "header",
        "parameters": [
          {
            "type": "document",
            "document": {
              "id": "MEDIA_ID_FROM_UPLOAD",
              "filename": "Report.pdf"
            }
          }
        ]
      }
    ]
  }
}
```

**Response (Success):**
```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917385107084", "wa_id": "917385107084"}],
  "messages": [{"id": "wamid.HBgMOTE3Mzg1MTA3MDg0..."}]
}
```

**Note:** Template `pdf_sender` must be created and approved in WhatsApp Manager with a document header.

---

### 1b. Send Simple Template Message API

**Endpoint:**
```
POST https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages
```

**Purpose:** Send simple pre-approved template messages (like hello_world) to initiate conversations.

**Headers:**
```
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "917385107084",
  "type": "template",
  "template": {
    "name": "hello_world",
    "language": {
      "code": "en_US"
    }
  }
}
```

**Response (Success):**
```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917385107084", "wa_id": "917385107084"}],
  "messages": [{"id": "wamid.HBgMOTE3Mzg1MTA3MDg0..."}]
}
```

---

### 2. Upload Media API

**Endpoint:**
```
POST https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/media
```

**Purpose:** Upload media files (PDF, images, videos) to WhatsApp servers.

**Headers:**
```
Authorization: Bearer {ACCESS_TOKEN}
```

**Request Body (multipart/form-data):**
```
file: <binary PDF data>
messaging_product: whatsapp
type: application/pdf
```

**Response (Success):**
```json
{
  "id": "2648273895571453"
}
```

The `id` returned is the **Media ID** used to send the document.

---

### 3. Send Document Message API

**Endpoint:**
```
POST https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages
```

**Purpose:** Send uploaded documents to recipients.

**Headers:**
```
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
```

**Request Body:**
```json
{
  "messaging_product": "whatsapp",
  "to": "917385107084",
  "type": "document",
  "document": {
    "id": "2648273895571453",
    "filename": "Demo_Report.pdf",
    "caption": "Here is your demo report."
  }
}
```

**Response (Success):**
```json
{
  "messaging_product": "whatsapp",
  "contacts": [{"input": "917385107084", "wa_id": "917385107084"}],
  "messages": [{"id": "wamid.HBgMOTE3Mzg1MTA3MDg0..."}]
}
```

---

## Application Flow

```
┌─────────────────────────────────────────────────────────────┐
│              main.py <receiver_number>                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PARSE: Get Receiver Number                                 │
│     └── From command line arg or .env file                  │
│                                                             │
│  STEP 0: Validate Configuration                             │
│     └── Check ACCESS_TOKEN and RECEIVER_NUMBER exist        │
│                                                             │
│  STEP 1: Generate PDF                                       │
│     └── Create dummy.pdf using reportlab                    │
│                                                             │
│  STEP 2: Upload PDF                                         │
│     └── POST /media → returns Media ID                      │
│                                                             │
│  STEP 3: Send PDF via Template Message (INITIATES CHAT!)    │
│     └── POST /messages (template: pdf_sender with PDF)      │
│     └── No 24-hour window required!                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 24-Hour Messaging Window & Template Messages

### The Reply Requirement (For Regular Messages)

WhatsApp Cloud API has a **24-hour messaging window** restriction for regular messages:

| Message Type | Can Send Anytime? | Requires Reply First? |
|--------------|-------------------|----------------------|
| Template Messages | ✅ Yes | ❌ No |
| Template with Media Header | ✅ Yes | ❌ No |
| Text Messages | ❌ No | ✅ Yes |
| Document/Media (standalone) | ❌ No | ✅ Yes |
| Interactive Messages | ❌ No | ✅ Yes |

### Solution: Template Messages with Document Header

By using a **template message with a PDF in the header**, you can:
- ✅ Send PDFs **anytime** to any opted-in user
- ✅ **Initiate conversations** without prior reply
- ✅ Bypass the 24-hour window restriction
- ✅ Deliver documents immediately

### How This Project Works

1. **Generate/Upload PDF** → Get Media ID from WhatsApp servers
2. **Send `pdf_sender` template** → PDF is embedded in the template header
3. **Recipient receives PDF** → No prior reply needed!

The `pdf_sender` template includes:
- **Header:** Document (your PDF)
- **Body:** "Hello, these pdf is shared by whatsapp manager"
- **Footer:** "spe"

### Creating the Template (WhatsApp Manager)

1. Go to WhatsApp Manager → Message Templates → Create Template
2. Set **Header** type to "Document"
3. Add **Body** text and optional **Footer**
4. Submit for review (usually approved within minutes)
5. Use the approved template name in your code

---

## Error Codes Reference

| Code | Error | Solution |
|------|-------|----------|
| 131030 | Recipient not in allowed list | Add number in Meta Developer Console |
| 131031 | Business not verified | Complete business verification |
| 131047 | Re-engagement required | Recipient must reply first |
| 131051 | Invalid parameter | Check request body format |
| 190 | Invalid access token | Generate new token |
| Local | ACCESS_TOKEN not found | Set ACCESS_TOKEN in `.env` file |
| Local | RECEIVER_NUMBER not found | Pass number as argument or set in `.env` |

---

## Project Files

| File | Purpose |
|------|---------|
| `main.py` | Main entry point - orchestrates the workflow, accepts receiver number as argument |
| `config.py` | Configuration, environment variables, and `set_receiver_number()` function |
| `pdf_generator.py` | Creates PDF using reportlab |
| `whatsapp_service.py` | WhatsApp API service functions |
| `requirements.txt` | Python dependencies |
| `.env` | Access token and receiver number storage (create this) |
| `.env.example` | Template for `.env` file |

---

## Access Token

The access token is obtained from:
1. Go to [Meta Developer Console](https://developers.facebook.com/)
2. Your App → WhatsApp → API Setup
3. Click "Generate access token"

**Note:** Test tokens expire after 24 hours. For production, create a permanent System User token.

---

## Running the Project

```bash
# 1. Navigate to project
cd whatsapp_pdf_sender

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run the script with receiver number
python main.py <receiver_number>

# Examples:
python main.py 917385107084
python main.py +91-7385107084
```

### Providing Receiver Number

The receiver number is **not hardcoded** and must be provided in one of two ways:

**Option 1: Command-line argument (Recommended)**
```bash
python main.py 917385107084
```
- Automatically strips `+`, `-`, and spaces
- Example formats accepted: `917385107084`, `+91-7385107084`, `+91 7385 107084`

**Option 2: Environment variable in `.env` file**
```env
ACCESS_TOKEN=your_token_here
RECEIVER_NUMBER=917385107084
```
Then run without argument:
```bash
python main.py
```

**Note:** The receiver number must be added to the allowed list in Meta Developer Console first.

---

## Next Steps

1. **Run the script** → PDF will be sent immediately via template
2. No need to reply first - template messages bypass the 24-hour window!
3. For production: Create a System User token for permanent access
4. For production: Verify your business in Meta Business Manager
5. Create additional templates for different PDF types/use cases

---

## Resources

- [WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Message Templates Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)
- [Media Messages Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages#media-messages)
- [Conversation-Based Pricing](https://developers.facebook.com/docs/whatsapp/pricing)
