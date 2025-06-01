from fastapi import UploadFile, HTTPException
import pandas as pd
import json
from io import StringIO
import pyarrow.parquet as pq
import io
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    async def process_file(self, file: UploadFile) -> pd.DataFrame:
        """Process uploaded file and return a pandas DataFrame."""
        try:
            logger.info(f"Processing file: {file.filename}")
            # Validate file size first
            self.validate_file_size(file)
            
            content = await file.read()
            
            if file.filename.endswith('.csv'):
                return self._process_csv(content)
            elif file.filename.endswith(('.xls', '.xlsx')):
                return self._process_excel(content)
            elif file.filename.endswith('.parquet'):
                return self._process_parquet(content)
            elif file.filename.endswith('.json'):
                return self._process_json(content)
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file format. Please upload CSV, Excel, Parquet, or JSON files."
                )
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

    def _process_csv(self, content: bytes) -> pd.DataFrame:
        """Process CSV file content."""
        try:
            text = content.decode('utf-8')
            logger.info("Attempting to read CSV data")
            df = pd.read_csv(StringIO(text))
            logger.info(f"Successfully read CSV with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error processing CSV file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error processing CSV file: {str(e)}")

    def _process_excel(self, content: bytes) -> pd.DataFrame:
        """Process Excel file content."""
        try:
            logger.info("Attempting to read Excel data")
            df = pd.read_excel(io.BytesIO(content))
            logger.info(f"Successfully read Excel with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error processing Excel file: {str(e)}")

    def _process_parquet(self, content: bytes) -> pd.DataFrame:
        """Process Parquet file content."""
        try:
            logger.info("Attempting to read Parquet data")
            table = pq.read_table(io.BytesIO(content))
            df = table.to_pandas()
            logger.info(f"Successfully read Parquet with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error processing Parquet file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error processing Parquet file: {str(e)}")

    def _process_json(self, content: bytes) -> pd.DataFrame:
        """Process JSON file content."""
        try:
            logger.info("Attempting to read JSON data")
            text = content.decode('utf-8')
            data = json.loads(text)
            df = pd.json_normalize(data)
            logger.info(f"Successfully read JSON with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error processing JSON file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error processing JSON file: {str(e)}")

    def validate_file_size(self, file: UploadFile, max_size_mb: int = 100) -> bool:
        """Validate file size against maximum allowed size."""
        try:
            max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
            file_size = len(file.file.read())
            file.file.seek(0)  # Reset file pointer
            
            if file_size > max_size_bytes:
                raise HTTPException(
                    status_code=400,
                    detail=f"File size exceeds maximum allowed size of {max_size_mb}MB"
                )
            return True
        except Exception as e:
            logger.error(f"Error validating file size: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error validating file size: {str(e)}") 