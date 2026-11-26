# Build the Power BI report
Power BI Desktop on Windows is required. No native PBIX is included.
1. Import both CSVs; name tables Transactions and Customers. Set date to Date, IDs to Text, flags to Whole number, amounts to Decimal number.
2. Create a one-to-many relationship Customers[customer_id] to Transactions[customer_id], single direction.
3. Create each measure from measures.dax individually using New measure. Format rates as percentages and money as CAD.
4. Import theme.json via View > Themes > Browse for themes.
5. Create eight cards for the first eight measures, line chart Date (month) / Gross Loss, bar chart fraud_category / Gross Loss (exclude None), and bar chart province / Net Loss. Add date, province and channel slicers.
6. Validate unfiltered totals against the README and save as fraud_dashboard.pbix.
The PNG is a Python-generated preview, not a screenshot of Power BI.
