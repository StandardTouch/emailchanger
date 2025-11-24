import frappe

def override_email_sender(email_obj):
    """Override sender for Project and Task to erpsupport@standardtouch.com"""
    try:
        # Log the email object for debugging
        frappe.log_error(
            f"Email Object: {email_obj.__dict__}", 
            "Email Routing Debug"
        )

        doctype = None
        if hasattr(email_obj, 'reference_doctype') and email_obj.reference_doctype:
            doctype = email_obj.reference_doctype
        elif hasattr(email_obj, 'communication') and email_obj.communication:
            # For mentions, reference_doctype might be on the linked Communication
            try:
                comm_doc = frappe.get_doc("Communication", email_obj.communication)
                if comm_doc and comm_doc.reference_doctype:
                    doctype = comm_doc.reference_doctype
                    frappe.log_error(f"Fetched Doctype from Communication: {doctype}", "Email Routing Debug")
            except Exception as e:
                frappe.log_error(f"Error fetching Communication: {str(e)}", "Email Routing Debug")
        elif hasattr(email_obj, 'doctype'):
            doctype = email_obj.doctype
        
        frappe.log_error(f"Detected Doctype: {doctype}", "Email Routing Debug")
        
        if doctype in ["Project", "Task"]:
            email_obj.sender = "erpsupport@standardtouch.com"
            email_obj.sender_name = "ERP Support"
            frappe.log_error(f"Overridden sender for {doctype}", "Email Routing Debug")
    except Exception as e:
        frappe.log_error(f"Email routing error: {str(e)}", "Email Routing")