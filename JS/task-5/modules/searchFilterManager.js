export function getFilteredProducts(products, { category = '', searchTerm = '', maxPrice = Infinity, minRating = 0 } = {}) {
  if (products.length === 0) return [];
  const term = searchTerm.toLowerCase();

  return products.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(term);
    const matchesCategory = category === '' || product.category === category;
    const matchesPrice = product.price <= maxPrice;
    const matchesRating = product.rating >= minRating;
    return matchesSearch && matchesCategory && matchesPrice && matchesRating;
  });
}
