import pandas as pd
from ctgan import CTGAN
from sklearn.preprocessing import LabelEncoder

sample_data = pd.read_excel("../resources/Sample_data.xlsx")

discrete_columns = [
    'TC_Name',
    'ITBS_Name',
    'ITBS_CID',
    'ITBS_Description',
    'ITBS_CDR',
    'ITBS_RTB_Lead','ITBS_BusinessOwner','ITBS_SystemArchitect','ITBA_Name','ITBA_Description','ITBA_CID','ITBS_RESCAT','ITBA_PO','ITBA_SA','ITBA_Status','ITBA_InstallType','ITBA_HousePosition','ITBA_SysID','ITSI_CID','ITSI_Description','ITSI_RESCAT','ITSI_CDR','ITSI_RTBLead','ITSI_OperationalStatus','ITSI_DRStatus','ITSI_InstallType','LCT_ServiceID','LCT_Name','OrgUnitName','ProductOwner','AgileLead','ServiceNowID','ProductVision','ProductRoadMap','ArchitectureVision','Primary_CTO_Architect','Service_Now','IncidentID','Incident_ShortDescription','Incident_Status','Incident_WorkNotes','Incident_AssignedTO','Incident_ReportedBy'
]

for col in discrete_columns:
    sample_data[col] = sample_data[col].astype('category')

label_encoder = LabelEncoder()
encoded_columns = {}


for col in sample_data.select_dtypes(include=['object']).columns:
    sample_data[col] = label_encoder.fit_transform(sample_data[col])
    encoded_columns[col] = label_encoder

print("Column Types After Encoding:")
print(sample_data.dtypes)

# Ensure all other string columns remain as categorical data (no numeric conversion)
# No need to apply pd.to_numeric on string columns. Only apply it to numeric columns.
numeric_columns = sample_data.select_dtypes(include=['float64', 'int64']).columns
sample_data[numeric_columns] = sample_data[numeric_columns].apply(pd.to_numeric, errors='coerce')


model = CTGAN()
model.fit(sample_data,discrete_columns)


# Generate synthetic data
try:
    num_rows = 100  # Specify the number of synthetic rows you want
    synthetic_data = model.sample(num_rows)
    print("Synthetic data generated successfully.")
    print("Synthetic Data Shape:", synthetic_data.shape)
except Exception as e:
    print("Error during data generation:", e)
    synthetic_data = None  # Set synthetic_data to None if an error occurs

#  Ensure column consistency (if needed)
if synthetic_data is not None:
    # Align columns if needed, especially after encoding
    for col, encoder in encoded_columns.items():
        # Get valid labels from the encoder
        valid_labels = encoder.classes_

        # Replace invalid labels (e.g., unseen labels) with the first valid label
        synthetic_data[col] = synthetic_data[col].apply(
            lambda x: x if x in valid_labels else valid_labels[0]  # Replace with first valid label
        )

        # Now apply the inverse transform to convert numeric labels back to strings
        try:
            synthetic_data[col] = encoder.inverse_transform(synthetic_data[col])
        except ValueError as ve:
            print(f"ValueError during inverse_transform for column {col}: {ve}")
            # Handle cases where inverse_transform fails (e.g., unseen labels)

    #  Save the synthetic data to a new Excel file
    synthetic_data.to_excel("synthetic_data.xlsx", index=False)
    print("Synthetic data saved to 'synthetic_data.xlsx'")
else:
    print("No synthetic data to save.")
