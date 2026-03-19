// app.js

// Check if local storage is supported
if (typeof(Storage) !== 'undefined') {
    // Initialize the todo list from local storage
    let todos = JSON.parse(localStorage.getItem('todos')) || [];

    // Function to display todos
    function displayTodos() {
        const todoList = document.getElementById('todo-list');
        todoList.innerHTML = '';
        todos.forEach((todo, index) => {
            const li = document.createElement('li');
            li.textContent = todo.text;
            todoList.appendChild(li);
        });
    }

    // Function to add a new todo
    function addTodo(text) {
        const todo = { text };
        todos.push(todo);
        localStorage.setItem('todos', JSON.stringify(todos));
        displayTodos();
    }

    // Event listener for adding todos
    document.getElementById('add-button').addEventListener('click', () => {
        const todoInput = document.getElementById('todo-input');
        const todoText = todoInput.value;
        if (todoText) {
            addTodo(todoText);
            todoInput.value = '';
        }
    });

    // Display existing todos on page load
    displayTodos();
} else {
    console.error('Local storage is not supported in this browser.');
}