import pandas as pd
from io import BytesIO

def export_excel_report(balance_sheet, summary, makeup=None):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        balance_sheet.to_excel(writer, sheet_name='Balance Sheet', index=False)
        summary.to_excel(writer, sheet_name='Reconciliation Summary', index=False)
        if makeup is not None:
            makeup.to_excel(writer, sheet_name='GL Makeup', index=False)

        workbook = writer.book
        format_header = workbook.add_format({'bold': True, 'bg_color': '#DCE6F1'})
        for sheet in ['Balance Sheet', 'Reconciliation Summary', 'GL Makeup']:
            try:
                worksheet = writer.sheets[sheet]
                worksheet.set_row(0, None, format_header)
                worksheet.autofilter(0, 0, 0, 6)
            except:
                continue

    output.seek(0)
    return output
