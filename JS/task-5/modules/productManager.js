export async function fetchProducts() {
  try {
    const res = await fetch("data.json");
    return await res.json();
  } catch (err) {
    console.error("Error fetching data", err);
    return [];
  }
}
