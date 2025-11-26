"""
emailchanger/custom_methods/comment.py - DEBUG VERSION

This version logs everything so you can see what's happening
"""

import frappe


def update_comment_mention_email_account(doc, method=None):
    """Change email account for mention notifications - DEBUG VERSION"""
    
    try:
        frappe.logger().info(f"[EmailChanger] Hook triggered!")
        frappe.logger().info(f"[EmailChanger] Email subject: {doc.subject}")
        frappe.logger().info(f"[EmailChanger] Email account: {doc.email_account}")
        
        # Check if this is a mention email
        if not doc.subject or 'mention' not in doc.subject.lower():
            frappe.logger().info(f"[EmailChanger] Not a mention email - skipping")
            return
        
        frappe.logger().info(f"[EmailChanger] This is a mention email!")
        
        try:
            # Get custom email account from DocType
            settings = frappe.get_doc('EmailChanger Settings')
            custom_email_account = settings.comment_email_account
            frappe.logger().info(f"[EmailChanger] Settings found! Custom account: {custom_email_account}")
            
        except frappe.DoesNotExistError:
            frappe.logger().error(f"[EmailChanger] EmailChanger Settings DocType not found!")
            return
        
        if not custom_email_account:
            frappe.logger().info(f"[EmailChanger] No custom account configured in settings")
            return
        
        # Verify account exists and is enabled
        email_account = frappe.db.get_value(
            'Email Account',
            custom_email_account,
            ['name', 'disabled'],
            as_dict=True
        )
        
        frappe.logger().info(f"[EmailChanger] Email account lookup result: {email_account}")
        
        if not email_account:
            frappe.logger().error(f"[EmailChanger] Email account '{custom_email_account}' not found!")
            return
        
        if email_account.disabled:
            frappe.logger().error(f"[EmailChanger] Email account '{custom_email_account}' is disabled!")
            return
        
        # Update email account
        frappe.logger().info(f"[EmailChanger] Updating email account from {doc.email_account} to {custom_email_account}")
        doc.email_account = custom_email_account
        frappe.logger().info(f"[EmailChanger] Email account updated successfully!")
        
    except Exception as e:
        frappe.logger().error(f"[EmailChanger] Error: {str(e)}")
        import traceback
        frappe.logger().error(traceback.format_exc())