# 🚀 COMMANDES RAPIDES - VERSION STABLE v1.2

## 🔄 Rollback d'urgence
```bash
# Rollback automatique vers la version stable
./rollback_v1.2.sh

# Ou manuellement
git checkout v1.2-stable
./start.sh
```

## 📊 Vérifications de statut
```bash
# Statut Git
git status
git log --oneline -5

# Statut Docker
docker-compose ps
docker-compose logs -f api
docker-compose logs -f worker

# Test de l'application
curl http://localhost:5002/api/products
```

## 🏷️ Tags et versions
```bash
# Lister les versions stables
git tag -l "*stable*"

# Voir les détails d'une version
git show v1.2-stable

# Créer une nouvelle version stable
git tag -a v1.X-stable -m "Description"
```

## 🔧 Développement
```bash
# Démarrer l'app
./start.sh

# Arrêter l'app  
./stop.sh

# Voir les logs
docker-compose logs -f

# Tests de l'API
./test_api.sh
```

## 📝 Documentation
- `VERSION_STABLE_v1.2.md` - Documentation complète
- `README.md` - Guide d'installation
- `GUIDE_TEST.md` - Guide de test
- `PROJECT_STATUS.md` - Statut du projet

## 🆘 En cas de problème
1. Vérifier les logs: `docker-compose logs -f api`
2. Redémarrer: `./start.sh`  
3. Rollback: `./rollback_v1.2.sh`
4. Vérifier la doc: `VERSION_STABLE_v1.2.md`

## ✅ Features validées v1.2
- [x] Calcul prix correct (28.1$ → 28.1$)
- [x] Statuts avec codes couleur
- [x] Mise à jour automatique paiement
- [x] Popups informatifs détaillés
- [x] Taxes par province
- [x] Paiement asynchrone
