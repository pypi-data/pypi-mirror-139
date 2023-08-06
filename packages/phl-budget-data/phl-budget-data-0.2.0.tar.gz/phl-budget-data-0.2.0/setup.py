# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['phl_budget_data',
 'phl_budget_data.cli',
 'phl_budget_data.etl',
 'phl_budget_data.etl.collections',
 'phl_budget_data.etl.collections.by_sector',
 'phl_budget_data.etl.collections.monthly',
 'phl_budget_data.etl.qcmr',
 'phl_budget_data.etl.qcmr.cash',
 'phl_budget_data.etl.qcmr.obligations',
 'phl_budget_data.etl.qcmr.personal_services',
 'phl_budget_data.etl.qcmr.positions',
 'phl_budget_data.etl.spending',
 'phl_budget_data.etl.utils']

package_data = \
{'': ['*'],
 'phl_budget_data': ['data/historical/qcmr/*',
                     'data/historical/revenue/*',
                     'data/historical/spending/*']}

install_requires = \
['billy-penn>=0.1.0,<0.2.0',
 'click==8.0.1',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.20.1,<2.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'rich-click>=0.3.0,<0.4.0']

extras_require = \
{'etl': ['selenium>=3.141.0,<4.0.0',
         'pdfplumber>=0.5.25,<0.6.0',
         'webdriver-manager>=3.3.0,<4.0.0',
         'intervaltree>=3.1.0,<4.0.0',
         'python-dotenv==0.19.2',
         'boto3>=1.17.12,<2.0.0',
         'beautifulsoup4>=4.9.3,<5.0.0',
         'textual>=0.1.15,<0.2.0']}

entry_points = \
{'console_scripts': ['phl-budget-data = phl_budget_data.cli.__main__:main']}

setup_kwargs = {
    'name': 'phl-budget-data',
    'version': '0.2.0',
    'description': 'PHL Budget Data',
    'long_description': '\n<p align="center">\n<img src="static/PHL%20Budget%20Data%20Logo.png"/>\n</p>\n\n\n## Installation\n\nTo get the latest version of the code, clone the repository, and use `poetry install` to install the dependencies.\n\nYou can also install the package into\na conda environment using the following command\n\n```bash\nconda activate py38\npip install .\n```\n\nThis will install the package into the `py38` environment.\n\n## Examples\n\nThe subsections below list examples for loading various kinds of budget-related data sets for the City of Philadelphia.\n\n### Revenue Reports\n\nData is available from the City of Philadelphia\'s Revenue reports, as published to the [City\'s website](https://www.phila.gov/departments/department-of-revenue/reports/).\n\n#### City Collections\n\nMonthly PDF reports are available on the City of Philadelphia\'s website according to fiscal year (example: [FY 2021](https://www.phila.gov/documents/fy-2021-city-monthly-revenue-collections/)).\n\n**Note:** Cleaned CSV files are available in the following folder: [src/phl_budget_data/data/processed/collections/monthly/city/](src/phl_budget_data/data/processed/collections/monthly/city/)\n\nLoad the data using Python:\n\n```python\nfrom phl_budget_data.clean import load_city_collections\n\ndata = load_city_collections()\ndata.head()\n```\n\nOutput:\n\n```python\n                        name  fiscal_year        total month_name  month  fiscal_month  year       date kind\n0                      sales         2021   14228731.0        jan      1             7  2021 2021-01-01  Tax\n1  wage_earnings_net_profits         2021  182689530.0        jan      1             7  2021 2021-01-01  Tax\n2                       soda         2021    5149478.0        jan      1             7  2021 2021-01-01  Tax\n3                outdoor_ads         2021     179166.0        jan      1             7  2021 2021-01-01  Tax\n4       real_estate_transfer         2021   27222198.0        jan      1             7  2021 2021-01-01  Tax\n```\n\n#### School District Collections\n\nMonthly PDF reports are available on the City of Philadelphia\'s website according to fiscal year (example: [FY 2021](https://www.phila.gov/documents/fy-2021-school-district-monthly-revenue-collections/)).\n\n**Note:** Cleaned CSV files are available in the following folder: [src/phl_budget_data/data/processed/collections/monthly/school/](src/phl_budget_data/data/processed/collections/monthly/school/)\n\nLoad the data using Python:\n\n```python\nfrom phl_budget_data.clean import load_school_collections\n\ndata = load_school_collections()\ndata.head()\n```\n\nOutput:\n\n```python\n                name  fiscal_year     total month_name  month  fiscal_month  year       date\n0        real_estate         2021  50817991        jan      1             7  2021 2021-01-01\n1      school_income         2021    436599        jan      1             7  2021 2021-01-01\n2  use_and_occupancy         2021  19395530        jan      1             7  2021 2021-01-01\n3             liquor         2021   1874302        jan      1             7  2021 2021-01-01\n4       other_nontax         2021      2000        jan      1             7  2021 2021-01-01\n```\n\n#### Monthly Wage Tax Collections by Industry\n\nMonthly PDF reports are available on the City of Philadelphia\'s website according to calendar year (example: [2020](https://www.phila.gov/documents/2020-wage-tax-by-industry/)).\n\n**Note:** Cleaned CSV files are available in the following folder: [src/phl_budget_data/data/processed/collections/by-sector/wage/](src/phl_budget_data/data/processed/collections/by-sector/wage/)\n\nLoad the data using Python:\n\n```python\nfrom phl_budget_data.clean import load_wage_collections_by_sector\n\ndata = load_wage_collections_by_sector()\ndata.head()\n```\n\nOutput:\n\n```python\n                                              sector               parent_sector      total month_name  month  fiscal_month  year  fiscal_year       date\n0                              Unclassified Accounts                         NaN   494978.0        jan      1             7  2021         2021 2021-01-01\n1                                    Wholesale Trade                         NaN  4497890.0        jan      1             7  2021         2021 2021-01-01\n2                 Nursing & Personal Care Facilities  Health and Social Services  3634459.0        jan      1             7  2021         2021 2021-01-01\n3  Outpatient Care Centers and Other Health Services  Health and Social Services  6267932.0        jan      1             7  2021         2021 2021-01-01\n4  Doctors, Dentists, and Other Health Practitioners  Health and Social Services  5392573.0        jan      1             7  2021         2021 2021-01-01\n```\n\n\n### Quarterly City Manager\'s Report\n\nPDF reports are available on the City of Philadelphia\'s website [here](https://www.phila.gov/finance/reports-Quarterly.html).\n\n### Cash Report\n\nLoad the data using Python:\n\n```python\nfrom phl_budget_data.clean import load_qcmr_cash_reports\n\nrevenue = load_qcmr_cash_reports(kind="revenue")\nrevenue.head()\n```\n\nOutput:\n\n```python\n                      category  fiscal_month  amount  fiscal_year  quarter  month\n0              Real Estate Tax             1     9.1         2021        4      7\n1  Wage, Earnings, Net Profits             1   134.1         2021        4      7\n2          Realty Transfer Tax             1    36.4         2021        4      7\n3                    Sales Tax             1    24.4         2021        4      7\n4                         BIRT             1   266.4         2021        4      7\n```\n\nData can be load by specifying `kind` as "revenue", "spending", "fund-balances", or "net-cash-flow".\n\n## Adding the Latest Data\n\nThis section describes how to add the latest processed data files to the repository.\n### QCMR Cash Reports\n\n1. Add the two-page PDF for the cash report to the `src/phl_budget_data/data/raw/qcmr/cash` folder\n2. Run the following command to convert the PDF to a processed CSV:\n\nFor example, for FY21 Q4:\n\n```python\npoetry shell\nphl-budget-etl qcmr cash --fiscal-year 2021 --quarter 4\n```\n\n3. Now, add the new CSV files to git, and push the changes to GitHub:\n\nFrom the root folder:\n\n```python\ngit add .\ngit commit -m "Add new QCMR cash report"\ngit push origin main\n```\n\n',
    'author': 'Nick Hand',
    'author_email': 'nick.hand@phila.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
