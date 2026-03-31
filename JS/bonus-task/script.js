const pageContainer = document.getElementById("page-container");

const routes = {
  home: HomePage,
  contact: ContactPage,
  about: AboutPage,
};

function getRoute() {
  return window.location.hash.replace("#", "") || "home";
}

function render() {
  const route = getRoute();
  const page = routes[route] || NotFound;
  pageContainer.innerHTML = page();
  setActiveLink(route);
}

function setActiveLink(route) {
  const current = document.querySelector("nav a.active");
  if (current) current.classList.remove("active");

  const next = document.querySelector(`nav a[href="#${route}"]`);
  if (next) next.classList.add("active");
}

window.addEventListener("hashchange", render);
window.addEventListener("load", render);

function HomePage() {
  return `
  <div class="home-page">
    <div class="home-section">
      <div class="home-image">
        <img src="./assets/shop-img.png" alt="shop image" />
      </div>
      <div class="home-text">
        <h3>Welcome to DAV Electronics!</h3>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Iure
          autem temporibus voluptatum aliquam rerum minima ipsam sunt.
        </p>
      </div>
    </div>

    <div class="home-section">
      <div class="home-image">
        <img src="./assets/customer-img.png" alt="customers" />
      </div>
      <div class="home-text">
        <h3>Delivering Best Quality Products</h3>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Fuga,
          ipsa voluptate ab nihil adipisci quasi aliquam consequuntur.
        </p>
      </div>
    </div>
  </div>
  `;
}
function ContactPage() {
  return `
  <div class="contact-page">
    <div class="form-container">
      <h2>Contact Form</h2>

      <form>
        <label for="name">Name</label>
        <input type="text" id="name" placeholder="Enter your name" />

        <label for="email">Email</label>
        <input type="email" id="email" placeholder="Enter your email" />

        <label for="message">Query</label>
        <textarea id="message" placeholder="Enter your query"></textarea>

        <button type="submit">Submit</button>
      </form>
    </div>
  </div>
  `;
}

function AboutPage() {
  return `
  <div class="about-page">
    <h2 class="about-header">About Us</h2>
    <div class="about-content">
      <div class="about-text">
        <p>
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Ipsam
          aliquid, incidunt architecto deleniti molestias sed, quod maxime
          ex atque delectus doloremque facilis quo nemo harum pariatur
          iste iusto odit nam ullam laboriosam consequatur numquam minima.
          Qui vitae vero assumenda enim officiis id commodi iusto possimus
          veritatis! Voluptatem a fugit possimus illum facilis omnis
          quisquam, labore earum amet. Laborum qui libero dolor
          perspiciatis porro iure fugit eveniet consequatur minima dolore?
          Minus, deleniti optio. Numquam aliquid quisquam recusandae!
          Illum necessitatibus molestias magni saepe quos voluptatem,
          debitis fugiat dolore! Assumenda delectus quam voluptatem, id,
          omnis animi reiciendis ea laboriosam sit vero velit odio.
        </p>
      </div>
      <div class="about-image">
        <img src="./assets/about-img.png" alt="Our Team" />
      </div>
    </div>
  </div>
  `;
}

function NotFound() {
  return `
  <div class="not-found">
    <h2>404 - Page Not Found</h2>
    <p>The page does not exist.</p>
  </div>
  `;
}
