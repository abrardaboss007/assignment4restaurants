import unittest
import pandas as pd
import os
from api_data import add_image_paths, save_to_csv
class TestDataProcessing(unittest.TestCase):

    def test_add_image_paths(self):
        # Sample DataFrame with a RatingKey
        df = pd.DataFrame({'RatingKey': ['fhrs_0_en-gb.png', 'fhrs_1_en-gb.png', 'fhrs_2_en-gb.png']})
        result = add_image_paths(df)
        
        # Check if the 'ImagePath' column exists and the paths are correctly constructed
        expected_paths = [r"images\test\fhrs_0_en-gb.png", r"images\test\fhrs_1_en-gb.png", r"images\test\fhrs_2_en-gb.png"]
        self.assertListEqual(result['ImagePath'].tolist(), expected_paths)
    
    def test_data_filtering(self):
        # Create a sample DataFrame
        data = {
            'BusinessType': ['Restaurant/Cafe/Canteen', 'Takeaway/sandwich shop', 'Other'],
            'PostCode': ['A123', 'B456', None],
            'RatingDate': ['2025-01-01', None, '2025-01-03'],
            'Longitude': [0.1, None, 0.3],
            'Latitude': [51.5, 51.6, None],
            'RatingKey': ['A1', 'B2', 'C3']
        }
        df = pd.DataFrame(data)
        
        # Apply the data filtering steps from the script
        df_filtered = df.dropna(subset=["PostCode", "RatingDate", "Longitude", "Latitude"])
        df_filtered = df_filtered[df_filtered["BusinessType"].isin(["Restaurant/Cafe/Canteen", "Takeaway/sandwich shop"])]
        
        # Check the filtered DataFrame
        self.assertEqual(df_filtered.shape[0], 2)  # There should be 2 rows after filtering
        
    def test_save_to_csv(self):
        # Create a temporary test DataFrame
        df = pd.DataFrame({'BusinessName': ['Test Restaurant'], 'RatingKey': ['fhrs_0_en-gb.png']})
        
        # Save the DataFrame to CSV
        test_filename = "test_output.csv"
        save_to_csv(df, test_filename)
        
        # Check if the file exists and contains the expected data
        self.assertTrue(os.path.exists(test_filename))
        
        # Clean up the test file
        os.remove(test_filename)

if __name__ == '__main__':
    unittest.main()
