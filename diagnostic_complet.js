// TEST COMPLET DE DIAGNOSTIC
console.clear();
console.log("=== DIAGNOSTIC COMPLET ===");

// 1. Vérifier que les éléments existent
console.log("1. VÉRIFICATION DES ÉLÉMENTS:");
const orderForm = document.getElementById('orderForm');
const submitBtn = orderForm?.querySelector('button[type="submit"]');
const productIdInput = orderForm?.querySelector('input[name="product_id"]');
const quantityInput = orderForm?.querySelector('input[name="quantity"]');

console.log("   - orderForm:", !!orderForm, orderForm);
console.log("   - submitBtn:", !!submitBtn, submitBtn);
console.log("   - productIdInput:", !!productIdInput);
console.log("   - quantityInput:", !!quantityInput);

// 2. Vérifier les événements
console.log("2. VÉRIFICATION DES ÉVÉNEMENTS:");
console.log("   - orderForm.onsubmit:", typeof orderForm?.onsubmit, orderForm?.onsubmit);

// 3. Test manuel DIRECT
console.log("3. TEST MANUEL DIRECT:");
if (orderForm && submitBtn) {
  // Supprimer tous les anciens événements
  orderForm.onsubmit = null;
  
  // Test ultra-simple
  orderForm.addEventListener('submit', function(e) {
    e.preventDefault();
    console.log("🎉 ÉVÉNEMENT SUBMIT REÇU !");
    
    // Test basique sans API
    const formData = new FormData(orderForm);
    const productId = formData.get('product_id');
    const quantity = formData.get('quantity');
    
    console.log("📝 Données du formulaire:", { productId, quantity });
    
    if (productId && quantity) {
      alert(`✅ FORMULAIRE FONCTIONNE !\nProduit: ${productId}, Quantité: ${quantity}`);
      
      // Test d'API simple
      console.log("🚀 Test d'API...");
      fetch('/api/products')
        .then(res => res.json())
        .then(data => {
          console.log("📦 API répond:", data);
          alert(`✅ API FONCTIONNE ! ${data.products?.length || 0} produits trouvés`);
        })
        .catch(err => {
          console.error("❌ Erreur API:", err);
          alert(`❌ Erreur API: ${err.message}`);
        });
    } else {
      alert("❌ Veuillez remplir les champs");
    }
  });
  
  console.log("✅ Événement de test attaché");
  console.log("👉 Maintenant, remplissez le formulaire et cliquez sur 'Créer'");
} else {
  console.error("❌ Éléments manquants !");
}

// 4. Test de l'API directement
console.log("4. TEST API DIRECT:");
fetch(window.location.origin + '/api/products')
  .then(res => {
    console.log("📡 Réponse API:", res.status, res.statusText);
    return res.json();
  })
  .then(data => {
    console.log("📦 Données API:", data);
  })
  .catch(err => {
    console.error("❌ Erreur API directe:", err);
  });
