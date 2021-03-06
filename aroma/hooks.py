from . import __version__ as app_version

app_name = "aroma"
app_title = "Aroma"
app_publisher = "GreyCube Technologies"
app_description = "Customization for hall and conference rent company"
app_icon = "octicon octicon-device-camera"
app_color = "red"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/aroma/css/aroma.css"
# app_include_js = "/assets/aroma/js/aroma.js"
# app_include_js = ["/assets/aroma/js/help_link.js"]
# include js, css files in header of web template
# web_include_css = "/assets/aroma/css/aroma.css"
# web_include_js = "/assets/aroma/js/aroma.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "aroma/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Sales Order" : "public/js/sales_order.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------
# auto_cancel_exempted_doctypes = ["Function Sheet"]
# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "aroma.install.before_install"
# after_install = "aroma.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "aroma.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Quotation": {
		"on_submit": "aroma.booking_controller.create_booking"
	},
	"Sales Order": {
		"on_submit": "aroma.booking_controller.create_booking"
	}	,
	"Sales Invoice": {
		"on_submit": "aroma.booking_controller.mark_function_sheet_as_billed",
		"before_cancel": "aroma.booking_controller.remove_function_sheet_si_reference"
	}		
}
after_migrate = "aroma.booking_controller.after_migrations"
# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"15 00 * * *": [
			"aroma.booking_controller.delete_expired_booking_in_initial_state",
		]
	},	
}

# Testing
# -------

# before_tests = "aroma.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "aroma.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "aroma.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"aroma.auth.validate"
# ]

