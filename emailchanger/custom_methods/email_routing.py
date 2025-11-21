import frappe

def override_email_sender(email_obj):
    """Override sender for Project and Task to erpsupport@standardtouch.com"""
    try:
        doctype = None
        if hasattr(email_obj, 'doc') and email_obj.doc:
            doctype = email_obj.doc.doctype
        elif hasattr(email_obj, 'doctype'):
            doctype = email_obj.doctype
        
        if doctype in ["Project", "Task"]:
            email_obj.sender = "erpsupport@standardtouch.com"
            email_obj.sender_name = "ERP Support"
    except Exception as e:
        frappe.log_error(f"Email routing error: {str(e)}", "Email Routing")