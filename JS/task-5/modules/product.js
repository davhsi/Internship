import { isLikedProduct, getLikedProductsCount } from "./favoritesManager.js";
import { getStarsHtml } from "./filter.js";
import { $, fmtCur } from "./helpers.js";

const bgColors = ["#e8f5e9", "#fdf2f8", "#f3f4f6", "#fffbeb", "#f0fdf4"];
const getTagHtml = (tag) => {
  if (!tag) return "";

  const t = tag.toLowerCase();
  const isAlert = ["hot", "-15%", "-20%"].includes(t);

  return `<span class="tag-pill ${
    isAlert ? "alert" : t === "new" ? "info" : ""
  }">${tag}</span>`;
};

const renderProduct = (p) => {
  const isFav = isLikedProduct(p.id);

  return `
    <div class="product-card">
      <div class="img-container" style="background:${
        bgColors[p.id % bgColors.length]
      }">

        ${getTagHtml(p.tag)}

        <button class="heart-toggle-btn" data-id="${p.id}">
          <img src="./assets/${
            isFav ? "full-heart" : "empty-heart"
          }.png" width="20" height="20" alt="heart" />
        </button>

        <img src="${p.image}" alt="product-img" id="product-img" />
      </div>

      <div class="product-description">
        <p class="category">${p.category.toUpperCase()}</p>
        <p class="name">${p.name}</p>

        <div class="rating-row">
          ${getStarsHtml(p.rating)}
          <span class="rating-val">${p.rating} (234)</span>
        </div>

        <div class="price-row">
          <div class="prices">
            <span class="old-price">${fmtCur(p.price + 200)}</span>
            <span class="price">${fmtCur(p.price)}</span>
          </div>
          <button class="add-to-cart" data-id="${p.id}">+ Add</button>
        </div>
      </div>
    </div>
  `;
};

export function buildProductGrid(products) {
  const grid = document.querySelector(".grid-container");
  if (!grid) return;

  if (products.length === 0) {
    grid.innerHTML = `<p class="no-products">No products found.</p>`;
    return;
  }

  grid.innerHTML = products.map(renderProduct).join("");
}

export function updateHeartBadge() {
  const badge = $("heart-badge");
  if (!badge) return;
  const count = getLikedProductsCount();
  badge.textContent = count;
  badge.style.display = count > 0 ? "block" : "none";
}

export function updateActiveTags(count, currentFilters) {
  const showingCount = $("showing-count");
  if (showingCount) showingCount.textContent = count;
  
  const container = $("active-tags");
  if (!container) return;

  const tag = (label, type, prim = false) => `<div class="filter-tag ${prim ? "primary" : ""}">${label} <button data-type="${type}">✕</button></div>`;
  const tags = [tag(currentFilters.category || "All Products", "category", true)];
  if (currentFilters.maxPrice < 3000) tags.push(tag(`Under Rs. ${currentFilters.maxPrice}`, "price"));
  if (currentFilters.minRating > 0) tags.push(tag(`${currentFilters.minRating}+ Stars`, "rating"));
  
  container.innerHTML = tags.join("");
}

export function initGridEvents(allProducts, addToCart, displayCart, toggleLikedProduct) {
  document.querySelector(".grid-container")?.addEventListener("click", (e) => {
    const productId = parseInt(e.target.closest("[data-id]")?.dataset.id);
    if (!productId) return;

    if (e.target.classList.contains("add-to-cart")) {
      const p = allProducts.find(x => x.id === productId);
      if (p) { 
        addToCart(p); 
        displayCart(); 
        if (window.innerWidth <= 800) $("cart-tab-btn")?.click(); 
      }
    }

    const heartBtn = e.target.closest(".heart-toggle-btn");
    if (heartBtn) {
      toggleLikedProduct(productId);
      updateHeartBadge();
      const img = heartBtn.querySelector("img");
      if (img) img.src = `./assets/${isLikedProduct(productId) ? 'full-heart' : 'empty-heart'}.png`;
    }
  });
}