/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

const API_URL = 'http://localhost:5000/api/v1'

async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  })

  if (response.ok) {
    const data = await response.json()
    document.cookie = `token=${data.access_token}; path=/`
    window.location.href = 'index.html'
  } else {
    alert('Login failed: ' + response.statusText)
  }
}

function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    // Your code here

  let params = new URLSearchParams(document.location.search)
  return params.get('id')
}

function checkAuthentication() {
    const token = getCookie('token')
    const loginLink = document.getElementById('login-link')

    if (!token) {
        loginLink.style.display = 'block'
    } else {
        loginLink.style.display = 'none'

        if (document.location.pathname.endsWith('/index.html')) {
          fetchPlaces(token)
        } else if (document.location.pathname.endsWith('/place.html')) {
          fetchPlaceDetails(token, getPlaceIdFromURL())
        }
    }
}

function getCookie(name) {
    // Function to get a cookie value by its name
    // Your code here

    const regex = new RegExp(`(^| )${name}=([^;]+)`)
    const match = document.cookie.match(regex)
    if (match) {
      return match[2]
    }
}

async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function

  const response = await fetch(`${API_URL}/places/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })

  if (response.ok) {
    const data = await response.json()
    displayPlaces(data)
  }
}

function displayPlaces(places) {
  // Clear the current content of the places list
  // Iterate over the places data
  // For each place, create a div element and set its content
  // Append the created element to the places list

  const placesList = document.getElementById('places-list')

  places.forEach(place => {
    let div = document.createElement('div')
    let title = document.createElement('h1')
    let price = document.createElement('p')
    let details = document.createElement('button')

    div.classList.add('place-card')

    title.innerText = place['title']
    price.innerText = `${place['price']}$ /Night`

    details.innerText = 'View Details'
    details.classList.add('details-button')
    details.addEventListener('click', () => {
      window.location.href = `place.html?id=${place['id']}`
    })

    div.appendChild(title)
    div.appendChild(price)
    div.appendChild(details)

    placesList.appendChild(div)

  })

}

async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function

  const response = await fetch(`${API_URL}/places/${placeId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })

  if (response.ok) {
    const data = await response.json()
    displayPlaceDetails(data)
  }
}

function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section

  const placeDetails = document.getElementById('place-details')

  const title = document.createElement('h1')
  const description = document.createElement('p')
  const price = document.createElement('h2')

  title.innerText = place['title']
  description.innerText = place['description']
  price.innerText = `${place['price']}$ /Night`

  placeDetails.appendChild(title)
  placeDetails.appendChild(description)
  placeDetails.appendChild(price)
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form')
  const passwordInput = document.getElementById('password')
  const togglePassword = document.getElementById('toggle-password')

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault()
      const email = document.getElementById('email').value
      const password = document.getElementById('password').value

      loginUser(email, password)
    });
  }

  if (togglePassword) {
    togglePassword.addEventListener('click', () => {
      const type = passwordInput.getAttribute('type')
      passwordInput.setAttribute('type', type === 'password' ? 'text' : 'password')
    })
  }

  const themeToggle = document.getElementById('theme-toggle')
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      localStorage.setItem('theme', localStorage.getItem('theme') === 'dark' ? 'light' : 'dark')
      document.body.classList.toggle('dark')

      let img = themeToggle.querySelector('img')
      if (img) {
        if (document.body.classList.contains('dark')) {
          img.src = 'images/moon.png'
        }else {
          img.src = 'images/sun.png'
        }
      }
    });
  }
  if (localStorage.getItem('theme') === 'dark') {
    img = themeToggle.querySelector('img')
    document.body.classList.add('dark')
    if (img) {
      img.src = 'images/moon.png'
    }
  }

  if (!document.location.pathname.endsWith('/login.html')) {
    checkAuthentication()
  }

})
