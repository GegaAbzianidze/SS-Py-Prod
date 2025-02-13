import pyrebase
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FirebaseUtils:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseUtils, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.firebase = None
        self.storage = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase configuration"""
        try:
            config = {
                "apiKey": "AIzaSyCu2tiwtp6OeEr8A_p1TLeJFf8DyWcW1ng",
                "authDomain": "ysnapstationprod.firebaseapp.com",
                "projectId": "snapstationprod",
                "storageBucket": "snapstationprod.firebasestorage.app",
                "messagingSenderId": "750452235005",
                "appId": "1:750452235005:web:01beb7ae946f2272c3fc94",
                "databaseURL": "https://snapstationprod-default-rtdb.europe-west1.firebasedatabase.app"
            }
            
            self.firebase = pyrebase.initialize_app(config)
            self.storage = self.firebase.storage()
            self.db = self.firebase.database()
            logger.debug("Firebase initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Firebase: {str(e)}")
            raise
    
    def upload_file(self, local_file_path, remote_path=None):
        """
        Upload a file to Firebase Storage
        
        Args:
            local_file_path (str): Path to the local file
            remote_path (str, optional): Custom remote path. If None, generates a default path
            
        Returns:
            str: URL of the uploaded file or None if upload fails
        """
        try:
            if not os.path.exists(local_file_path):
                raise FileNotFoundError(f"File not found: {local_file_path}")
            
            if remote_path is None:
                # Generate default remote path based on timestamp and file name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = os.path.basename(local_file_path)
                remote_path = f"uploads/{timestamp}_{file_name}"
            
            # Upload file
            self.storage.child(remote_path).put(local_file_path)
            
            # Get the download URL
            url = self.storage.child(remote_path).get_url(None)
            logger.debug(f"File uploaded successfully: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return None
    
    def upload_media_files(self, file_paths, event_id=None):
        """
        Upload multiple media files to Firebase Storage
        
        Args:
            file_paths (list): List of local file paths
            event_id (str, optional): Event ID to organize files
            
        Returns:
            list: List of URLs for the uploaded files
        """
        try:
            urls = []
            base_path = f"events/{event_id}" if event_id else "uploads"
            
            for file_path in file_paths:
                if os.path.exists(file_path):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name = os.path.basename(file_path)
                    remote_path = f"{base_path}/{timestamp}_{file_name}"
                    
                    # Upload file
                    self.storage.child(remote_path).put(file_path)
                    url = self.storage.child(remote_path).get_url(None)
                    urls.append(url)
                    logger.debug(f"File uploaded successfully: {url}")
                
            return urls
            
        except Exception as e:
            logger.error(f"Error uploading media files: {str(e)}")
            return []
    
    def delete_file(self, remote_path):
        """
        Delete a file from Firebase Storage
        
        Args:
            remote_path (str): Path to the file in Firebase Storage
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            self.storage.delete(remote_path)
            logger.debug(f"File deleted successfully: {remote_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    def create_event(self, event_id, event_data):
        """Create a new event in the Realtime Database"""
        try:
            # Create event in the events node
            result = self.db.child("events").child(event_id).set(event_data)
            if result:
                logger.debug(f"Event created successfully with ID: {event_id}")
                return True
            else:
                logger.error("Failed to create event in database")
                return False
            
        except Exception as e:
            logger.error(f"Error creating event in database: {str(e)}")
            return False 