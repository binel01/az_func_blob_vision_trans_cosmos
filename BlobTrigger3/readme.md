# BlogTrigger3 - Python

Cette fonction permet suite à l'ajout d'un fichier dans un conteneur Azure Blob Storage, de générer une description 
en utilisant Azure Cognitive Services puis sauvegarder cette description dans Azure Cosmos DB.

<Todo> Ajouter la traduction en français de la description obtenue par Computer Vision
<Todo> Ajouter la gestion des exceptions liée aux appels des APIs de services

## Fonctionnement

*Déclencheur*: ajout d'un fichier dans un conteneur Azure Blob Storage
*Action 1*: l'URL du fichier ajouté est envoyé à COMPUTER VISION pour obtenir une description de l'image
*Action 2*: la description obtenue est enregistrée dans Azure Cosmos DB

## Configuration

Afin de faire fonctionner cette fonction, certaines variables d'environnement doivent être définies:
- AzureWebJobsStorage : la chaîne de connexion au compte de stockage utilisé par la fonction
- BLOB_STORAGE_ACCOUNT : le nom du compte de stockage utilisé pour déclencher la fonction
- VISION_SUBS_KEY : la clé à utiliser pour le service Computer Vision Image Analysis
- VISION_ENDPOINT : le point d'accès au service Computer Vision Image Analysis
- DB_CONN_STR : chaîne de connexion à la base de données Cosmos DB for MongoDB
- DB_NAME : nom de la base de données MongoDB
- DB_COLL_NAME : nom de la collection MongoDB



