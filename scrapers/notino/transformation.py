import pandas as pd
from datetime import datetime

class NotinoTransformation:
    def __init__(self, country: str, retailer: str):
        self.country = country
        self.retailer = retailer

    def transform_data(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        transformed_df = raw_df.copy()
        transformed_df['country'] = self.country
        transformed_df['currency'] = 'CZK'  # Adjust based on actual country/currency
        transformed_df['scraped_at'] = datetime.now().isoformat()

        transformed_df['price'] = transformed_df['price'].str.replace(' Kč', '').str.replace(',', '.').astype(float)
        if 'price_after_sale' in transformed_df.columns:
            transformed_df['price_after_sale'] = transformed_df['price_after_sale'].str.replace(' Kč', '').str.replace(',', '.').astype(float)
        else:
            transformed_df['price_after_sale'] = transformed_df['price']
        
        transformed_df['discount_amount'] = transformed_df.apply(
            lambda row: row['price'] - row['price_after_sale'] if row['price_after_sale'] else 0, axis=1
        )

        return transformed_df

def main(raw_df: pd.DataFrame, country: str, retailer: str):
    transformation = NotinoTransformation(country=country, retailer=retailer)
    transformed_df = transformation.transform_data(raw_df)
    return transformed_df

if __name__ == "__main__":
    raw_df = pd.read_csv("notino_raw.csv")
    transformed_df = main(raw_df, country="cz", retailer="notino")
    transformed_df.to_csv("notino_transformed.csv", index=False)
