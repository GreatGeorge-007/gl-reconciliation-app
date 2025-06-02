import pandas as pd
import random
from datetime import datetime, timedelta

def generate_dummy_data():
    branches = ['Lagos', 'Abuja', 'Kano', 'Port Harcourt', 'Enugu']
    gl_codes = ['1001', '2001', '3001', '1002', '2002']
    descriptions = {
        '1001': 'Cash Account',
        '2001': 'Payables',
        '3001': 'Equity Capital',
        '1002': 'Fixed Assets',
        '2002': 'Accrued Liabilities'
    }
    
    rows = []
    for _ in range(300):
        branch = random.choice(branches)
        gl_code = random.choice(gl_codes)
        date = datetime.now() - timedelta(days=random.randint(0, 30))
        debit = round(random.uniform(1000, 10000), 2)
        credit = 0 if random.random() > 0.5 else round(random.uniform(1000, 10000), 2)
        narration = f"Transaction on {gl_code}"
        journal_ref = f"JR-{random.randint(1000,9999)}"

        rows.append({
            'branch': branch,
            'gl_code': gl_code,
            'gl_description': descriptions[gl_code],
            'debit': debit,
            'credit': credit,
            'narration': narration,
            'journal_ref': journal_ref,
            'date': date.date()
        })

    return pd.DataFrame(rows)
