# Modules
MODULES = [
    "Global – Tables (General information about the application)",
    "SD – Tables ( Sales & Distribution Module – Customization & Transaction Tables)",
    "MM – Tables ( Material Management – Purchase & Inventory Module) – Customization & Transaction Tables)",
]

# Tuples of (table, description, how to use the table)

GLOBAL_MODULE = [
    ("GL_COMPANY_C", "Define Company / Tenant Registration Table", ""),
    (
        "GL_PLANT_C",
        "Define Branch / Plant and Branch is assigned to the Company. Plant is under the Company code.",
        "",
    ),
    (
        "GL_DOCTYPE_C",
        "Define Sales Types, Purchase Types, Contract Types, Project Types. Customization of Tenant Business help of Documents",
        "",
    ),
    (
        "GL_SEARCH_QUERIES_M",
        "All Pick lists have the Search ID and Query and conditions from the Table and have the Search ID.",
        "Pick List Query Procedure, Views, Reports, Charts",
    ),
    (
        "GL_SEC_FUNCTIONS_S",
        "All screens from UI will be from the Table with Function Code.",
        "Transactions, Customizations, Configurations, User Rights, Reports, Charts",
    ),
    (
        "GL_BUSINESSAREA_C",
        "Define Business Area – The combination of Branch and Product division",
        "",
    ),
    ("GL_STORAGELOC_C", "Define Storage location (Ware House Location)", ""),
    ("GL_PURCHASEORG_C", "Define Purchase Organization in the Company", ""),
    (
        "GL_SALESAREA_C",
        "Define Sales Area (The Combination of Sales Organization, Dist. Channel, and Division)",
        "",
    ),
    ("GL_DISTCHANNEL_C", "Define Distribution Channel", ""),
    ("GL_DIVISION_C", "Define Division", ""),
    ("GL_SALESORG_C", "Define Sales Organization in the Company", ""),
    (
        "GL_PRICING_D",
        "Configuration of Pricing Procedure, Formulas Building, Pricing Conditions, Assigning the Pricing Procedure to Business Types",
        "",
    ),
    ("GL_NORANGE_C_H", "Define No Ranges of the Document types", ""),
    ("GL_SEC_USER_AUTH", "User Rights and Privileges", ""),
    ("GL_FYEAR_C", "Define Financial Year", ""),
    ("GL_CURRENCY_C", "Define Currency", ""),
]

SALES_AND_DISTRIBUTION_MODULE = [
    (
        "SD_CUSTACCGRP_C",
        "Define Customer Account Groups for Categorizing and Classifications of the Customers for the Business Types",
        "",
    ),
    (
        "FI_PAYTERM_C",
        "Define Payment Terms and assigning to the Customer and Sale Transaction",
        "",
    ),
    (
        "FI_PAYMENTMODE_C",
        "Define Payment Methods – Mode of Payment doing by Customers and company allowing methods",
        "",
    ),
    ("SD_CUST_CONTACT_M", "Customer Master - Contact Details of the Customer", ""),
    ("SD_CUSTACC_M", "Customer Master – Reconciliation Account – Sundry Debtors", ""),
    ("SD_CUSTBANK_M", "Customer Master – Customer Bank Account details", ""),
    (
        "SD_CUSTADD_M",
        "Customer Master – Customer Record with all the Master details",
        "",
    ),
    ("SD_CUSTPARTNER_C", "Customer Master – Customer Partner Functions assignment", ""),
    ("SD_CUSTSALES_M", "Customer Master – Sales Area wise Customers", ""),
    (
        "SD_QUOTATIONCONFIGURATION_C",
        "Sales Quotation – Type of Quotations and Configuration of Document will be configured",
        "",
    ),
    (
        "SD_QUOTATION_H",
        "Sales Quotation – Header details – Customer, Payment terms and Quotation Types",
        "",
    ),
    (
        "SD_QUOTATION_T",
        "Sales Quotation – Transaction Details – Line Item details, Pricing Details, and Quotation line item Value and Qty",
        "",
    ),
    ("SD_QUOTATION_TAX_T", "Sales Quotation – Line item wise tax details", ""),
    (
        "SD_ORDERCONFIGURATION_C",
        "Sales Order - Type of Sale Configuration by Document type",
        "",
    ),
    (
        "SD_ORDER_H",
        "Sales Order- Header Details – Order Type / Contract Type / Sales Type, Customer and Payment terms",
        "",
    ),
    (
        "SD_ORDER_T",
        "Sales Order – Transaction Details – Line Item wise details, Pricing and line item Value and Qty",
        "",
    ),
    ("SD_ORDER_TAX_T", "Sales Order – Line item wise Tax details", ""),
    ("SD_DELIVERYTYPE_C", "Delivery Type (Outbound type) Configuration", ""),
    (
        "SD_DLVCHALLAN_H",
        "Sales Delivery Challan (Out Bound Delivery)– Header Details – Type of Delivery, Customer and Shipment Location",
        "",
    ),
    (
        "SD_DLVCHALLAN_T",
        "Sales Delivery Challan (Out Bound Delivery) – Transaction Details – Line item, Qty and Batch details of Material",
        "",
    ),
    (
        "MM_MAT_TRANS_T",
        "Inventory Entry – Ref. to Out Bound Delivery. Stock will be reduced from Available stock",
        "",
    ),
    ("SD_BILLINGTYPE_C", "Billing Types Configuration", ""),
    (
        "SD_BILLING_H",
        "Sales Billing – Header Details – Customer, Billing Type and Payment Terms",
        "",
    ),
    (
        "SD_BILLING_T",
        "Sales Billing – Transaction Details – Line Item details, Qty, Value of Materials and Reference documents of Order, Delivery and Invoice details",
        "",
    ),
    ("SD_BILLING_TAX_T", "Sales Invoice – Line item wise Tax details", ""),
    (
        "FI_ACD_H",
        "Account Determination – Header details – Document Type, Financial Year, Post Period and Reference Document Type",
        "",
    ),
    (
        "FI_ACD_T",
        "Account Determination by Line item wise – Transaction details and Account Postings",
        "",
    ),
    (
        "FI_CUSTOP_IDX",
        "Customer Index – Customer current Running Balance and all customer ledger Postings",
        "",
    ),
]

MATERIAL_MANAGEMENT_MODULE = (
    (
        "MM_MATERIAL_TYPE_C",
        "Industry Specific - Business Type indicating by the Material Type. Tenant have multiple Material Types which have group of Products and Services.",
        "",
    ),
    (
        "MM_MATERIAL_GROUP_C",
        "Group of Products and Services which under the similar and type of Products",
        "",
    ),
    (
        "MM_MATERIAL_SUBGROUP_C",
        "Multiple sub group of Products and services under Material Groups",
        "",
    ),
    (
        "MM_MATERIAL_BASIC_M",
        "Material Master Record - Material Basic and Standard info Record",
        "",
    ),
    ("MM_MATERIAL_INVENTORY_M", "Material – Inventory Management Info Record", ""),
    ("MM_MATERIAL_PURCHASE_M", "Material Master – Purchase View Info Record", ""),
    ("MM_MATERIAL_SALES_M", "Material Master – Sales View Info", ""),
    ("MM_MATERIAL_SERVICES_M", "Material Master – Service View Info", ""),
    (
        "MM_MATERIAL_DEPENDENTITEMS_M",
        "Material Master – Dependent Items Information",
        "",
    ),
    ("MM_MATERIAL_BOM_M", "Material Master – Bills of Material", ""),
    (
        "MM_VENDOR_ACGP_C",
        "Vendor Account Group maintaining for Vendor Master Records classifications",
        "",
    ),
    ("MM_VENDOR_ADD_M", "Vendor Master Record for General and Address", ""),
    ("MM_VENDOR_ACC_M", "Vendor Reconciliation – Sundry Creditors", ""),
    ("MM_VENDOR_BANK_M", "Vendor Bank Account Details", ""),
    ("MM_VENDOR_CONTACTPERSON_M", "Vendor Master – Contact Info", ""),
    (
        "MM_DOCUMENTCONFIG_C",
        "Purchase Type will be configured by Purchase document Type, Order types, Material Movement types, Goods Receipts types and Billing type will be configured",
        "",
    ),
    (
        "MM_PUR_PO_H",
        "Purchase Order – Header details – Vendor / Supplier, Payment terms and Methods",
        "",
    ),
    ("MM_PUR_PO_T", "Purchase Order – Line Item details", ""),
    (
        "MM_BATCHSTK_T",
        "If, Material is Batch Managed, Material stock will be displayed by Batch no",
        "",
    ),
    (
        "MM_GRPRICING_T",
        "Goods movement and Pricing details table for different Goods movements",
        "",
    ),
    ("FI_VENOP_IDX", "Vendor Running Balance and Index details", ""),
    (
        "FI_BANKOP_IDX",
        "Company Bank accounts Reconciliation process and determination of Account Postings and Index details",
        "",
    ),
    (
        "FI_DOCTYPECONFIG_C",
        "All Financial documents will be configured in the Table by document types. All type of Credit Memo, Debit Memo, Receipts and Payments, Opening Balances of documents will be configured based on Reconciliation Group",
        "",
    ),
    ("FI_BANK_C", "Define Bank", ""),
    (
        "FI_BANKACCTYPE_C",
        "Define Bank Account type and Registered Accounts and assigned to the Reconciliation",
        "",
    ),
    (
        "FI_ACCGRP_C",
        "Define GL Accounts Group and Account Group will be assign to any one of Group type.",
        "A=Assets, I = Incomes, E= Expenditures, L=Liabilities",
    ),
    ("FI_COA_C_T", "Define Chart of Accounts under any one of defined Group", ""),
    ("FI_PERIODPOSTING_C", "Posting period Open and Close in the Financial Year", ""),
    ("FI_CUSTBALANCE_H", "Customer Running Balance – Dr / Cr", ""),
    ("FI_VENDBALANCE_H", "Vendor Running Balance – Dr / Cr", ""),
    ("FI_BANKBALANCE_H", "Company Bank Balance – Dr / Cr", ""),
    ("FI_GLBALANCE_H", "GL account Balance", ""),
)

# List of (table, description, usage, module)
TABLES = [
    (name, description, usage, MODULES[0])
    for (name, description, usage) in GLOBAL_MODULE
]
TABLES += [
    (name, description, usage, MODULES[1])
    for (name, description, usage) in SALES_AND_DISTRIBUTION_MODULE
]
TABLES += [
    (name, description, usage, MODULES[2])
    for (name, description, usage) in MATERIAL_MANAGEMENT_MODULE
]
