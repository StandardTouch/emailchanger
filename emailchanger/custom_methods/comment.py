import frappe

def set_hardcoded_sender(doc, method):
	frappe.local.outgoing_email_account = "erpsupport@standardtouch.com"