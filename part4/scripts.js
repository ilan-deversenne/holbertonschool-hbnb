/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

const API_URL = 'http://localhost:5000/api/v1';

async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const passwordInput = document.getElementById('password');
  const togglePassword = document.getElementById('toggle-password');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      loginUser(email, password);
    });
  }

  if (togglePassword) {
    togglePassword.addEventListener('click', () => {
      const type = passwordInput.getAttribute('type');
      passwordInput.setAttribute('type', type === 'password' ? 'text' : 'password');
    });
  }

  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      localStorage.setItem('theme', localStorage.getItem('theme') === 'dark' ? 'light' : 'dark');
      document.body.classList.toggle('dark');

      let img = themeToggle.querySelector('img');
      if (img) {
        if (document.body.classList.contains('dark')) {
          img.src = 'images/moon.png';
        }else {
          img.src = 'images/sun.png';
        }
      }
    });
  }
  if (localStorage.getItem('theme') === 'dark') {
    img = themeToggle.querySelector('img');
    document.body.classList.add('dark');
    if (img) {
      img.src = 'images/moon.png';
    }
  }

});
