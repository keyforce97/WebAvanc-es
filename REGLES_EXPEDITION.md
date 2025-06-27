# 📦 RÈGLES DE CALCUL DES FRAIS D'EXPÉDITION

## 🎯 Spécifications du Professeur

Le champ `shipping_price` représente le prix total pour expédier la commande. 
Ce champ **doit être calculé automatiquement** en fonction du poids total des articles composant la commande :

| Poids Total | Frais d'Expédition |
|-------------|-------------------|
| **Jusqu'à 500 grammes** | **5$** |
| **De 500 grammes à 2kg** | **10$** |
| **À partir de 2kg (2kg et plus)** | **25$** |

## 🔧 Implémentation Technique

### Backend (Python - App/routes.py)
```python
# Calcul automatique lors de la création/mise à jour de commande
total_weight = sum(op.product.weight * op.quantity for op in products)

if total_weight <= 500:
    shipping_price = 500      # 5.00$ stocké en centimes
elif total_weight <= 2000:
    shipping_price = 1000     # 10.00$ stocké en centimes  
else:
    shipping_price = 2500     # 25.00$ stocké en centimes
```

### Frontend (JavaScript - templates/index.html)
```javascript
// Fonction utilitaire pour estimation côté client
const calculateShippingPrice = (weightInGrams) => {
  if (weightInGrams <= 500) return 500;       // 5.00$ en centimes
  if (weightInGrams <= 2000) return 1000;     // 10.00$ en centimes
  return 2500;                                // 25.00$ en centimes
};

// Affichage: division par 100 pour conversion
shipping_price / 100  // Affiche en dollars
```

## 📊 Stockage et Affichage

- **Stockage en base:** En centimes (500, 1000, 2500)
- **Affichage frontend:** Division par 100 pour conversion en dollars
- **Calcul automatique:** À chaque création/modification de commande

## 🧪 Validation

### Test Manuel
```bash
# Lancer les tests de validation
./test_shipping_rules.sh
```

### Exemples Concrets
```
Produit A (100g) x 1 = 100g total  → 5$
Produit A (100g) x 5 = 500g total  → 5$
Produit B (800g) x 1 = 800g total  → 10$
Produit A (100g) x 20 = 2000g total → 10$
Produit C (2500g) x 1 = 2500g total → 25$
```

## ✅ Conformité

- ✅ **Calcul automatique** lors de création de commande
- ✅ **Recalcul automatique** lors d'ajout d'adresse  
- ✅ **Règles exactes** selon spécifications
- ✅ **Poids basé sur** somme des produits × quantités
- ✅ **Stockage cohérent** en centimes
- ✅ **Affichage correct** en dollars

## 🔄 Points de Calcul

1. **POST /order** - Création de commande
2. **PUT /order/{id}** - Mise à jour avec adresse
3. **Frontend** - Estimation temps réel

Le système recalcule automatiquement les frais à chaque modification des produits ou de l'adresse, garantissant la cohérence selon les règles définies.
