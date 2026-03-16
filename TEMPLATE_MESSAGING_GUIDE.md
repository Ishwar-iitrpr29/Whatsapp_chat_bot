# WhatsApp Cloud API - Template Messaging Guide

## Overview

This guide explains how WhatsApp template messages work and why they can bypass the 24-hour messaging window.

---

## The 24-Hour Messaging Window

WhatsApp has a **conversation-based messaging model** to prevent spam:

```
┌─────────────────────────────────────────────────────────────────┐
│                    REGULAR MESSAGES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Business ──────X──────> User                                  │
│              (BLOCKED - no prior conversation)                  │
│                                                                 │
│   User ─────────────────> Business   ← User initiates           │
│              (Message received)                                 │
│                                                                 │
│   ┌──────────── 24-HOUR WINDOW OPENS ────────────┐              │
│   │                                              │              │
│   │   Business ────────> User  ✓ Allowed         │              │
│   │   Business ────────> User  ✓ Allowed         │              │
│   │   (text, images, PDFs, anything!)            │              │
│   │                                              │              │
│   └──────────────────────────────────────────────┘              │
│                                                                 │
│   After 24 hours: WINDOW CLOSES → Back to blocked               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Template Messages - The Exception

**Template messages are pre-approved by Meta** and can be sent **anytime**, even without a conversation:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEMPLATE MESSAGES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Business ──── TEMPLATE ────> User   ✓ ALWAYS ALLOWED          │
│                                                                 │
│   • No prior conversation needed                                │
│   • No 24-hour window needed                                    │
│   • Can include: text, images, videos, documents, buttons       │
│   • Must be pre-approved by Meta                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why Templates Bypass the 24-Hour Window

| Aspect | Regular Messages | Template Messages |
|--------|------------------|-------------------|
| **Approval** | None needed | Must be approved by Meta |
| **Content** | Anything | Fixed format, reviewed for spam |
| **Initiation** | User must message first | Business can initiate |
| **24-hour window** | Required | Not required |
| **Cost** | Free (within window) | Paid per conversation |
| **Use case** | Customer support replies | Notifications, alerts, marketing |

**Meta's reasoning:**
- Templates are **reviewed** before approval → no spam
- Templates have **fixed structure** → predictable content
- Business **pays per conversation** → economic disincentive for spam
- Users can **opt-out** → control over receiving

---

## APIs Used in This Project

### 1. Upload Media API

**Endpoint:**
```
POST https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/media
```

**Purpose:** Upload your PDF to WhatsApp's servers first

**Headers:**
```
Authorization: Bearer {ACCESS_TOKEN}
```

**Request Body (multipart/form-data):**
```
file: <your PDF binary>
messaging_product: whatsapp
type: application/pdf
```

**Response (Success):**
```json
{
  "id": "1234567890123456"
}
```

The `id` returned is the **Media ID** - you'll use this in the next API call.

---

### 2. Send Template Message with Document API

**Endpoint:**
```
POST https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages
```

**Purpose:** Send the template with your PDF embedded in header

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
              "id": "1234567890123456",
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
  "messages": [{"id": "wamid.HBgMOTE3..."}]
}
```

---

## Template Structure (pdf_sender)

Your approved template has the following structure:

| Component | Content |
|-----------|---------|
| **Header** | Document (PDF) - *provided dynamically via API* |
| **Body** | "Hello, these pdf is shared by whatsapp manager" |
| **Footer** | "spe" |

**Important:** The PDF you uploaded when creating the template was only a **sample for approval**. Each time you send the template via API, you must provide the actual PDF to send.

---

## Complete Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                        YOUR APPLICATION                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. PREPARE PDF                                                  │
│     └── Your PDF file (report.pdf, invoice.pdf, etc.)            │
│                                                                  │
│  2. UPLOAD TO WHATSAPP SERVERS                                   │
│     │                                                            │
│     │  POST /media                                               │
│     │  ├── file: <PDF binary>                                    │
│     │  └── type: application/pdf                                 │
│     │                                                            │
│     └── Response: { "id": "MEDIA_ID_12345" }                     │
│                                                                  │
│  3. SEND TEMPLATE MESSAGE                                        │
│     │                                                            │
│     │  POST /messages                                            │
│     │  ├── template: "pdf_sender"                                │
│     │  ├── language: "en"                                        │
│     │  └── components:                                           │
│     │      └── header:                                           │
│     │          └── document: { id: "MEDIA_ID_12345" }            │
│     │                                                            │
│     └── Response: { "messages": [{ "id": "wamid..." }] }         │
│                                                                  │
│  4. USER RECEIVES                                                │
│     ┌────────────────────────┐                                   │
│     │  📄 Report.pdf         │                                 │
│     │  ──────────────────    │                                   │
│     │  Hello, these pdf is   │                                   │
│     │  shared by whatsapp    │                                   │
│     │  manager               │                                   │
│     │  ──────────────────    │                                   │
│     │  spe             16:12 │                                   │
│     └────────────────────────┘                                   │
│                                                                  │
│  ✓ No prior reply needed!                                        │
│  ✓ No 24-hour window needed!                                     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Conversation Types & Pricing

WhatsApp categorizes conversations for billing:

| Category | Who Opens | Duration | Example |
|----------|-----------|----------|---------|
| **Marketing** | Business (template) | 24 hours | Promotions, offers |
| **Utility** | Business (template) | 24 hours | Order updates, receipts |
| **Authentication** | Business (template) | 24 hours | OTPs, verification |
| **Service** | User (reply) | 24 hours | Customer support |

Your `pdf_sender` template is categorized as **Marketing**.

---

## Using Public URL Instead of Upload

Alternative method using a publicly accessible PDF URL:

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
              "link": "https://example.com/report.pdf",
              "filename": "Report.pdf"
            }
          }
        ]
      }
    ]
  }
}
```

**Note:** The URL must be publicly accessible (no authentication required).

---

## Error Codes Reference

| Code | Error | Solution |
|------|-------|----------|
| 190 | Invalid access token | Generate new token in Meta Developer Console |
| 131030 | Recipient not in allowed list | Add number in Meta Developer Console |
| 131031 | Business not verified | Complete business verification |
| 131047 | Re-engagement required | Only for regular messages, not templates |
| 131051 | Invalid parameter | Check request body format |
| 132000 | Template not found | Check template name and approval status |
| 132001 | Template paused | Template was paused by Meta |
| 132007 | Template format error | Components don't match template structure |

---

## Running the Application

```bash
# With specific PDF
python main.py 917385107084 "path/to/your/report.pdf"

# With default.pdf in project folder
python main.py 917385107084

# Generates dummy PDF if none specified
python main.py 917385107084
```

---

## Key Takeaways

1. **Template messages = Pre-approved by Meta** → Can be sent anytime
2. **PDF in header** = Document is part of the template, not a separate message
3. **Single API call** = Template + PDF delivered together
4. **No user action required** = Business initiates the conversation
5. **Each send needs upload** = PDF must be uploaded fresh each time (Media IDs expire)

---

## Resources

- [WhatsApp Cloud API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Message Templates Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)
- [Media Messages Guide](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages#media-messages)
- [Template Components](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages#template-object)
- [Conversation-Based Pricing](https://developers.facebook.com/docs/whatsapp/pricing)


┌────────────────────────────────────────────────────────────────────┐
│  STEP 1: You send template (pdf_sender)                           │
│                                                                    │
│      Business ──── pdf_sender ────> User                           │
│                                                                    │
│      ┌─────── MARKETING CONVERSATION OPENS (24 hrs) ───────┐       │
│      │  • You can send more templates                      │       │
│      │  • User can reply                                   │       │
│      └─────────────────────────────────────────────────────┘       │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│  STEP 2: User replies (optional but enables free messaging)       │
│                                                                    │
│      User ─────── "Thanks!" ──────> Business                       │
│                                                                    │
│      ┌─────── SERVICE CONVERSATION OPENS (24 hrs) ─────────┐       │
│      │  • You can send ANY message type for FREE:          │       │
│      │    - Text messages                                  │       │
│      │    - Images, videos, audio                          │       │
│      │    - Documents (PDFs, etc.)                         │       │
│      │    - Interactive buttons                            │       │
│      │  • No template needed!                              │       │
│      └─────────────────────────────────────────────────────┘       │
│                                                                    │
│  STEP 3: Free conversation within window                          │
│                                                                    │
│      Business ──── "Here's more info" ────> User  ✓                │
│      Business ──── 📄 another.pdf ────────> User  ✓                │
│      User ─────── "Question about PDF" ───> Business               │
│      Business ──── "Answer here..." ──────> User  ✓                │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

Summary:
Scenario	                 What You Can Send
Before any message	         Only template messages
After you send template	     Templates only (user hasn't replied)
After user replies	         Anything! Text, PDFs, images, etc.
After 24 hours of silence	 Only template messages again
So yes:
✅ User can reply to your PDF template
✅ Once user replies, you can send any message type (text, more PDFs, etc.)
✅ This creates a back-and-forth conversation
✅ The template message initiates the chat