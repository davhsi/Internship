let cart = [];
let currentDiscount = null;

export function loadCart() {
  const existingCart = localStorage.getItem("cart");
  if (existingCart) {
    cart = JSON.parse(existingCart);
  }
}

export function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
}

export function getCart() {
  return cart;
}

export function addToCart(product) {
  const existing = cart.find((item) => item.id === product.id);
  if (existing) {
    updateQuantity(product.id, existing.quantity + 1);
  } else {
    cart.push({ ...product, quantity: 1 });
    saveCart();
  }
}

export function updateQuantity(productId, quantity) {
  const index = cart.findIndex((item) => item.id === productId);
  if (index === -1) return;

  if (quantity <= 0) {
    cart.splice(index, 1);
  } else {
    cart[index].quantity = quantity;
  }
  saveCart();
}

export function getCartTotal() {
  return cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export function getCartCount() {
  return cart.reduce((sum, item) => sum + item.quantity, 0);
}

export function applyDiscount(code) {
  const validCodes = { DAV10: 0.1, DAV20: 0.2 };
  const discount = validCodes[code.toUpperCase()];
  if (!discount) return { success: false, message: "Invalid coupon code" };

  currentDiscount = { discount, discountCode: code.toUpperCase() };
  return {
    success: true,
    message: `Coupon applied! ${discount * 100}% discount`,
  };
}

export function getDiscountInfo() {
  return currentDiscount || { discount: 0, discountCode: "" };
}

export function removeDiscount() {
  currentDiscount = null;
}
