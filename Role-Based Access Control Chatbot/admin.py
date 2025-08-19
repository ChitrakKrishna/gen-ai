import pandas as pd

# Load the CSV file
df = pd.read_csv(r'DS-RPC-01/data/hr/hr_data.csv')

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

department = None  # Declare globally


def get_department(input_email, input_id):
    # Load the CSV file
    df = pd.read_csv(r'DS-RPC-01/data/hr/hr_data.csv')

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    department = None  # Declare globally

    user = df[
            (df['email'] == input_email) &
            (df['employee_id'] == input_id)
        ]

    if not user.empty:
        # Extract user row and department
        user_row = user.iloc[0]
        department = user_row['department']

    return department




if __name__ == '__main__':
    while True:
        # Take user input
        input_email = input("Enter your email: ").strip().lower()
        input_id = input("Enter your employee ID: ").strip()

        # Filter the user
        user = df[
            (df['email'] == input_email) &
            (df['employee_id'] == input_id)
        ]

        if not user.empty:
            # Extract user row and department
            user_row = user.iloc[0]
            department = user_row['department']

            print("\n" + "="*50)
            print(f"Welcome aboard, {user_row['full_name']}!")
            print(f"Role       : {user_row['role']}")
            print(f"Department : {department}")
            print("You have successfully logged in.")
            print("="*50)

            # You can now use the department variable elsewhere
            break
        else:
            print("\n❌ Invalid email or employee ID. Please try again.\n")
            