const thumbnails = document.querySelectorAll(".thumbnail");
const lightbox = document.querySelector(".lightbox");
const lightboxImg = document.querySelector(".lightbox-img");
const closeBtn = document.querySelector(".close-btn");

thumbnails.forEach((thumbnail) => {
  thumbnail.addEventListener("click", function () {
    lightbox.style.display = "flex";
    lightboxImg.src = this.src;
  });
});

closeBtn.addEventListener("click", function () {
  lightbox.style.display = "none";
});

lightbox.addEventListener("click", function (e) {
  if (e.target !== lightboxImg) {
    lightbox.style.display = "none";
  }
});