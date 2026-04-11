/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

const API_URL = 'http://localhost:5000/api/v1'

/*
  Login user

  email: Account email
  password: Account password
  */
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

/*
  Get place id from url (id)
  */
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
          const placeId = getPlaceIdFromURL()

          fetchPlaceDetails(token, placeId)
          fetchPlaceReviews(token, placeId)
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

/*
  Fetch place details

  token: Authorization token
  placeId: Id of place to fetch
  */
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

/*
  Display fetched place details

  place: Array that contains fetched place data
  */
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

/*
  Fetch reviews

  token: Authorization token
  placeId: Id of place to fetch
  */
async function fetchPlaceReviews(token, placeId) {
  const response = await fetch(`${API_URL}/reviews/${placeId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  })

  if (response.ok) {
    const data = await response.json()
    displayPlaceReviews(data)
  }
}

/*
  Display fetched reviews

  reviews: Array that contains reviews
  */
function displayPlaceReviews(reviews) {
  console.log(reviews)

  const reviewsSection = document.getElementById('reviews')

  reviews.forEach(review => {
    let div = document.createElement('div')
    let author = document.createElement('h1')
    let text = document.createElement('p')

    div.classList.add('review-details')

    author.innerText = ':3'
    text.innerText = review['text']

    let starContainer = document.createElement('div')
    starContainer.classList.add('star-container')

    for(let i = 0; i < 5; i++) {
      let star = document.createElement('img')
      let filename = i < review['rating'] ? 'star_bg' : 'star'
      if (localStorage.getItem('theme') === 'dark') {
        filename = `${filename}_white`
      }
      star.src = `images/${filename}.png`
      star.width = '12'

      starContainer.appendChild(star)
    }

    div.appendChild(author)
    div.appendChild(text)
    div.appendChild(starContainer)

    reviewsSection.appendChild(div)
  })
}

function setStars(stars) {
  for(let i = 1; i < 6; i++) {
    let star = document.getElementById(`star-${i}`)
    star.src = 'images/star.png'
    if (localStorage.getItem('theme') === 'dark') {
      star.src = 'images/star_white.png'
    }
  }

  for(let i = 1; i <= stars; i++) {
    let star = document.getElementById(`star-${i}`)
    star.src = 'images/star_bg.png'
    if (localStorage.getItem('theme') === 'dark') {
      star.src = 'images/star_bg_white.png'
    }
  }

  document.getElementById('rating').value = stars
}

async function add_review(token, text, rating, placeId) {
  const response = await fetch(`${API_URL}/reviews/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      'text': text,
      'rating': parseInt(rating),
      'place_id': placeId
    })
  })

  if (!response.ok) {
    alert(`Failed to add review`)
  }
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
    })
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

      const logo = document.querySelector('.logo')
      if (logo) {
        if (document.body.classList.contains('dark')) {
          logo.src = 'images/logo_white.png'
        } else {
          logo.src = 'images/logo.png'
        }
      }

      if (document.location.pathname.endsWith('/place.html')) {
        setStars(document.getElementById('rating'))
      }
    });
  }
  if (localStorage.getItem('theme') === 'dark') {
    img = themeToggle.querySelector('img')
    document.body.classList.add('dark')
    if (img) {
      img.src = 'images/moon.png'
    }

    const logo = document.querySelector('.logo')
    if (logo) {
      logo.src = 'images/logo_white.png'
    }
  }

  if (!document.location.pathname.endsWith('/login.html')) {
    checkAuthentication()
  }

  if (document.location.pathname.endsWith('/place.html')) {
    if (localStorage.getItem('theme') === 'dark') {
      document.getElementById(`star-1`).src = 'images/star_bg_white.png'
      for(let i = 2; i < 6; i++) {
        let star = document.getElementById(`star-${i}`)
        star.src = 'images/star_white.png'
      }
    }

    for(let i = 1; i < 6; i++) {
      let star = document.getElementById(`star-${i}`)

      star.addEventListener('click', () => {
        setStars(i)
      })
    }

    const reviewForm = document.getElementById('review-form')
    if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault()

        const token = getCookie('token')
        const text = document.getElementById('review-text').value
        const rating = document.getElementById('rating').value
        const placeId = getPlaceIdFromURL()

        add_review(token, text, rating, placeId)
      })
    }
  }

})
