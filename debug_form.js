// Test de débogage pour le formulaire
console.log("=== TEST DE DÉBOGAGE FORMULAIRE ===");

// 1. Vérifier que les éléments existent
const orderForm = document.getElementById('orderForm');
const submitBtn = orderForm?.querySelector('button[type="submit"]');

console.log("1. Éléments trouvés:");
console.log("   - orderForm:", !!orderForm, orderForm);
console.log("   - submitBtn:", !!submitBtn, submitBtn);

// 2. Vérifier les événements attachés
console.log("2. Événements attachés:");
console.log("   - orderForm.onsubmit:", typeof orderForm?.onsubmit);

// 3. Test d'attachement manuel
if (orderForm) {
  console.log("3. Attachement manuel d'un test...");
  
  // Supprimer l'ancien événement
  orderForm.onsubmit = null;
  
  // Attacher un nouveau test simple
  orderForm.addEventListener('submit', function(e) {
    e.preventDefault();
    console.log("🎉 ÉVÉNEMENT SUBMIT DÉTECTÉ !");
    alert("✅ Le formulaire fonctionne !");
  });
  
  console.log("✅ Test attaché. Essayez de cliquer sur 'Créer'");
} else {
  console.error("❌ Formulaire non trouvé !");
}

// 4. Test direct du bouton
if (submitBtn) {
  submitBtn.onclick = function() {
    console.log("🎯 CLIC DIRECT SUR LE BOUTON !");
    alert("✅ Le bouton répond !");
  };
}
