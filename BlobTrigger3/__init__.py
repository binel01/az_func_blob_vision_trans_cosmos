import logging
import os

import azure.functions as func
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import ImageDescription
from msrest.authentication import CognitiveServicesCredentials

import pymongo

# ===== AZURE BLOB STORAGE =====
# Compte de stockage déclencheur Azure Blob Storage
BLOB_STORAGE_ACCOUNT = os.environ["BLOB_STORAGE_ACCOUNT"]

# ===== AZURE COGNITIVE SERVICES - IMAGE ANALYSIS =====
# Clé de Azure Cognitive Services
VISION_SUBS_KEY = os.environ["VISION_SUBS_KEY"]
# Point d'accès à Azure Cognitive Services
VISION_ENDPOINT = os.environ["VISION_ENDPOINT"]

# ===== COSMOS DB for MONGO DB =====
# Chaîne de connexion à Cosmos DB
DB_CONN_STR = os.environ["DB_CONN_STR"]
# Base de données
DB_NAME = os.getenv("DB_NAME", "azcogimagedescdb1")
# Collection
DB_COLL_NAME = os.getenv("DB_COLL_NAME", "desciptions")


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes\n")
    
    # Détermination de l'URL de l'image uploadée
    image_url = f"https://{BLOB_STORAGE_ACCOUNT}.blob.core.windows.net/{myblob.name}"
    logging.info(f"File URL: {image_url}")

    """
    ========================================================
    1. Analyse de l'image
    ========================================================
    """
    print("===== Description de l'image =====")
    # Récupération duc lient Computer Vision
    vision_client = ComputerVisionClient(VISION_ENDPOINT, CognitiveServicesCredentials(VISION_SUBS_KEY))
    # Génération de la description
    description:ImageDescription = vision_client.describe_image(image_url)
    if (len(description.captions) == 0):
        logging.info("Pas de description détectée")
    else:
        for caption in description.captions:
            logging.info("Description: '{}' avec la probabilité: {}".format(caption.text, caption.confidence))
    
    """
    ========================================================
    2. Sauvegarde de la description dans la base de données
    ========================================================
    """
    logging.info("===== Enregistrement de la description dans la base de données =====")
    # Création du client MongoDB
    mongo_client = pymongo.MongoClient(DB_CONN_STR)
    # Récupération de la base de données
    database = mongo_client[DB_NAME]
    # Récupération de la collection
    collection = database[DB_COLL_NAME]

    # Création de l'objet Description qui sera enregistré dans Cosmos DB
    image_desc = {
        "url": image_url,
        "description": description.captions[0].text,
        "confidence": description.captions[0].confidence
    }

    # Insertion de la description dans la base de données
    result = collection.update_one(
        {"url": image_desc["url"]}, {"$set": image_desc}, upsert=True
    )
    if result == None:
        logging.info("Echec d'insertion dans la base de données")
    else:
        logging.info("Insertion dans la base de donnée réussie !!")

