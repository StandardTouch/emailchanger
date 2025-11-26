import frappe
from frappe.email.queue import send


def set_hardcoded_sender(doc, method):
    comment_email_account = frappe.db.get_single_value('System Settings', 'comment_email_account')
    