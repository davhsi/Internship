const addBtn = document.getElementById("addBtn");
const expenseName = document.getElementById("expenseName");
const expenseCategory = document.getElementById("expenseCategory");
const expenseAmount = document.getElementById("expenseAmount");
const expenseList = document.getElementById("expenseList");
const total = document.getElementById("total");

let expenses = JSON.parse(localStorage.getItem("expenses")) || [];

renderAll()

addBtn.addEventListener("click", () => {
   const name = expenseName.value.trim();
   const amount = parseFloat(expenseAmount.value);
   const category = expenseCategory.value;
   
   if(name === '' || isNaN(amount) || amount <= 0){
    alert("Invalid name and amount");
    return;
   }

   const newExpense = {name, amount, category};
   expenses.push(newExpense);
   localStorage.setItem('expenses', JSON.stringify(expenses));

   addExpenseToDOM(newExpense, expenses.length -1);
   updateTotal();
   
   expenseName.value = '';
   expenseAmount.value = '';
});

function addExpenseToDOM(expense, index) {
    const li = document.createElement('li');
    li.setAttribute("data-index", index);
    li.innerHTML = `

        <div class = "expense-info">
            <p class="name">${expense.name}</p>
            <p class="category">${expense.category}</p>
        </div>
        <div class="expense-right">
            <span class="amount>Rs${expense.amount}"</span>
            <button class="delete-btn">x</button>
        </div>

    `;

    li.querySelector(".delete-btn").addEventListener("click", (e) => {
        const idx = parseInt(e.target.closest("li").getAttribute("data-index"));
        expenses.splice(idx, 1);
        localStorage.setItem("expenses", JSON.stringify(expenses));
        renderAll();
    })

    expenseList.appendChild(li);
}

function renderAll() {
    expenseList.innerHTML = '';
    expenses.forEach((exp, i) => addExpenseToDOM(exp, i));
    updateTotal();
}

function updateTotal(){
    const sum = expenses.reduce((sum, exp) => sum + exp.amount, 0);
    total.textContent = "Rs." + sum.toFixed(2);
}