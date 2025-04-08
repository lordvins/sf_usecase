from snowflake.snowpark import Session
from google.cloud import secretmanager
from google.cloud import storage
import os
from flask import Flask, request, jsonify
import google.auth
import requests
import json
import pandas as pd

# Print Pandas version for debugging
print(pd.__version__)

# Set the path to the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/service-account-key.json"

def get_secret(secret_id, project_id):
    """Fetches a secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    secret = response.payload.data.decode("UTF-8")
    return json.loads(secret)  # Parse the JSON string into a Python dictionary

# Example usage: Fetch Snowflake connection parameters from Secret Manager
project_id = "total-reef-436711-p3"
secret_id = "snowflake_credentials"
connection_parameters = get_secret(secret_id, project_id)

# Step 2: Establish a Snowpark session
session = Session.builder.configs(connection_parameters).create()

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def handle_request():
    # Handle GET requests
    if request.method == "GET":
        print("Received GET request.")
        return jsonify({"message": "Service is running."}), 200

    # Handle POST requests
    elif request.method == "POST":
        # Log the incoming request
        print("Received POST request:", request.json)

        # Get the JSON payload
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        # Extract required data from the payload
        file_name = data.get("name")
        bucket_name = data.get("bucket")
        if not file_name or not bucket_name:
            return jsonify({"error": "Missing file_name or bucket_name"}), 400

        # Step 3: Load and process the JSON file
        try:
            # Define paths
            destination_file_name = "/app/ElectricVehiclePopulationData.json"

            # Download the blob
            download_blob(bucket_name, file_name, destination_file_name)

            # Load the JSON file as usual
            json_file_path = destination_file_name
            with open(json_file_path, "r") as file:
                json_data = json.load(file)

            # Extract headers from the 'meta' section
            columns = [col["fieldName"] for col in json_data["meta"]["view"]["columns"]]

            # Extract actual data from the 'data' section
            data = json_data["data"]

            # Create a DataFrame using the extracted data and columns
            df = pd.DataFrame(data, columns=columns)

            # Step 4: Filter the necessary columns
            columns_to_keep = [
                "vin_1_10", "county", "city", "state", "zip_code", "model_year", "make", "model",
                "ev_type", "cafv_type", "electric_range", "base_msrp", "legislative_district",
                "dol_vehicle_id", "electric_utility", "_2020_census_tract"
            ]
            df_to_insert = df[columns_to_keep]

            # Step 5: Create the Snowflake table schema
            table_name = "VV_SF_ELECTRIC_VEHICLE_DATA"
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                vin STRING,
                county STRING,
                city STRING,
                state STRING,
                zip_code STRING,
                model_year STRING,
                make STRING,
                model STRING,
                ev_type STRING,
                cafv_type STRING,
                electric_range NUMBER,
                base_msrp NUMBER,
                legislative_district NUMBER,
                dol_vehicle_id STRING,
                electric_utility STRING,
                _2020_census_tract STRING
            );
            """
            session.sql(create_table_query).collect()

            # Step 6: Insert data into Snowflake
            session.write_pandas(df_to_insert, table_name, auto_create_table=True)

            print("JSON data successfully uploaded to Snowflake!")
            return jsonify({"message": f"File '{file_name}' processed successfully"}), 200

        except Exception as e:
            print(f"Failed to process file: {e}")
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Flask will listen on the port provided by Cloud Run
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

