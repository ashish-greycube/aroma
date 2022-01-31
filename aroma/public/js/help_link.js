frappe.provide("frappe.help.help_links");
console.log('inside')
const docsUrl = "https://erpnext.com/docs/";

frappe.help.help_links["Form/Rename Tool"] = [
	{
		label: "Bulk Rename",
		url: docsUrl + "user/manual/en/using-erpnext/articles/bulk-rename",
	},
	{
		label: "Google",
		url: "https://google.com",
	},	
];
