# Activity-3
Planned Screens for Activity 3
- Login
- Dashboard
- Employees
- Business Days
- Sales
- Expense Types
- Expenses
- Merchandise Types
- Merchandise Purchases
- Payroll
- Shifts
- Invoices


NAV FLOW
- Login
  ↓
Dashboard
  ├── Employees
  │     └── Add / Edit Employee
  ├── Business Days
  ├── Sales
  │     └── Daily Sales Details
  ├── Expense Types
  ├── Expenses
  │     └── Add Expense
  ├── Merchandise Types
  ├── Merchandise Purchases
  │     └── Add Purchase
  ├── Payroll
  │     └── Payroll Details
  ├── Shifts
  │     └── Add / Edit Shift
  └── Invoices
        └── Invoice Details

  Dashboard Plan

Summary Cards:
- Total Sales → sales_daily
- Total Expenses → expenses
- Payroll Total → payroll
- Unpaid Invoices → invoices

Dashboard Sections:
- Recent Sales
- Recent Expenses
- Today's Shifts
- Invoice Status


1. Login

The Login screen is the entry point of the application. It allows authorized users to enter their username and password to access the store management system. This screen helps control access before users reach the main dashboard.

2. Dashboard

The Dashboard screen gives users a quick overview of the most important store information. It includes summary cards for total sales, total expenses, payroll total, and unpaid invoices, along with sections for recent sales, today’s shifts, recent expenses, and invoice status. This screen is designed to give managers a high-level summary of daily operations.

3. Employees

The Employees screen displays employee records and allows users to view, add, or edit employee information. It is used to manage employee data in the system and connects directly to the employees table.

4. Business Days

The Business Days screen shows records for store operating days. It includes information such as the date and day name, along with a details section for the selected record. This screen is based on the business_days table.

5. Sales

The Sales screen displays daily sales information. It includes summary sections for cash sales, credit sales, and total sales, as well as a table of sales records. This screen connects to the sales_daily table and helps users review store revenue activity.

6. Expense Types

The Expense Types screen lists the different categories of expenses used in the system. It allows users to view or manage expense type records and is connected to the expense_types table.

7. Expenses

The Expenses screen displays expense records and provides a section for entering new expenses. It also includes a summary area for viewing totals. This screen is based on the expenses table and helps track money leaving the business.

8. Merchandise Types

The Merchandise Types screen shows the categories of merchandise used in the store system. It includes a list of merchandise types, a details section, and a summary area. This screen maps to the merch_types table.

9. Merchandise Purchases

The Merchandise Purchases screen displays records of merchandise purchases and includes a form for adding new purchase entries. It also provides a totals section for purchase summaries. This screen is connected to the merch_purchases table.

10. Payroll

The Payroll screen is used to display payroll-related records. It includes summary cards for payroll information and a table of payroll entries by employee and date. This screen maps directly to the payroll table.

11. Shifts

The Shifts screen displays employee shift records, including clock-in and clock-out times. It also includes a form for adding or editing shifts and a summary section for shift-related information. This screen is based on the shifts table.

12. Invoices

The Invoices screen displays invoice records and provides summary information such as total invoices, paid invoices, and unpaid invoices. It is connected to the invoices table and helps users track invoice and payment status.
  
