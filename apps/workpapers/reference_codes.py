# ============================================================
# reference_codes.py
# Predefined audit reference codes with structured
# audit programme procedures
# ============================================================

REFERENCE_CODES = [
    # Planning
    ('A100', 'A100 — Engagement Letter & Terms'),
    ('A110', 'A110 — Audit Planning Memorandum'),
    ('A120', 'A120 — Understanding the Client Business'),
    ('A130', 'A130 — Prior Year Review & Adjustments'),
    ('A140', 'A140 — Preliminary Analytical Review'),
    ('A150', 'A150 — Materiality Calculation'),
    ('A160', 'A160 — Audit Team & Responsibilities'),

    # Risk Assessment
    ('B100', 'B100 — Risk Assessment Matrix'),
    ('B110', 'B110 — Inherent Risk Assessment'),
    ('B120', 'B120 — Control Risk Assessment'),
    ('B130', 'B130 — Fraud Risk Assessment'),
    ('B140', 'B140 — Related Party Identification'),

    # Internal Controls
    ('C100', 'C100 — Internal Controls Overview'),
    ('C110', 'C110 — Revenue Controls Walkthrough'),
    ('C120', 'C120 — Cash & Bank Controls'),
    ('C130', 'C130 — Payroll Controls'),
    ('C140', 'C140 — Procurement Controls'),
    ('C150', 'C150 — IT General Controls'),
    ('C160', 'C160 — Internal Control Questionnaire'),

    # Cash & Bank
    ('D100', 'D100 — Bank Confirmation Letters'),
    ('D110', 'D110 — Bank Reconciliation Testing'),
    ('D120', 'D120 — Cash Count'),
    ('D130', 'D130 — Petty Cash Testing'),
    ('D140', 'D140 — Bank Transfers Testing'),

    # Revenue & Receivables
    ('E100', 'E100 — Revenue Analytical Review'),
    ('E110', 'E110 — Revenue Cut-off Testing'),
    ('E120', 'E120 — Sales Invoice Testing'),
    ('E130', 'E130 — Accounts Receivable Confirmation'),
    ('E140', 'E140 — Bad Debt Provision Review'),
    ('E150', 'E150 — Revenue Recognition Policy Review'),

    # Inventory
    ('F100', 'F100 — Inventory Count Attendance'),
    ('F110', 'F110 — Inventory Valuation Testing'),
    ('F120', 'F120 — Inventory Obsolescence Review'),
    ('F130', 'F130 — Cost of Sales Testing'),
    ('F140', 'F140 — Inventory Cut-off Testing'),

    # Payroll
    ('G100', 'G100 — Payroll Analytical Review'),
    ('G110', 'G110 — Payroll Testing — Completeness'),
    ('G120', 'G120 — PAYE & NSSF Compliance'),
    ('G130', 'G130 — Staff Costs Reconciliation'),
    ('G140', 'G140 — Director Remuneration Review'),

    # Fixed Assets
    ('H100', 'H100 — Fixed Asset Register Review'),
    ('H110', 'H110 — Additions Testing'),
    ('H120', 'H120 — Disposals Testing'),
    ('H130', 'H130 — Depreciation Review'),
    ('H140', 'H140 — Physical Verification'),

    # Payables & Liabilities
    ('I100', 'I100 — Accounts Payable Testing'),
    ('I110', 'I110 — Supplier Statement Reconciliation'),
    ('I120', 'I120 — Accruals & Provisions Review'),
    ('I130', 'I130 — Long-term Liabilities Review'),
    ('I140', 'I140 — Cut-off Testing — Payables'),

    # Completion
    ('Z100', 'Z100 — Subsequent Events Review'),
    ('Z110', 'Z110 — Going Concern Assessment'),
    ('Z120', 'Z120 — Summary of Unadjusted Differences'),
    ('Z130', 'Z130 — Audit Completion Checklist'),
    ('Z140', 'Z140 — Management Representation Letter'),
    ('Z150', 'Z150 — Final Analytical Review'),
]

REFERENCE_TITLES = {
    'A100': 'Engagement Letter & Terms of Reference',
    'A110': 'Audit Planning Memorandum',
    'A120': 'Understanding the Client Business & Environment',
    'A130': 'Prior Year Adjustments & Opening Balances Review',
    'A140': 'Preliminary Analytical Review',
    'A150': 'Materiality Calculation & Justification',
    'A160': 'Audit Team Composition & Responsibilities',
    'B100': 'Overall Risk Assessment Matrix',
    'B110': 'Inherent Risk Assessment by Area',
    'B120': 'Control Risk Assessment',
    'B130': 'Fraud Risk Assessment',
    'B140': 'Related Party Identification & Transactions',
    'C100': 'Internal Controls — Overview & Strategy',
    'C110': 'Revenue Controls — Walkthrough & Testing',
    'C120': 'Cash & Bank Controls — Walkthrough',
    'C130': 'Payroll Controls — Walkthrough',
    'C140': 'Procurement & Payments Controls',
    'C150': 'IT General Controls Assessment',
    'C160': 'Internal Control Questionnaire',
    'D100': 'Bank Confirmation Letters',
    'D110': 'Bank Reconciliation Testing',
    'D120': 'Cash Count & Verification',
    'D130': 'Petty Cash Testing',
    'D140': 'Bank Transfers & Intercompany Testing',
    'E100': 'Revenue Analytical Procedures',
    'E110': 'Revenue Cut-off Testing',
    'E120': 'Sales Invoice Testing & Tracing',
    'E130': 'Accounts Receivable Confirmation',
    'E140': 'Bad Debt Provision & Recoverability Review',
    'E150': 'Revenue Recognition Policy Review',
    'F100': 'Inventory Count Attendance',
    'F110': 'Inventory Valuation Testing',
    'F120': 'Inventory Obsolescence Review',
    'F130': 'Cost of Sales Testing',
    'F140': 'Inventory Cut-off Testing',
    'G100': 'Payroll Analytical Review',
    'G110': 'Payroll Testing — Completeness & Accuracy',
    'G120': 'PAYE & NSSF Statutory Compliance',
    'G130': 'Staff Costs Reconciliation',
    'G140': 'Director Remuneration Review',
    'H100': 'Fixed Asset Register Review',
    'H110': 'Capital Additions Testing',
    'H120': 'Disposals Testing',
    'H130': 'Depreciation Calculation Review',
    'H140': 'Physical Verification of Fixed Assets',
    'I100': 'Accounts Payable Testing',
    'I110': 'Supplier Statement Reconciliation',
    'I120': 'Accruals & Provisions Review',
    'I130': 'Long-term Liabilities Review',
    'I140': 'Cut-off Testing — Payables',
    'Z100': 'Subsequent Events Review',
    'Z110': 'Going Concern Assessment',
    'Z120': 'Summary of Unadjusted Differences',
    'Z130': 'Audit Completion Checklist',
    'Z140': 'Management Representation Letter',
    'Z150': 'Final Analytical Review',
}

# ============================================================
# STRUCTURED AUDIT PROGRAMMES
# Each programme is a list of procedure dictionaries
# Each procedure has:
#   - id: unique identifier for the field
#   - title: procedure name
#   - description: what the auditor must do
#   - result_type: 'text', 'textarea', 'select', 'number'
#   - options: list of options if result_type is 'select'
# ============================================================
AUDIT_PROGRAMMES = {

    'A': [
        {
            'id': 'engagement_letter',
            'title': '1. Engagement Letter',
            'description': 'Review the engagement letter and confirm terms of engagement, scope, and responsibilities are agreed with management.',
            'result_type': 'textarea',
        },
        {
            'id': 'understanding_entity',
            'title': '2. Understanding the Entity',
            'description': 'Document understanding of the client\'s business, industry, regulatory environment and key risk areas.',
            'result_type': 'textarea',
        },
        {
            'id': 'prior_year_review',
            'title': '3. Prior Year Review',
            'description': 'Review prior year financial statements and audit findings. Note any adjustments or matters carried forward.',
            'result_type': 'textarea',
        },
        {
            'id': 'preliminary_analytical',
            'title': '4. Preliminary Analytical Review',
            'description': 'Perform preliminary analytical procedures to identify areas of potential risk or unusual movements.',
            'result_type': 'textarea',
        },
        {
            'id': 'planning_conclusion',
            'title': 'Overall Planning Conclusion',
            'description': 'State your overall conclusion on the planning phase.',
            'result_type': 'select',
            'options': ['Satisfactory', 'Satisfactory with issues noted', 'Unsatisfactory'],
        },
    ],

    'B': [
        {
            'id': 'inherent_risk',
            'title': '1. Inherent Risk Assessment',
            'description': 'For each significant account assess the inherent risk considering complexity, volume, history of errors and management judgement.',
            'result_type': 'textarea',
        },
        {
            'id': 'control_risk',
            'title': '2. Control Risk Assessment',
            'description': 'Evaluate the design and implementation of internal controls over each significant risk area.',
            'result_type': 'textarea',
        },
        {
            'id': 'fraud_risk',
            'title': '3. Fraud Risk Assessment',
            'description': 'Consider fraud risk factors including incentives, opportunities and attitudes. Document any fraud risk indicators.',
            'result_type': 'textarea',
        },
        {
            'id': 'related_parties',
            'title': '4. Related Parties',
            'description': 'Identify all related parties and related party transactions. Assess completeness of disclosures.',
            'result_type': 'textarea',
        },
        {
            'id': 'overall_risk_level',
            'title': 'Overall Risk Level',
            'description': 'State the overall engagement risk level.',
            'result_type': 'select',
            'options': ['High', 'Moderate', 'Low'],
        },
    ],

    'C': [
        {
            'id': 'controls_identified',
            'title': '1. Key Controls Identified',
            'description': 'Identify and list the key controls designed to prevent or detect material misstatements in this area.',
            'result_type': 'textarea',
        },
        {
            'id': 'walkthrough',
            'title': '2. Walkthrough Testing',
            'description': 'Select one transaction and trace it from initiation through to recording to confirm controls are in place. Document the transaction selected and results.',
            'result_type': 'textarea',
        },
        {
            'id': 'sample_size',
            'title': '3. Control Testing — Sample Size',
            'description': 'State the sample size used for control testing.',
            'result_type': 'number',
        },
        {
            'id': 'exceptions_found',
            'title': '4. Exceptions Found',
            'description': 'Document any exceptions or deviations found during control testing.',
            'result_type': 'textarea',
        },
        {
            'id': 'controls_effective',
            'title': '5. Are Controls Operating Effectively?',
            'description': 'State your conclusion on control effectiveness.',
            'result_type': 'select',
            'options': ['Yes — controls are effective', 'Partially — some weaknesses noted', 'No — controls are ineffective'],
        },
        {
            'id': 'impact_on_substantive',
            'title': '6. Impact on Substantive Procedures',
            'description': 'Describe how the control testing results affect the planned substantive procedures.',
            'result_type': 'textarea',
        },
    ],

    'D': [
        {
            'id': 'banks_confirmed',
            'title': '1. Bank Confirmations',
            'description': 'Send confirmation letters to all banks. List all banks confirmed and reconcile responses to the general ledger balance.',
            'result_type': 'textarea',
        },
        {
            'id': 'bank_balance',
            'title': '2. Bank Balance per Statement (UGX)',
            'description': 'Enter the total bank balance per bank statement at year end.',
            'result_type': 'number',
        },
        {
            'id': 'book_balance',
            'title': '3. Bank Balance per Ledger (UGX)',
            'description': 'Enter the total bank balance per the general ledger at year end.',
            'result_type': 'number',
        },
        {
            'id': 'reconciling_items',
            'title': '4. Reconciling Items',
            'description': 'List and explain all reconciling items between the bank statement and general ledger.',
            'result_type': 'textarea',
        },
        {
            'id': 'unusual_items',
            'title': '5. Unusual or Large Transactions',
            'description': 'Note any unusual or large transactions identified during bank statement review.',
            'result_type': 'textarea',
        },
        {
            'id': 'cutoff_result',
            'title': '6. Cut-off Testing Result',
            'description': 'Describe the results of cash cut-off testing around year end.',
            'result_type': 'textarea',
        },
        {
            'id': 'cash_conclusion',
            'title': 'Overall Cash Conclusion',
            'description': 'State your conclusion on the cash and bank balance.',
            'result_type': 'select',
            'options': ['Cash balance is fairly stated', 'Cash balance is fairly stated with exceptions noted', 'Cash balance is not fairly stated'],
        },
    ],

    'E': [
        {
            'id': 'current_year_revenue',
            'title': '1. Current Year Revenue (UGX)',
            'description': 'Enter total revenue for the current year.',
            'result_type': 'number',
        },
        {
            'id': 'prior_year_revenue',
            'title': '2. Prior Year Revenue (UGX)',
            'description': 'Enter total revenue for the prior year.',
            'result_type': 'number',
        },
        {
            'id': 'variance_explanation',
            'title': '3. Variance Explanation',
            'description': 'Explain the movement between current and prior year revenue. Is the movement expected and supported?',
            'result_type': 'textarea',
        },
        {
            'id': 'cutoff_sample_size',
            'title': '4. Cut-off Testing — Sample Size',
            'description': 'State the number of invoices tested before and after year end.',
            'result_type': 'number',
        },
        {
            'id': 'cutoff_exceptions',
            'title': '5. Cut-off Testing — Exceptions',
            'description': 'Document any invoices recorded in the wrong period. Include invoice numbers and amounts.',
            'result_type': 'textarea',
        },
        {
            'id': 'invoice_sample_size',
            'title': '6. Invoice Testing — Sample Size',
            'description': 'State the number of sales invoices tested.',
            'result_type': 'number',
        },
        {
            'id': 'invoice_exceptions',
            'title': '7. Invoice Testing — Exceptions',
            'description': 'Document any invoices that could not be agreed to supporting documents.',
            'result_type': 'textarea',
        },
        {
            'id': 'receivables_confirmed',
            'title': '8. Receivables Confirmations',
            'description': 'Describe confirmation procedures performed and responses received.',
            'result_type': 'textarea',
        },
        {
            'id': 'revenue_conclusion',
            'title': 'Overall Revenue Conclusion',
            'description': 'State your conclusion on revenue.',
            'result_type': 'select',
            'options': ['Revenue is fairly stated', 'Revenue is fairly stated with exceptions noted', 'Revenue is not fairly stated'],
        },
    ],

    'F': [
        {
            'id': 'count_attendance',
            'title': '1. Inventory Count Attendance',
            'description': 'Describe the physical count attended. Note date, location, and counting procedures observed.',
            'result_type': 'textarea',
        },
        {
            'id': 'test_counts',
            'title': '2. Test Counts Performed',
            'description': 'Document the test counts performed during the physical count.',
            'result_type': 'number',
        },
        {
            'id': 'count_exceptions',
            'title': '3. Count Exceptions',
            'description': 'Document any differences between count sheets and physical stock.',
            'result_type': 'textarea',
        },
        {
            'id': 'inventory_value',
            'title': '4. Total Inventory Value (UGX)',
            'description': 'Enter the total inventory value per the inventory listing.',
            'result_type': 'number',
        },
        {
            'id': 'valuation_exceptions',
            'title': '5. Valuation Testing Exceptions',
            'description': 'Document any items where cost exceeds net realisable value.',
            'result_type': 'textarea',
        },
        {
            'id': 'obsolescence',
            'title': '6. Obsolescence Assessment',
            'description': 'Describe slow-moving or obsolete stock identified and adequacy of provision.',
            'result_type': 'textarea',
        },
        {
            'id': 'inventory_conclusion',
            'title': 'Overall Inventory Conclusion',
            'description': 'State your conclusion on inventory.',
            'result_type': 'select',
            'options': ['Inventory is fairly stated', 'Inventory is fairly stated with exceptions noted', 'Inventory is not fairly stated'],
        },
    ],

    'G': [
        {
            'id': 'current_year_payroll',
            'title': '1. Current Year Payroll Cost (UGX)',
            'description': 'Enter total payroll cost for the current year.',
            'result_type': 'number',
        },
        {
            'id': 'prior_year_payroll',
            'title': '2. Prior Year Payroll Cost (UGX)',
            'description': 'Enter total payroll cost for the prior year.',
            'result_type': 'number',
        },
        {
            'id': 'payroll_variance',
            'title': '3. Variance Explanation',
            'description': 'Explain the movement in payroll cost between years. Is it consistent with headcount changes?',
            'result_type': 'textarea',
        },
        {
            'id': 'payroll_sample',
            'title': '4. Payroll Testing — Sample Size',
            'description': 'State the number of employees tested.',
            'result_type': 'number',
        },
        {
            'id': 'payroll_exceptions',
            'title': '5. Payroll Testing — Exceptions',
            'description': 'Document any exceptions found during payroll testing.',
            'result_type': 'textarea',
        },
        {
            'id': 'paye_compliance',
            'title': '6. PAYE & NSSF Compliance',
            'description': 'Confirm PAYE and NSSF deductions are correctly calculated and remitted on time. Note any late remittances.',
            'result_type': 'textarea',
        },
        {
            'id': 'payroll_conclusion',
            'title': 'Overall Payroll Conclusion',
            'description': 'State your conclusion on payroll.',
            'result_type': 'select',
            'options': ['Payroll is fairly stated', 'Payroll is fairly stated with exceptions noted', 'Payroll is not fairly stated'],
        },
    ],

    'H': [
        {
            'id': 'additions_tested',
            'title': '1. Additions Tested (UGX)',
            'description': 'Enter the total value of additions tested.',
            'result_type': 'number',
        },
        {
            'id': 'additions_exceptions',
            'title': '2. Additions Testing Exceptions',
            'description': 'Document any additions that could not be agreed to invoices or authorisation.',
            'result_type': 'textarea',
        },
        {
            'id': 'disposals_tested',
            'title': '3. Disposals Tested',
            'description': 'Describe the disposals tested and confirm proceeds received and gain/loss correctly calculated.',
            'result_type': 'textarea',
        },
        {
            'id': 'depreciation_sample',
            'title': '4. Depreciation Testing — Sample Size',
            'description': 'State the number of assets tested for depreciation.',
            'result_type': 'number',
        },
        {
            'id': 'depreciation_exceptions',
            'title': '5. Depreciation Exceptions',
            'description': 'Document any differences in depreciation calculation.',
            'result_type': 'textarea',
        },
        {
            'id': 'physical_verification',
            'title': '6. Physical Verification',
            'description': 'Document the physical verification performed. Note any assets not located.',
            'result_type': 'textarea',
        },
        {
            'id': 'fa_conclusion',
            'title': 'Overall Fixed Assets Conclusion',
            'description': 'State your conclusion on fixed assets.',
            'result_type': 'select',
            'options': ['Fixed assets are fairly stated', 'Fixed assets are fairly stated with exceptions noted', 'Fixed assets are not fairly stated'],
        },
    ],

    'I': [
        {
            'id': 'supplier_statements',
            'title': '1. Supplier Statement Reconciliation',
            'description': 'Describe the supplier statements reconciled to the creditor ledger. Note any unreconciled items.',
            'result_type': 'textarea',
        },
        {
            'id': 'payables_sample',
            'title': '2. Payables Testing — Sample Size',
            'description': 'State the number of purchase invoices tested.',
            'result_type': 'number',
        },
        {
            'id': 'payables_exceptions',
            'title': '3. Payables Testing Exceptions',
            'description': 'Document any invoices that could not be agreed to supporting documents.',
            'result_type': 'textarea',
        },
        {
            'id': 'accruals_review',
            'title': '4. Accruals & Provisions Review',
            'description': 'Assess reasonableness of accruals and confirm all significant liabilities are recorded.',
            'result_type': 'textarea',
        },
        {
            'id': 'cutoff_payables',
            'title': '5. Cut-off Testing Result',
            'description': 'Describe the results of payables cut-off testing around year end.',
            'result_type': 'textarea',
        },
        {
            'id': 'payables_conclusion',
            'title': 'Overall Payables Conclusion',
            'description': 'State your conclusion on payables.',
            'result_type': 'select',
            'options': ['Payables are fairly stated', 'Payables are fairly stated with exceptions noted', 'Payables are not fairly stated'],
        },
    ],

    'Z': [
        {
            'id': 'subsequent_events',
            'title': '1. Subsequent Events',
            'description': 'Describe any significant events identified after the balance sheet date up to the date of the auditor\'s report.',
            'result_type': 'textarea',
        },
        {
            'id': 'going_concern',
            'title': '2. Going Concern Assessment',
            'description': 'Assess whether the entity can continue as a going concern for at least 12 months from the balance sheet date.',
            'result_type': 'textarea',
        },
        {
            'id': 'going_concern_conclusion',
            'title': '3. Going Concern Conclusion',
            'description': 'State your going concern conclusion.',
            'result_type': 'select',
            'options': ['Going concern basis is appropriate', 'Going concern basis is appropriate with disclosures required', 'Going concern basis is not appropriate'],
        },
        {
            'id': 'unadjusted_differences',
            'title': '4. Total Unadjusted Differences (UGX)',
            'description': 'Enter the total value of unadjusted audit differences.',
            'result_type': 'number',
        },
        {
            'id': 'material_unadjusted',
            'title': '5. Are Unadjusted Differences Material?',
            'description': 'State whether unadjusted differences are material individually or in aggregate.',
            'result_type': 'select',
            'options': ['No — below materiality threshold', 'Yes — material and require adjustment'],
        },
        {
            'id': 'completion_checklist',
            'title': '6. Completion Checklist',
            'description': 'Confirm all required audit procedures have been performed and documented.',
            'result_type': 'select',
            'options': ['All procedures complete', 'Procedures complete with outstanding items noted'],
        },
        {
            'id': 'audit_opinion',
            'title': 'Overall Audit Opinion',
            'description': 'State the overall audit opinion.',
            'result_type': 'select',
            'options': ['Unqualified — Clean opinion', 'Qualified', 'Adverse', 'Disclaimer of opinion'],
        },
    ],
}


def get_programme_for_reference(reference_code):
    if not reference_code:
        return []
    prefix = reference_code[0].upper()
    return AUDIT_PROGRAMMES.get(prefix, [])


def get_title_for_reference(reference_code):
    return REFERENCE_TITLES.get(reference_code, '')