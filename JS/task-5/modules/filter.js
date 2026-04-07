import { $ } from "./helpers.js";

export const getStarsHtml = (rating) => {
  const full = Math.floor(rating);
  const hasHalf = rating - full >= 0.25;
  const empty = 5 - full - (hasHalf ? 1 : 0);

  const img = (src, alt) =>
    `<img src="./assets/${src}.png" width="14" height="14" alt="${alt}" />`;

  return `<span class="stars-img-row" style="display:inline-flex; align-items:center; gap:2px;">
    ${img("full-star", "★").repeat(full)}${hasHalf ? img("half-star", "½") : ""}${img("empty-star", "☆").repeat(empty)}
  </span>`;
};

export function renderRatingList() {
  const ratingList = $("rating-list");
  if (!ratingList) return;

  const ratings = [
    { value: 0, label: "All Ratings" },
    { value: 5, label: "5 stars" },
    { value: 4.5, label: "4.5+ stars" },
    { value: 4, label: "4+ stars" },
    { value: 3, label: "3+ stars" },
  ];

  ratingList.innerHTML = ratings
    .map(
      (r, idx) => `
    <li class="rating-item ${idx === 0 ? "active" : ""}" data-rating="${r.value}">
      ${getStarsHtml(r.value)} <span style="margin-left:4px;">${r.label}</span>
    </li>
  `,
    )
    .join("");
}

export function initSidebarFilters(updateFilterState) {
  const setupList = (id, key) => $(id)?.addEventListener("click", (e) => {
    const item = e.target.closest("[data-" + key + "]");
    if (!item) return;
    item.parentElement.querySelectorAll(".active").forEach(el => el.classList.remove("active"));
    item.classList.add("active");
    updateFilterState(key === "category" ? "category" : "minRating", parseFloat(item.dataset[key]) || item.dataset[key]);
  });

  setupList("category-list", "category");
  setupList("rating-list", "rating");

  const priceSlider = $("price-range");
  if (priceSlider) {
    const sync = () => {
      const v = priceSlider.value, p = (v / 3000) * 100;
      priceSlider.style.background = `linear-gradient(to right, #10b981 ${p}%, #4b5563 ${p}%)`;
      const label = $("price-max-label");
      if (label) label.textContent = `Rs. ${v}`;
    };
    priceSlider.addEventListener("input", () => { sync(); updateFilterState("maxPrice", parseInt(priceSlider.value)); });
    sync();
  }

  $("search-input")?.addEventListener("input", e => updateFilterState("searchTerm", e.target.value));
}

export function initActiveTags() {
  $("active-tags")?.addEventListener("click", (e) => {
    const type = e.target.closest("button")?.dataset.type;
    if (type === "category") document.querySelector('.category-item[data-category=""]')?.click();
    else if (type === "price") {
      const slider = $("price-range");
      if (slider) { slider.value = 3000; slider.dispatchEvent(new Event("input")); }
    } else if (type === "rating") document.querySelector('.rating-item[data-rating="0"]')?.click();
  });
}

export function populateCategoryBadgeCounts(products) {
  const counts = {};
  products.forEach((p) => (counts[p.category] = (counts[p.category] || 0) + 1));

  const allCount = $("count-all");
  if (allCount) allCount.textContent = products.length;

  ["electronics", "clothing", "book"].forEach((cat) => {
    const el = $(`count-${cat}`);
    if (el) el.textContent = counts[cat] || 0;
  });
}
