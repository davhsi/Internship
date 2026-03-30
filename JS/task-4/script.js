const quoteContainer = document.querySelector(".quote-container");
const loading = document.querySelector(".loading");

let page = 1;
const limit = 10;
const API_URL = "https://dummyjson.com/quotes";

let isLoading = false;

async function fetchQuotes() {
  if (isLoading) return;
  isLoading = true;
  loading.style.display = "block";
  try {
    const response = await fetch(
      `${API_URL}?limit=${limit}&skip=${(page - 1) * limit}`,
    );
    const data = await response.json();

    if (data.quotes.length === 0) {
      loading.textContent = "No more quotes";
      loading.style.display = "block";
      return;
    }

    data.quotes.forEach((q) => {
      const quoteElement = document.createElement("div");
      quoteElement.classList.add("quote");
      quoteElement.innerHTML = `
        <h2>${q.quote}</h2>
        <p>Author: ${q.author}</p>`;
      quoteContainer.appendChild(quoteElement);
    });

    page++;
    loading.style.display = "none";
  } catch (err) {
    console.log("Error loading quotes", err);
  } finally {
    isLoading = false;
  }
}

window.addEventListener("scrollend", () => {
  if (isLoading) return;
  fetchQuotes();
});

fetchQuotes();
