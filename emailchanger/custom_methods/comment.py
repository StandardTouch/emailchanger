"""
emailchanger/custom_methods/comment.py

Correct approach: Modify the 'sender' field in Email Queue for mention emails
"""

import frappe


def update_comment_mention_email_account(doc, method=None):
    """
    Intercept Email Queue before_send and change sender if it's a mention
    
    The 'sender' field in Email Queue is what determines which email address sends it
    """
    
    try:
        frappe.logger().info(f"[EmailChanger] Processing email: {doc.name}")
        frappe.logger().info(f"[EmailChanger] Subject: {doc.subject}")
        frappe.logger().info(f"[EmailChanger] Current sender: {doc.sender}")
        
        # Check if this is a mention email
        is_mention = False
        
        # Method 1: Check subject for "mention"
        if doc.subject and "mention" in doc.subject.lower():
            frappe.logger().info(f"[EmailChanger] Found 'mention' in subject")
            is_mention = True
        
        # Method 2: Check message content for "mention"
        if not is_mention and doc.message and "mention" in doc.message.lower():
            frappe.logger().info(f"[EmailChanger] Found 'mention' in message")
            is_mention = True
        
        # Method 3: Check communication field
        if not is_mention and doc.communication:
            frappe.logger().info(f"[EmailChanger] Has communication field - likely a mention")
            is_mention = True
        
        if not is_mention:
            frappe.logger().info(f"[EmailChanger] Not a mention email - skipping")
            return
        
        frappe.logger().info(f"[EmailChanger] This is a mention email!")
        
        # Get your custom email account
        # CHANGE THIS TO YOUR ACTUAL EMAIL ACCOUNT!
        custom_email_account = "ERP Support"
        
        frappe.logger().info(f"[EmailChanger] Custom account to use: {custom_email_account}")
        
        # Get the email address of the custom account
        email_account = frappe.db.get_value(
            'Email Account',
            custom_email_account,
            ['email_id', 'disabled'],
            as_dict=True
        )
        
        if not email_account:
            frappe.logger().error(f"[EmailChanger] Email account '{custom_email_account}' not found!")
            return
        
        if email_account.disabled:
            frappe.logger().error(f"[EmailChanger] Email account '{custom_email_account}' is disabled!")
            return
        
        custom_email_address = email_account.email_id
        
        # Change the sender field!
        frappe.logger().info(f"[EmailChanger] Changing sender from '{doc.sender}' to '{custom_email_address}'")
        doc.sender = custom_email_address
        
        frappe.logger().info(f"[EmailChanger] SUCCESS! Email will be sent from: {doc.sender}")
        
    except Exception as e:
        frappe.logger().error(f"[EmailChanger] Error: {str(e)}")
        import traceback
        frappe.logger().error(traceback.format_exc())