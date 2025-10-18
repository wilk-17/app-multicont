# Discrepancy AST Report

## Assignment
- entity_fields: ['id', 'employee_id', 'item_id', 'assigned_date']
- legacy_model_fields: ['id', 'employee_id', 'item_id', 'assigned_date']
- api_files_referencing: ['assignment_api']
- handler_files_candidate: []

## Branch
- entity_fields: ['id', 'organization_id', 'city_id']
- legacy_model_fields: ['id', 'organization_id', 'city_id']
- api_files_referencing: []
- handler_files_candidate: []

## City
- entity_fields: ['id', 'description', 'code', 'state_id']
- legacy_model_fields: ['id', 'description', 'code', 'state_id']
- api_files_referencing: []
- handler_files_candidate: []

## Employee
- entity_fields: ['id', 'person_id', 'branch_id']
- legacy_model_fields: ['id', 'person_id', 'branch_id']
- api_files_referencing: []
- handler_files_candidate: []

## InventoryItem
- entity_fields: ['id', 'name', 'description', 'quantity', 'price', 'category_id']
- legacy_model_fields: ['id', 'name', 'description', 'quantity', 'price', 'category_id']
- api_files_referencing: ['inventory_item_api']
- handler_files_candidate: []

## Invoice
- entity_fields: ['id', 'sales_order_id', 'quotation_line_id', 'date', 'total']
- legacy_model_fields: ['id', 'sales_order_id', 'quotation_line_id', 'date', 'total']
- api_files_referencing: []
- handler_files_candidate: []

## InvoiceItem
- entity_fields: ['id', 'invoice_id', 'item_id', 'quantity', 'price']
- legacy_model_fields: ['id', 'invoice_id', 'item_id', 'quantity', 'price']
- api_files_referencing: []
- handler_files_candidate: []

## ItemCategory
- entity_fields: ['id', 'name', 'description']
- legacy_model_fields: ['id', 'name']
- api_files_referencing: []
- handler_files_candidate: []

## Organization
- entity_fields: ['id', 'historical_name', 'current_name']
- legacy_model_fields: ['id', 'historical_name', 'current_name']
- api_files_referencing: []
- handler_files_candidate: []

## Permission
- entity_fields: ['id', 'name']
- legacy_model_fields: ['id', 'name']
- api_files_referencing: []
- handler_files_candidate: []

## Person
- entity_fields: ['id', 'dni', 'first_name', 'last_name', 'address', 'phone', 'city_id', 'status', 'creation_date', 'update_date']
- legacy_model_fields: ['id', 'dni', 'first_name', 'last_name', 'address', 'phone', 'city_id']
- api_files_referencing: []
- handler_files_candidate: ['assignment_handler', 'branch_handler', 'city_handler', 'employee_handler', 'inventory_item_handler', 'invoice_handler', 'invoice_item_handler', 'item_category_handler', 'organization_handler', 'permission_handler', 'person_handler', 'quotation_line_handler', 'quote_handler', 'quote_item_handler', 'role_handler', 'sales_order_handler', 'sales_order_item_handler', 'state_handler', 'user_handler', 'user_role_handler']

## QuotationLine
- entity_fields: ['id', 'quote_id', 'description', 'quantity', 'price', 'item_id']
- legacy_model_fields: ['id', 'quote_id', 'description', 'quantity', 'price', 'item_id']
- api_files_referencing: []
- handler_files_candidate: []

## Quote
- entity_fields: ['id', 'customer_name', 'date', 'total']
- legacy_model_fields: ['id', 'customer_name', 'date', 'total']
- api_files_referencing: ['quote_api']
- handler_files_candidate: []

## QuoteItem
- entity_fields: ['id', 'quote_id', 'item_id', 'quantity']
- legacy_model_fields: ['id', 'quote_id', 'item_id', 'quantity']
- api_files_referencing: []
- handler_files_candidate: []

## Role
- entity_fields: ['id', 'name']
- legacy_model_fields: ['id', 'name']
- api_files_referencing: []
- handler_files_candidate: []

## SalesOrder
- entity_fields: ['id', 'quote_id', 'date', 'total']
- legacy_model_fields: ['id', 'quote_id', 'date', 'total']
- api_files_referencing: ['sales_order_api']
- handler_files_candidate: []

## SalesOrderItem
- entity_fields: ['id', 'sales_order_id', 'item_id', 'quantity']
- legacy_model_fields: ['id', 'sales_order_id', 'item_id', 'quantity']
- api_files_referencing: []
- handler_files_candidate: []

## State
- entity_fields: ['id', 'description', 'code']
- legacy_model_fields: ['id', 'description', 'code']
- api_files_referencing: []
- handler_files_candidate: []

## User
- entity_fields: ['id', 'username', 'password', 'role_id']
- legacy_model_fields: ['id', 'username', 'password', 'role_id']
- api_files_referencing: []
- handler_files_candidate: ['user_handler']

## UserRole
- entity_fields: ['id', 'user_id', 'role_id', 'creation_date']
- legacy_model_fields: ['id', 'user_id', 'role_id']
- api_files_referencing: []
- handler_files_candidate: []

## __init__
- entity_fields: []
- legacy_model_fields: []
- api_files_referencing: []
- handler_files_candidate: []
