import pandas as pd
import numpy as np

def generate_excel_files_with_mapping():
    """
    Generates SRC.xlsx and TGT.xlsx with a specific column mapping and data differences.
    
    The files are created with the following schema:
    - SRC.xlsx: ID, NAME, AGE, COUNTRY, JOIN_DATE, SRC_SALARY
    - TGT.xlsx: TGT_ID, TGT_FULL_NAME, TGT_AGE, TGT_COUNTRY, TGT_START_DATE, TGT_EXTRA_COL
    """

    # --- Configuration ---
    num_rows = 1000000  # Number of rows for the generated files
    
    # --- Generate common data (matching rows) ---
    np.random.seed(42)
    ids = np.arange(1, num_rows + 1)
    names = np.random.choice([
        'Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Shan', 'Konduru',
        'Bhushan', 'Ravi', 'Pavan', 'Kumar', 'Sarma', 'Krishna', 'Sailaja',
        'Sri', 'Kirani', 'Rashmika', 'Anushka', 'Nani', 'Vijay', 'Ajith',
        'Thalapathy', 'Suriya', 'Ram Charan', 'Allu Arjun', 'Mahesh Babu',
        'Prabhas', 'Jr NTR', 'Yash', 'Darshan', 'Upendra', 'Kiccha Sudeep',
        'Puneeth Rajkumar', 'Radhika Pandit', 'Shraddha Srinath', 'Rashmika Mandanna',
        'Anushka Shetty', 'Tamannaah Bhatia', 'Kajal Aggarwal', 'Samantha Akkineni',
        'Nayanthara', 'Trisha Krishnan', 'Keerthy Suresh', 'Aishwarya Rai',
        'Deepika Padukone', 'Alia Bhatt', 'Katrina Kaif', 'Priyanka Chopra',
        'Ananya Panday', 'Sara Ali Khan', 'Janhvi Kapoor', 'Disha Patani',
        'Sachin Tendulkar', 'Virat Kohli', 'Rohit Sharma', 'MS Dhoni',
        'Jasprit Bumrah', 'Hardik Pandya', 'KL Rahul', 'Shikhar Dhawan',
        'Rishabh Pant', 'Yuzvendra Chahal', 'Bhuvneshwar Kumar', 'Ravindra Jadeja',
        'Ben Stokes', 'Joe Root', 'Jofra Archer', 'Jos Buttler', 'Eoin Morgan',
        'Kane Williamson', 'Ross Taylor', 'Trent Boult', 'Tim Southee',
        'Mitchell Starc', 'Pat Cummins', 'Steve Smith', 'David Warner',
        'Bill Gates', 'Elon Musk', 'Jeff Bezos', 'Warren Buffett',
        'Mark Zuckerberg', 'Larry Page', 'Sergey Brin', 'Tim Cook',
        'Sundar Pichai', 'Satya Nadella', 'Sheryl Sandberg', 'Susan Wojcicki'
        ], size=num_rows)
    ages = np.random.randint(20, 60, size=num_rows)
    countries = np.random.choice([
        'USA', 'Canada', 'UK', 'India', 'Germany', 'France', 'Russia', 'Italy',
        'Spain', 'Australia', 'Brazil', 'China', 'Japan', 'South Korea', 'Mexico',
        'Netherlands', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Poland', 'Turkey',
        'Saudi Arabia', 'UAE', 'South Africa', 'Egypt', 'Nigeria', 'Argentina',
        'Chile', 'Colombia', 'Peru', 'Venezuela', 'Thailand', 'Vietnam', 'Indonesia',
        'Philippines', 'Malaysia', 'Singapore', 'New Zealand', 'Ireland', 'Belgium',
        'Switzerland', 'Austria', 'Portugal', 'Greece', 'Czech Republic', 'Hungary',
        'Romania', 'Bulgaria', 'Croatia', 'Slovakia', 'Slovenia', 'Ukraine'
                                  ], size=num_rows)
    join_dates = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.arange(num_rows), unit='s')
    
    # --- Create Source DataFrame (SRC.xlsx) ---
    source_df = pd.DataFrame({
        'ID': ids,
        'NAME': names,
        'AGE': ages,
        'COUNTRY': countries,
        'JOIN_DATE': join_dates,
        'SRC_SALARY': np.random.randint(50000, 100000, size=num_rows) # Exists only in source
    })
    
    # --- Create Target DataFrame (TGT.xlsx) ---
    target_df = pd.DataFrame({
        'TGT_ID': ids,
        'TGT_FULL_NAME': names,
        'TGT_AGE': ages,
        'TGT_COUNTRY': countries,
        'TGT_START_DATE': join_dates,
        'TGT_EXTRA_COL': np.random.choice(['A', 'B', 'C'], size=num_rows) # Exists only in target
    })

    # --- Introduce Differences for Testing ---
    
    # 1. Row-wise data differences (mismatched AGE for ID 10 and 20)
    source_df.loc[9, 'AGE'] = 99  # ID=10 (index 9)
    target_df.loc[19, 'TGT_AGE'] = 111 # ID=20 (index 19)
    
    # 2. Rows in source only (delete a few from the target)
    target_df.drop(index=[100, 101, 102], inplace=True)
    
    # 3. Rows in target only (delete a few from the source)
    source_df.drop(index=[200, 201, 202], inplace=True)
    
    # 4. Column data type/format differences (join dates)
    # Convert a few dates in target to a different string format
    target_df['TGT_START_DATE'] = target_df['TGT_START_DATE'].dt.strftime('%m/%d/%Y')
    
    # --- Save to Excel files ---
    output_dir = 'DATA/EXEL_TO_EXCEL'
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    source_path = os.path.join(output_dir, 'src_mapping.xlsx')
    target_path = os.path.join(output_dir, 'tgt_mapping.xlsx')
    
    source_df.to_excel(source_path, index=False)
    target_df.to_excel(target_path, index=False)
    
    print(f"Generated {source_path} and {target_path} successfully.")

if __name__ == '__main__':
    generate_excel_files_with_mapping()