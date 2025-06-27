// Script de test pour debugger le problème
console.log("=== Test de l'API ===");

// Test 1: Vérifier l'URL de base
console.log("1. URL de base:", window.location.origin);

// Test 2: Appel direct à l'API
fetch(window.location.origin + '/api/products')
  .then(response => {
    console.log("2. Réponse:", response.status, response.statusText);
    console.log("2. Content-Type:", response.headers.get('content-type'));
    return response.text();
  })
  .then(text => {
    console.log("2. Texte reçu (premiers 100 chars):", text.substring(0, 100));
    try {
      const json = JSON.parse(text);
      console.log("2. Parsing JSON réussi, nombre de produits:", json.products?.length);
    } catch (e) {
      console.error("2. Erreur parsing JSON:", e.message);
      console.log("2. Texte complet:", text);
    }
  })
  .catch(error => {
    console.error("2. Erreur fetch:", error);
  });
