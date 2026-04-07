import { loadCart, addToCart } from "./modules/cartManager.js";
import { fetchProducts } from "./modules/productManager.js";
import { displayCart, initCartUI, initMobileTabs } from "./modules/cart.js";
import {
  buildProductGrid,
  updateHeartBadge,
  initGridEvents,
  updateActiveTags,
} from "./modules/product.js";
import {
  renderRatingList,
  initSidebarFilters,
  initActiveTags,
  populateCategoryBadgeCounts,
} from "./modules/filter.js";
import { getFilteredProducts } from "./modules/searchFilterManager.js";
import { toggleLikedProduct } from "./modules/favoritesManager.js";

let allProducts = [];
let currentFilters = {
  category: "",
  searchTerm: "",
  maxPrice: 3000,
  minRating: 0,
};

function applyFilters() {
  const filtered = getFilteredProducts(allProducts, currentFilters);
  buildProductGrid(filtered);
  updateActiveTags(filtered.length, currentFilters);
}

function updateFilterState(key, value) {
  currentFilters[key] = value;
  applyFilters();
}

async function start() {
  loadCart();
  allProducts = await fetchProducts();
  populateCategoryBadgeCounts(allProducts);

  initSidebarFilters(updateFilterState);
  renderRatingList();
  initActiveTags();
  initMobileTabs();
  initCartUI();
  initGridEvents(allProducts, addToCart, displayCart, toggleLikedProduct);

  updateHeartBadge();
  applyFilters();
}

document.addEventListener("DOMContentLoaded", start);
