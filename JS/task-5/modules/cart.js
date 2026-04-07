import {
  getCart,
  updateQuantity,
  getCartCount,
  getCartTotal,
  getDiscountInfo,
  applyDiscount,
  removeDiscount,
} from "./cartManager.js";

import { breakdownTotal, getTaxRate } from "./taxManager.js";
import { $, fmtCur } from "./helpers.js";

const renderCartItem = (item) => `
  <div class="cart-item">
    <div class="cart-item-thumb"><img src="${item.image || ""}" alt="${item.name}" /></div>
    <div class="cart-item-info">
      <p class="cart-item-name">${item.name}</p>
      <p class="cart-item-meta">${item.category || ""}</p>
      <div class="quantity-selector">
        <button type="button" class="decrement-btn" data-id="${item.id}">-</button>
        <input type="number" class="qty-input" value="${item.quantity}" data-id="${item.id}" min="1" />
        <button type="button" class="increment-btn" data-id="${item.id}">+</button>
      </div>
    </div>
    <div class="cart-item-right">
      <span class="cart-item-price">${fmtCur(item.price * item.quantity)}</span>
      <button class="remove-item" data-id="${item.id}">remove</button>
    </div>
  </div>
`;

export function displayCart() {
  const cart = getCart();
  const count = getCartCount();
  const subtotal = getCartTotal();
  const discountInfo = getDiscountInfo();
  const breakdown = breakdownTotal(
    subtotal,
    subtotal * (discountInfo.discount || 0),
  );

  const setText = (id, text) => {
    const el = $(id);
    if (el) el.textContent = text;
  };

  setText("cart-item-count", count === 1 ? "1 item" : `${count} items`);
  setText("desktop-cart-badge", count);
  setText("cart-subtotal", fmtCur(breakdown.subtotal));
  setText("tax-label", `Tax (${getTaxRate().toFixed(1)}%)`);
  setText("tax-amount", fmtCur(breakdown.tax));
  setText("cart-total", fmtCur(breakdown.total));

  const cartTabBtn = $("cart-tab-btn");
  if (cartTabBtn)
    cartTabBtn.textContent = count > 0 ? `Cart (${count})` : "Cart";

  const subtotalLabel = $("subtotal-label");
  if (subtotalLabel)
    subtotalLabel.textContent =
      count > 0
        ? `Subtotal (${count} item${count > 1 ? "s" : ""})`
        : "Subtotal";

  const hasDiscount = discountInfo.discount > 0;
  const discountRow = $("discount-row");
  const removeBtn = $("remove-coupon-btn");

  if (discountRow) discountRow.style.display = hasDiscount ? "" : "none";
  if (removeBtn) removeBtn.style.display = hasDiscount ? "" : "none";

  if (hasDiscount) {
    setText("discount-label", `Promo ${discountInfo.discountCode}`);
    setText("discount-amount", `-${fmtCur(breakdown.discount)}`);
  }

  const cartItems = $("cart-items");
  if (!cartItems) return;
  cartItems.innerHTML =
    cart.length === 0
      ? '<p class="empty">Your cart is empty.</p>'
      : cart.map(renderCartItem).join("");
}


export function initCartUI() {
  const sidebar = $("cart-sidebar");
  if (!sidebar) return;

  sidebar.addEventListener("click", (e) => {
    const { id, classList, dataset } = e.target;
    if (id === "checkout-btn") return alert("Proceeding to checkout...");

    if (id === "apply-coupon-btn") {
      const code = $("coupon-input")?.value.trim();
      const msgEl = $("coupon-applied-msg");
      if (!code) {
        if (msgEl) {
          msgEl.textContent = "Please enter a promo code.";
          msgEl.style.display = "";
          msgEl.className = "coupon-applied-msg error";
        }
        return;
      }
      const result = applyDiscount(code);
      if (msgEl) {
        msgEl.textContent = result.success
          ? `✓ ${code.toUpperCase()} applied -- ${Math.round(getDiscountInfo().discount * 100)}% off!`
          : result.message;
        msgEl.style.display = "";
        msgEl.className = result.success
          ? "coupon-applied-msg success"
          : "coupon-applied-msg error";
      }
      return displayCart();
    }

    if (id === "remove-coupon-btn") {
      removeDiscount();
      return displayCart();
    }

    const productId = parseInt(e.target.dataset.id);
    const item = getCart().find((i) => i.id === productId);
    if (!item) return;

    if (classList.contains("increment-btn"))
      updateQuantity(productId, item.quantity + 1);
    else if (classList.contains("decrement-btn"))
      updateQuantity(productId, item.quantity - 1);
    else if (classList.contains("remove-item")) updateQuantity(productId, 0);
    else return;

    displayCart();
  });

  sidebar.addEventListener("change", (e) => {
    if (e.target.classList.contains("qty-input")) {
      const id = parseInt(e.target.dataset.id);
      const qty = Math.max(1, parseInt(e.target.value) || 1);
      updateQuantity(id, qty);
      displayCart();
    }
  });

  displayCart();
}

export function initMobileTabs() {
  const tabs = $("mobile-tabs");
  if (!tabs) return;

  const productsPanel = $("products-panel");
  const cartPanel = $("cart-sidebar");

  tabs.addEventListener("click", (e) => {
    const btn = e.target.closest(".tab-btn");
    if (!btn) return;

    document
      .querySelectorAll(".tab-btn")
      .forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");

    if (btn.dataset.tab === "products") {
      productsPanel.classList.remove("tab-hidden");
      cartPanel.classList.add("tab-hidden");
    } else {
      cartPanel.classList.remove("tab-hidden");
      productsPanel.classList.add("tab-hidden");
    }
  });
}
