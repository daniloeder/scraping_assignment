import pandas as pd

class NotinoTransformation:
    def __init__(self, country: str, retailer: str):
        self.country = country
        self.retailer = retailer


    # implement any methods you need to transform the scraped data

    # add to the scraped data at least these columns:
    # - country
    # - currency
    # - scraped_at (date and time when the data was scraped)

    # ensure that price and price_after_sale columns are in float format
    # add discount amount column with the discount (float)


    def transform_data(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        transformed_df = raw_df.copy()

        return transformed_df

def main(raw_df: pd.DataFrame, country: str, retailer: str):
    transformation = NotinoTransformation(country=country, retailer=retailer)

    transformed_df = transformation.transform_data(raw_df)

    return transformed_df

if __name__ == "__main__":
    raw_df = pd.read_csv("notino_raw.csv")
    transformed_df = main(raw_df, country="cz", retailer="notino")
    transformed_df.to_csv("notino_transformed.csv", index=False)