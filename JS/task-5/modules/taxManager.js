const TAX_RATE = 0.07;

export function getTaxRate() {
  return TAX_RATE * 100;
}

export function breakdownTotal(subtotal, discountAmount = 0) {
  const afterDiscount = subtotal - discountAmount;
  const tax = afterDiscount * TAX_RATE;
  return {
    subtotal,
    discount: discountAmount,
    afterDiscount,
    tax,
    total: afterDiscount + tax,
  };
}
