# Intégration HYCU avec Visual TOM
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.md)&nbsp;
[![fr](https://img.shields.io/badge/lang-en-red.svg)](README-fr.md)  
Ce projet permet l'intégration de HYCU Backup avec le planificateur Visual TOM.

La solution fournit un script Python qui peut déclencher et surveiller les sauvegardes HYCU via l'API HYCU, avec des capacités de surveillance et de rapport complètes.

Le script Python `vtom-hycu_backup-jobs.py` est utilisé avec sa queue batch associé pour les environnements Windows et Linux.

# Avertissement
Aucun Support et aucune Garantie ne sont fournis par Absyss SAS pour ce projet et le matériel associé. L'utilisation des fichiers de ce projet est à vos propres risques.
Absyss SAS n'assume aucune responsabilité pour les dommages causés par l'utilisation de l'un des fichiers proposés ici via ce dépôt Github.
Des jours de conseil peuvent être demandés pour aider à la mise en œuvre.

# Prérequis

  * Visual TOM 7.1.2 ou supérieur
  * Windows avec PowerShell installé
  * Python 3.x ou supérieur
  * Accès à l'API HYCU avec un token d'authentification valide
  * Connectivité réseau au serveur HYCU

# Instructions

## Intégration HYCU Backup

Le script fournit une gestion complète des sauvegardes HYCU via l'API HYCU. Il prend en charge les actions suivantes :
  * Déclencher des travaux de sauvegarde avec des configurations personnalisées
  * Surveiller le statut d'exécution des sauvegardes en temps réel
  * Générer des rapports d'exécution détaillés
  * Méthodes d'authentification multiples (token, fichier, variables d'environnement)
  * Intervalles de surveillance et délais d'attente configurables
  * Gestion d'erreurs complète avec des codes de sortie spécifiques

## Fonctionnalités

- **Déclenchement de sauvegarde** : Démarrer les sauvegardes HYCU avec des configurations personnalisées
- **Surveillance en temps réel** : Surveiller le statut d'exécution des sauvegardes avec des intervalles configurables
- **Rapports détaillés** : Générer des rapports d'exécution complets
- **Authentification flexible** : Support pour l'authentification par token, fichier et variables d'environnement
- **Gestion d'erreurs** : Gestion d'erreurs complète avec des codes de sortie spécifiques
- **Gestion des délais d'attente** : Délais d'attente de surveillance configurables pour les sauvegardes de longue durée

# Guide d'utilisation

Le modèle d'application doit être importé dans Visual TOM.
Le travail Visual TOM doit être exécuté depuis un système avec accès réseau au serveur HYCU.

Notes :
Le script Python `vtom-hycu_backup-jobs.py` utilise des variables génériques et prend en charge plusieurs méthodes d'authentification.

## Tests avec l'intégration HYCU

### Exécution via queue Visual TOM
```batch
submit_queue_hycu.bat "Sauvegarde quotidienne" "https://hycu.example.com" "VOTRE_TOKEN" "" "30" "3600" "" "" ""
submit_queue_hycu.bat "Sauvegarde de production" "https://hycu.example.com" "" "auth.json" "60" "7200" "backup_config.json" "" "verbose"
submit_queue_hycu.bat "Sauvegarde rapide" "https://hycu.example.com" "VOTRE_TOKEN" "" "30" "3600" "" "no-monitor" ""
```

### Exécution directe (Python uniquement)
  ``` Python
python vtom-hycu_backup-jobs.py --backup-name "Sauvegarde quotidienne" --url https://hycu.example.com --auth-token VOTRE_TOKEN
python vtom-hycu_backup-jobs.py --backup-name "Sauvegarde de production" --url https://hycu.example.com --auth-file auth.json
python vtom-hycu_backup-jobs.py --backup-name "Sauvegarde rapide" --url https://hycu.example.com --auth-token VOTRE_TOKEN --no-monitor
  ```
  
## Méthodes d'authentification

### 1. Authentification par token
```bash
python vtom-hycu_backup-jobs.py --backup-name "Sauvegarde quotidienne" --url https://hycu.example.com --auth-token VOTRE_TOKEN
```

### 2. Fichier d'authentification
Créer un fichier JSON avec les identifiants d'authentification :
```json
{
  "token": "votre_token_auth_hycu_ici",
  "username": "admin",
  "api_version": "v1"
}
```

Puis l'utiliser avec :
```bash
python vtom-hycu_backup-jobs.py --backup-name "Sauvegarde quotidienne" --url https://hycu.example.com --auth-file auth.json
```

### 3. Variables d'environnement
```bash
export HYCU_URL=https://hycu.example.com
export HYCU_AUTH_TOKEN=VOTRE_TOKEN
python vtom-hycu_backup-jobs.py --backup-name "Sauvegarde quotidienne"
```

## Fichiers de configuration

### Configuration de sauvegarde
Créer un fichier de configuration de sauvegarde `backup_config.json` :
```json
{
  "name": "Exemple de sauvegarde de production",
  "type": "full",
  "retention": "30 jours",
  "compression": true,
  "encryption": true,
  "schedule": "quotidien",
  "target": "base-de-donnees-production",
  "priority": "haute",
  "notifications": {
    "email": "admin@example.com",
    "webhook": "https://webhook.example.com/backup-status"
  }
}
```

## Codes de sortie

| Code | Description |
|------|-------------|
| 0 | Succès - Sauvegarde terminée avec succès |
| 1 | Erreur de configuration - URL ou authentification manquante |
| 2 | Erreur de surveillance - Erreur pendant la surveillance de la sauvegarde |
| 3 | Erreur de délai d'attente - Surveillance de la sauvegarde expirée |
| 4 | Sauvegarde échouée - Exécution de la sauvegarde échouée |
| 5 | Sauvegarde annulée - La sauvegarde a été annulée |
| 6 | Statut inconnu - La sauvegarde s'est terminée avec un statut inconnu |
| 7 | Interruption utilisateur - Opération annulée par l'utilisateur |
| 8 | Erreur inattendue - Une erreur inattendue s'est produite |

## Sortie du rapport

Le script génère un rapport détaillé après la fin de la sauvegarde :

```
==================================================
RAPPORT D'EXÉCUTION DE SAUVEGARDE HYCU
==================================================
Horodatage : 2024-01-15T10:30:45.123456
ID du travail : backup_12345
Statut : terminé
Heure de début : 2024-01-15T10:30:45
Heure de fin : 2024-01-15T10:35:22
Progression : 100%
==================================================
```

## Gestion d'erreurs

Le script inclut une gestion d'erreurs complète :
- **Erreurs réseau** : Problèmes de connexion avec l'API HYCU
- **Erreurs d'authentification** : Tokens invalides ou expirés
- **Erreurs de configuration** : Paramètres requis manquants
- **Erreurs de délai d'attente** : Délais d'attente de surveillance des sauvegardes
- **Erreurs API** : Erreurs de réponse de l'API HYCU

Toutes les erreurs sont enregistrées avec des messages appropriés et des codes de sortie.

## Considérations de sécurité

- Stocker les tokens d'authentification de manière sécurisée
- Utiliser des variables d'environnement pour les données sensibles
- S'assurer que les fichiers d'authentification ont les permissions appropriées
- Considérer l'utilisation de fichiers d'authentification chiffrés pour un usage en production

## Dépannage

### Problèmes courants

1. **Authentification échouée** : Vérifier que votre token est valide et non expiré
2. **Connexion refusée** : Vérifier l'URL HYCU et la connectivité réseau
3. **Erreurs de délai d'attente** : Augmenter la valeur de délai d'attente pour les sauvegardes de longue durée
4. **Permission refusée** : S'assurer des permissions de fichier appropriées pour les fichiers d'authentification

### Mode débogage

Utiliser le drapeau `--verbose` pour un enregistrement détaillé :
```bash
python vtom-hycu_backup-jobs.py --verbose --backup-name "Sauvegarde de débogage"
```

## Compatibilité API

Ce script est conçu pour fonctionner avec l'API HYCU v1. Les endpoints suivants sont utilisés :
- `POST /api/v1/backups` - Déclencher une sauvegarde
- `GET /api/v1/backups/{job_id}/status` - Obtenir le statut de la sauvegarde

# Licence
Ce projet est sous licence Apache 2.0 - voir le fichier [LICENSE](license) pour plus de détails

# Code de conduite
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS a adopté le [Contributor Covenant](CODE_OF_CONDUCT.md) comme Code de conduite, et nous nous attendons à ce que les participants au projet s'y conforment. Veuillez lire le [texte complet](CODE_OF_CONDUCT.md) pour comprendre quelles actions seront et ne seront pas tolérées.
