"""
emailchanger/custom_methods/comment.py

Alternative approach: Read config from a custom DocType instead of site_config.json
This works on Frappe Cloud without needing to contact support.
"""

import frappe


def update_comment_mention_email_account(doc, method=None):
    """Change email account for mention notifications"""
    
    try:
        # Check if this is a mention email
        if not doc.subject or 'mention' not in doc.subject.lower():
            return
        
        # Get custom email account from DocType record (EmailChanger Settings)
        settings = frappe.get_doc('EmailChanger Settings')
        custom_email_account = settings.comment_email_account
        
        if not custom_email_account:
            # No custom account configured
            return
        
        # Verify account exists and is enabled
        email_account = frappe.db.get_value(
            'Email Account',
            custom_email_account,
            ['name', 'disabled'],
            as_dict=True
        )
        
        if not email_account or email_account.disabled:
            return
        
        # Update email account
        doc.email_account = custom_email_account
        
    except frappe.DoesNotExistError:
        # Settings record doesn't exist yet - do nothing
        return
    except Exception as e:
        frappe.log_error(f"Error updating email account: {str(e)}")