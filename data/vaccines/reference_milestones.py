"""
Factory tables for loading database with ground truth or set categorical data.
"""

# Milestone Information
#   milestone_id => category_num+milestone_in_category_num
milestones = (
    {
        'milestone_id': 11,
        'name': 'discovery',
        'category': 'pre-clinical',
    },
    {
        'milestone_id': 12,
        'name': 'pre_clinical_studies',
        'category': 'pre-clinical',
    },
    {
        'milestone_id': 13,
        'name': 'lead_selection',
        'category': 'pre-clinical'
    },
    {
        'milestone_id': 21,
        'name': 'clinical_batch',
        'category': 'manufacturing',
    },
    {
        'milestone_id': 31,
        'name': 'ind',
        'category': 'regulatory',
    },
    {
        'milestone_id': 41,
        'name': 'phase_1',
        'category': 'clinical_development',
    },
    {
        'milestone_id': 42,
        'name': 'phase_2',
        'category': 'clinical_development',
    },
    {
        'milestone_id': 43,
        'name': 'phase_3',
        'category': 'clinical_development',
    },
    {
        'milestone_id': 44,
        'name': 'phase_4',
        'category': 'clinical_development',
    },
    {
        'milestone_id': 51,
        'name': 'nda',
        'category': 'regulatory',
    },
    {
        'milestone_id': 61,
        'name': 'complete',
        'category': 'completion',
    },
    {
        'milestone_id': 62,
        'name': 'approved',
        'category': 'completion',
    },
)

# Rename to milestone names from helpwithcovid
def get_milestone_renaming_schema(columns=None):
    if columns is None:
        milestone_col_name_schema = {
            'ID': 'product_id',
            'Source?': 'source',
            'Pre-Clinical Studies Started': 'pre_clinical_studies',
            'Lead Selection Finalized': 'lead_selection',
            'Clinical Batch Finalized': 'clinical_batch',
            'IND or Equivalent Approval Finalized': 'ind',
            'Phase 1 Started': 'phase_1',
            'Phase 2 Started': 'phase_2',
            'Phase 3 Started': 'phase_3',
            'NDA or equivalent Approval Finalized': 'nda',
            'Discovery Started': 'discovery',
        }
    return milestone_col_name_schema
