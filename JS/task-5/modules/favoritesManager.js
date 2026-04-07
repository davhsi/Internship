export function getLikedProducts() {
  const favoritesJSON = localStorage.getItem("liked_products");
  return favoritesJSON ? JSON.parse(favoritesJSON) : [];
}

export function saveLikedProducts(favorites) {
  localStorage.setItem("liked_products", JSON.stringify(favorites));
}

export function toggleLikedProduct(productId) {
  const favorites = getLikedProducts();
  const index = favorites.indexOf(productId);
  if (index >= 0) {
    favorites.splice(index, 1);
  } else {
    favorites.push(productId);
  }
  saveLikedProducts(favorites);
}

export function isLikedProduct(productId) {
  return getLikedProducts().includes(productId);
}

export function getLikedProductsCount() {
  return getLikedProducts().length;
}
