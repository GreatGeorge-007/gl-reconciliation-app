recon_logic.py
import pandas as pd

def classify_gl(gl_code):
    if gl_code.startswith('1'):
        return 'Asset'
    elif gl_code.startswith('2'):
        return 'Liability'
    elif gl_code.startswith('3'):
        return 'Equity'
    elif gl_code.startswith('4'):
        return 'Income'
    elif gl_code.startswith('5'):
        return 'Expense'
    return 'Other'

def reconcile_branch_gl(df, branch: str, start_date, end_date):
    df = df[(df['branch'] == branch) & (df['date'] >= start_date) & (df['date'] <= end_date)]
    df['net'] = df['debit'] - df['credit']
    df['gl_class'] = df['gl_code'].apply(classify_gl)

    balance_sheet = df.groupby(['gl_code', 'gl_description', 'gl_class']).agg({
        'net': 'sum'
    }).reset_index()

    makeup = df.groupby(['gl_code', 'journal_ref']).agg({
        'debit': 'sum',
        'credit': 'sum',
        'narration': 'first',
        'date': 'first'
    }).reset_index()

    reconciliation = []
    for gl_code in balance_sheet['gl_code']:
        balance = balance_sheet.loc[balance_sheet['gl_code'] == gl_code, 'net'].values[0]
        total_makeup = makeup.loc[makeup['gl_code'] == gl_code, ['debit', 'credit']].sum()
        net_makeup = total_makeup['debit'] - total_makeup['credit']
        match = abs(balance - net_makeup) < 0.01

        reconciliation.append({
            "gl_code": gl_code,
            "balance": balance,
            "makeup_total": net_makeup,
            "status": "MATCH" if match else "MISMATCH",
            "difference": round(balance - net_makeup, 2)
        })

    summary = pd.DataFrame(reconciliation)
    return balance_sheet, makeup, summary
