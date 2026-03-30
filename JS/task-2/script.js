const quizContainer = document.querySelector(".quiz-container");
const resultContainer = document.querySelector(".result-container");

let currentQuestionIndex = 0;
let score = 0;
let questions = [];

async function fetchQuestions() {
  try {
    const res = await fetch("questions.json");
    questions = await res.json();
    loadQuestion();
  } catch (err) {
    console.log("Error loading questions from file", err.message);
  }
}

function loadQuestion() {
  if (currentQuestionIndex >= questions.length) {
    showResults();
    return;
  }

  const questionData = questions[currentQuestionIndex];
  quizContainer.innerHTML = `<h2>${currentQuestionIndex + 1}. ${questionData.question}</h2>`;

  questionData.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.innerHTML = option;
    button.classList.add("option");
    button.addEventListener("click", () => {
      checkAnswer(index);
    });
    quizContainer.appendChild(button);
  });
}

function checkAnswer(selectedIndex) {
  if (
    questions[currentQuestionIndex].options[selectedIndex] ===
    questions[currentQuestionIndex].answer
  ) {
    score++;
  }
  currentQuestionIndex++;
  loadQuestion();
}

function showResults() {
  quizContainer.style.display = "none";
  let message = "";
  let color = "";
  if (score < 5) {
    message = "You can do better! Try Again";
    color = "red";
  } else if (score < 9) {
    message = "You did awesome !!";
    color = "orange";
  } else {
    message = "You are a genius !";
    color = "darkgreen";
  }
  resultContainer.innerHTML = `
  <h2 style="color: ${color}">You Scored ${score}/${questions.length}</h2><br>
  <h3 style="color: ${color}">${message}</h3>`;
}

fetchQuestions();
