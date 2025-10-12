/**
 * Ontario Will and POA Precedents
 * Common responses and options based on Ontario legal best practices
 * Sourced from Ontario Succession Law Reform Act and common legal precedents
 */

export const executorOptions = [
  { value: 'spouse', label: 'My spouse/partner', description: 'Most common choice for married individuals' },
  { value: 'adult_child', label: 'My adult child', description: 'Responsible adult children' },
  { value: 'sibling', label: 'My brother or sister', description: 'Trusted family member' },
  { value: 'parent', label: 'My parent', description: 'For younger individuals' },
  { value: 'friend', label: 'A trusted friend', description: 'Close friend with good judgment' },
  { value: 'professional', label: 'A professional executor (lawyer, accountant)', description: 'For complex estates' },
  { value: 'trust_company', label: 'A trust company', description: 'For large or complex estates' },
  { value: 'other', label: 'Other', description: 'Specify a different relationship' }
];

export const beneficiaryRelationships = [
  { value: 'spouse', label: 'Spouse/Partner' },
  { value: 'child', label: 'Child' },
  { value: 'grandchild', label: 'Grandchild' },
  { value: 'sibling', label: 'Brother/Sister' },
  { value: 'parent', label: 'Parent' },
  { value: 'niece_nephew', label: 'Niece/Nephew' },
  { value: 'friend', label: 'Friend' },
  { value: 'charity', label: 'Charitable Organization' },
  { value: 'other', label: 'Other' }
];

export const distributionOptions = [
  { 
    value: 'equal_split', 
    label: 'Divide equally among all beneficiaries',
    description: 'Each beneficiary receives an equal share',
    example: 'If 3 beneficiaries, each receives 33.33%'
  },
  { 
    value: 'spouse_all', 
    label: 'Everything to my spouse, then to children',
    description: 'Common for married couples with children',
    example: 'Spouse inherits everything; if spouse predeceases, goes to children'
  },
  { 
    value: 'specific_percentages', 
    label: 'Specify percentage for each beneficiary',
    description: 'Customize the distribution percentages',
    example: '50% to spouse, 25% to each child'
  },
  { 
    value: 'per_stirpes', 
    label: 'Per stirpes (by family branch)',
    description: 'If a child predeceases, their share goes to their children',
    example: 'Common for multi-generational distribution'
  },
  { 
    value: 'specific_items', 
    label: 'Specific items to specific people',
    description: 'Allocate particular items to particular beneficiaries',
    example: 'House to child A, investments to child B'
  },
  { 
    value: 'other', 
    label: 'Other arrangement',
    description: 'Custom distribution plan'
  }
];

export const guardianshipOptions = [
  { value: 'yes', label: 'Yes, I have minor children and need to appoint guardians' },
  { value: 'no', label: 'No, I do not have minor children' },
  { value: 'adult', label: 'My children are all adults (18+)' }
];

export const assetCategories = [
  { 
    value: 'real_estate', 
    label: 'Real Estate',
    description: 'Primary residence, vacation properties, rental properties',
    examples: ['Primary home', 'Cottage', 'Rental property', 'Commercial property']
  },
  { 
    value: 'bank_accounts', 
    label: 'Bank Accounts & Cash',
    description: 'Savings, chequing, GICs, term deposits',
    examples: ['Savings account', 'Chequing account', 'GICs', 'Cash holdings']
  },
  { 
    value: 'investments', 
    label: 'Investments',
    description: 'RRSPs, TFSAs, stocks, bonds, mutual funds',
    examples: ['RRSP', 'TFSA', 'Stock portfolio', 'Mutual funds', 'Bonds']
  },
  { 
    value: 'business', 
    label: 'Business Interests',
    description: 'Ownership in companies, partnerships',
    examples: ['Company shares', 'Partnership interest', 'Sole proprietorship']
  },
  { 
    value: 'personal_property', 
    label: 'Personal Property',
    description: 'Vehicles, jewelry, art, collectibles',
    examples: ['Vehicle', 'Jewelry', 'Art collection', 'Antiques', 'Furniture']
  },
  { 
    value: 'digital_assets', 
    label: 'Digital Assets',
    description: 'Online accounts, cryptocurrencies, digital files',
    examples: ['Cryptocurrency', 'Domain names', 'Social media accounts', 'Digital photos']
  },
  { 
    value: 'insurance', 
    label: 'Life Insurance',
    description: 'Life insurance policies and benefits',
    examples: ['Term life insurance', 'Whole life policy', 'Group insurance']
  },
  { 
    value: 'other', 
    label: 'Other Assets',
    description: 'Any other property or assets'
  }
];

export const specificBequestTemplates = [
  {
    value: 'jewelry',
    label: 'Jewelry to family member',
    template: 'I give my [describe jewelry] to [beneficiary name]',
    example: 'I give my diamond engagement ring to my daughter, Sarah Smith'
  },
  {
    value: 'vehicle',
    label: 'Vehicle to beneficiary',
    template: 'I give my [year, make, model] vehicle to [beneficiary name]',
    example: 'I give my 2020 Honda Accord to my son, John Smith'
  },
  {
    value: 'property_specific',
    label: 'Specific real property',
    template: 'I give my property located at [address] to [beneficiary name]',
    example: 'I give my property located at 123 Main St, Toronto to my daughter, Jane Doe'
  },
  {
    value: 'monetary',
    label: 'Specific dollar amount',
    template: 'I give $[amount] to [beneficiary name]',
    example: 'I give $10,000 to my nephew, Michael Johnson'
  },
  {
    value: 'charitable',
    label: 'Charitable donation',
    template: 'I give [amount or percentage] to [charity name]',
    example: 'I give $5,000 to the Canadian Cancer Society'
  },
  {
    value: 'collection',
    label: 'Collection or hobby items',
    template: 'I give my [describe collection] to [beneficiary name]',
    example: 'I give my stamp collection to my brother, Robert Brown'
  },
  {
    value: 'other',
    label: 'Other specific bequest',
    template: 'I give [describe item] to [beneficiary name]'
  }
];

export const poaPropertyPowers = [
  {
    value: 'banking',
    label: 'Banking and Financial Transactions',
    description: 'Managing bank accounts, paying bills, making deposits/withdrawals',
    isDefault: true
  },
  {
    value: 'real_estate',
    label: 'Real Estate Transactions',
    description: 'Buying, selling, leasing, or managing real property',
    isDefault: true
  },
  {
    value: 'investments',
    label: 'Investment Management',
    description: 'Managing investments, stocks, bonds, RRSPs, TFSAs',
    isDefault: true
  },
  {
    value: 'business',
    label: 'Business Operations',
    description: 'Operating or managing business interests',
    isDefault: false
  },
  {
    value: 'legal',
    label: 'Legal Proceedings',
    description: 'Initiating or defending legal actions on your behalf',
    isDefault: false
  },
  {
    value: 'government_benefits',
    label: 'Government Benefits',
    description: 'Applying for and managing government benefits and pensions',
    isDefault: true
  },
  {
    value: 'taxes',
    label: 'Tax Matters',
    description: 'Filing tax returns and dealing with tax authorities',
    isDefault: true
  },
  {
    value: 'insurance',
    label: 'Insurance',
    description: 'Managing insurance policies and claims',
    isDefault: true
  }
];

export const poaCarePowers = [
  {
    value: 'medical_treatment',
    label: 'Medical Treatment Decisions',
    description: 'Consenting to or refusing medical treatment',
    isDefault: true
  },
  {
    value: 'healthcare_providers',
    label: 'Healthcare Provider Selection',
    description: 'Choosing doctors, specialists, and healthcare facilities',
    isDefault: true
  },
  {
    value: 'living_arrangements',
    label: 'Living Arrangements',
    description: 'Decisions about where you live and type of accommodation',
    isDefault: true
  },
  {
    value: 'nutrition',
    label: 'Nutrition and Hydration',
    description: 'Decisions about diet and nutritional support',
    isDefault: true
  },
  {
    value: 'clothing',
    label: 'Clothing and Personal Care',
    description: 'Decisions about clothing and personal hygiene',
    isDefault: true
  },
  {
    value: 'safety',
    label: 'Safety and Security',
    description: 'Decisions to keep you safe and secure',
    isDefault: true
  },
  {
    value: 'social',
    label: 'Social Activities',
    description: 'Participation in social and recreational activities',
    isDefault: true
  }
];

export const poaTypeOptions = [
  {
    value: 'continuing',
    label: 'Continuing Power of Attorney',
    description: 'Remains in effect if you become mentally incapable',
    recommended: true
  },
  {
    value: 'non_continuing',
    label: 'Non-Continuing Power of Attorney',
    description: 'Becomes invalid if you become mentally incapable',
    recommended: false
  }
];

export const poaEffectiveDate = [
  {
    value: 'immediate',
    label: 'Effective immediately upon signing',
    description: 'Attorney can act as soon as the document is signed'
  },
  {
    value: 'incapacity',
    label: 'Effective upon my mental incapacity',
    description: 'Attorney can only act after you are declared mentally incapable'
  },
  {
    value: 'specific_date',
    label: 'Effective on a specific date',
    description: 'Specify a future date when powers become effective'
  }
];

export const helpTexts = {
  executor: {
    title: 'Understanding Executors',
    content: 'An executor (or estate trustee) is responsible for managing your estate after you pass away. They will gather your assets, pay debts and taxes, and distribute your estate according to your will. Choose someone who is trustworthy, organized, and willing to serve.',
    tips: [
      'Choose someone who lives in Ontario if possible to simplify the process',
      'Consider naming an alternate executor in case your first choice cannot serve',
      'The executor can be a beneficiary',
      'You should discuss this role with the person before naming them'
    ]
  },
  beneficiary: {
    title: 'Choosing Beneficiaries',
    content: 'Beneficiaries are the people or organizations who will receive your assets. You can name multiple beneficiaries and specify what each should receive.',
    tips: [
      'Be specific about who you mean (use full legal names)',
      'Consider what happens if a beneficiary predeceases you',
      'You can include charitable organizations as beneficiaries',
      'Minor children can be beneficiaries, but consider setting up a trust'
    ]
  },
  guardian: {
    title: 'Appointing Guardians',
    content: 'A guardian is someone who will take care of your minor children (under 18) if both parents pass away. This is one of the most important decisions in your will.',
    tips: [
      'Choose someone who shares your values and parenting style',
      'Consider the guardian\'s age, health, and financial situation',
      'Name an alternate guardian in case your first choice cannot serve',
      'Discuss this responsibility with the person before naming them',
      'The court will consider your wishes but has final authority'
    ]
  },
  distribution: {
    title: 'Distributing Your Estate',
    content: 'You can distribute your estate in many ways. The most common is to divide everything equally among your beneficiaries, but you can also give specific items to specific people or use percentages.',
    tips: [
      'Consider tax implications of different distribution methods',
      'Think about what\'s fair vs. what\'s equal',
      '"Per stirpes" distribution ensures each family branch receives an equal share',
      'You can make specific bequests and then divide the remainder (residue)'
    ]
  },
  attorney_property: {
    title: 'Power of Attorney for Property',
    content: 'This legal document allows someone you trust to manage your financial affairs and property if you become unable to do so. In Ontario, this is governed by the Substitute Decisions Act.',
    tips: [
      'Choose someone who is financially responsible and trustworthy',
      'A "continuing" POA remains valid if you become mentally incapable',
      'You can specify what powers the attorney has and any limitations',
      'You must be mentally capable when you create this document',
      'This document becomes invalid when you pass away'
    ]
  },
  attorney_care: {
    title: 'Power of Attorney for Personal Care',
    content: 'This allows someone to make personal care and healthcare decisions for you if you become unable to make them yourself. This includes medical treatment, living arrangements, and personal care.',
    tips: [
      'Choose someone who understands your values and wishes',
      'You must be at least 16 years old to create this document',
      'You can include specific instructions about your care preferences',
      'This is different from a living will or advance directive',
      'The attorney must follow your known wishes and act in your best interests'
    ]
  },
  witnesses: {
    title: 'Witness Requirements',
    content: 'Ontario law requires TWO witnesses for wills and powers of attorney. Witnesses must be present when you sign and must also sign in your presence.',
    tips: [
      'Witnesses must be 18 years or older',
      'Witnesses cannot be beneficiaries in a will',
      'Witnesses cannot be the attorney in a POA or their spouse',
      'Witnesses should be mentally capable',
      'All parties should be present at the same time during signing',
      'NO notarization is required in Ontario'
    ]
  }
};

export const aiPromptTemplates = {
  executor_suggestion: 'Based on Ontario legal best practices, consider the following when choosing an executor...',
  beneficiary_distribution: 'Here are common distribution strategies used in Ontario wills...',
  asset_identification: 'Common assets to include in your Ontario will include...',
  guardian_considerations: 'When appointing guardians in Ontario, important factors to consider...',
  poa_limitations: 'You may want to consider these limitations or conditions for your power of attorney...'
};
