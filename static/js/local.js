let originCode = "";
let destinationCode = "";
let departureDate = "";
let adults = 1;
let children = 0;
let fromLocationArray = [];
let toLocationArray = [];
let flights = [];

const fromLocationData = document.getElementById("fromLocationData");
const toLocationData = document.getElementById("toLocationData");
const flightData = document.getElementById("flightData");

function handleFromLocation() {
  const fromInput = document.getElementById("from");
  const fromLocationData = document.getElementById("fromLocationData");

  if (fromInput && fromLocationData) {
    const fromInputValue = fromInput.value.trim();
    if (fromInputValue.length > 1) {
      fetch(`https://traviabooking.azurewebsites.net/api/v1/flight/select_destination/${fromInputValue}`)
        .then((response) => response.json())
        .then((data) => {
          const fromLocationArray = data.data;
          if (fromLocationArray) {
            const locationList = document.createElement("div");
            locationList.classList.add("location__list");
            fromLocationArray.forEach((location) => {
              const locationItem = document.createElement("a");
              locationItem.classList.add("location__item");
              locationItem.classList.add("js-location-item");
              locationItem.innerText = `${location.name}, ${location.subType}: ${location.address.cityName}`;
              locationItem.onclick = () => {
                fromInput.value = location.name;
                originCode = location.iataCode;
                fromLocationData.style.display = "none";
              };
              locationList.appendChild(locationItem);
            });
            fromLocationData.innerHTML = "";
            fromLocationData.appendChild(locationList);
            fromLocationData.style.display = "block";
          }
        })
        .catch((error) => console.log(error));
    } else {
      fromLocationData.innerHTML = "";
      fromLocationData.style.display = "none";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const fromInput = document.getElementById("from");
  const fromLocationData = document.getElementById("fromLocationData");

  if (fromInput) {
    fromInput.addEventListener("input", handleFromLocation);
  }

  if (fromLocationData) {
    fromLocationData.addEventListener("mouseleave", () => {
      fromLocationData.style.display = "none";
    });
  }
});


function getFromLocation(originCode) {
  console.log(originCode);
  fromLocationData.style.display = "none";
}

function handleToLocation() {
  const toInput = document.getElementById("to");
  const toLocationData = document.getElementById("toLocationData");

  if (toInput && toLocationData) {
    const toInputValue = toInput.value.trim();
    if (toInputValue.length > 1) {
      fetch(`https://traviabooking.azurewebsites.net/api/v1/flight/select_destination/${toInputValue}`)
        .then((response) => response.json())
        .then((data) => {
          const toLocationArray = data.data;
          if (toLocationArray) {
            const locationList = document.createElement("div");
            locationList.classList.add("location__list");
            toLocationArray.forEach((location) => {
              const locationItem = document.createElement("a");
              locationItem.classList.add("location__item");
              locationItem.classList.add("js-location-item");
              locationItem.innerText = `${location.name}, ${location.subType}: ${location.address.cityName}`;
              locationItem.onclick = () => {
                toInput.value = location.name;
                destinationCode = location.iataCode;
                toLocationData.style.display = "none";
              };
              locationList.appendChild(locationItem);
            });
            toLocationData.innerHTML = "";
            toLocationData.appendChild(locationList);
            toLocationData.style.display = "block";
          }
        })
        .catch((error) => console.log(error));
    } else {
      toLocationData.innerHTML = "";
      toLocationData.style.display = "none";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const toInput = document.getElementById("to");
  const toLocationData = document.getElementById("toLocationData");

  if (toInput) {
    toInput.addEventListener("input", handleToLocation);
  }

  if (toLocationData) {
    toLocationData.addEventListener("mouseleave", () => {
      toLocationData.style.display = "none";
    });
  }
});

function getToLocation(destinationCode) {
  console.log(destinationCode);
  toLocationData.style.display = "none";
}

function handleFindFlight() {
  departureDate = document.getElementById("date").value;
  let flightEl = "";
  const flightData = document.getElementById("flightData");

  fetch(`https://traviabooking.azurewebsites.net/api/v1/flight/search_offers/?originCode=${originCode}&destinationCode=${destinationCode}&departureDate=${departureDate}`)
    .then((response) => response.json())
    .then((data) => {
      flights = data.data;

      if (flights) {
        flights.map((flight) => {
          // Extract the validating airline code from the flight object
          const airlineCode = flight.validatingAirlineCodes[0];
          // Construct the URL of the airline logo based on the airline code
          const logoUrl = `https://s1.apideeplink.com/images/airlines/${airlineCode}.png`;
          // Convert the flight object to a string
          const dataflight = JSON.stringify({flight});

          flightEl +=
            `
            <div class="flight">
              <form method="post">
                {% csrf_token %}
              <div class="flight__wrap">
                <div class="flight__item">
                  <div class="flight__logo">
                    <img src="${logoUrl}" alt="${airlineCode}" />
                  </div>
                  <div class="flight__details">
                    <div class="flight__box">
                      <div class="flight__title">${originCode}</div>
                      <div class="flight__time">${flight.itineraries[0].segments[0].departure.at.split("T")[1].substring(0, 5)}</div>
                    </div>
                    <div class="flight__note">${flight.itineraries[0].segments.length} stops</div>
          `;

          for (let i = 0; i < flight.itineraries[0].segments.length; i++) {
            flightEl +=
              `
              <div class="flight__box">
                <div class="flight__title">${flight.itineraries[0].segments[i].arrival.iataCode}</div>
                <div class="flight__time">${flight.itineraries[0].segments[i].arrival.at.split("T")[1].substring(0, 5)}</div>
              </div>
              `;
          }

          flightEl +=
            `
                  </div>
                </div>
              </div>
              <div class="flight__control">
                <div class="flight__info">
                  <svg class="icon icon-tick">
                    <use xlink:href="#icon-tick"></use>
                  </svg>
                  ${flight.price.currency}
                </div>
                <input type="hidden" name="dataflight" id="dataflight" value="{{ dataflight }}">
                <!-- button type=submit class="button-stroke flight__button" href = "{% url 'flight_checkout'%}"" -->
                <!-- input type="hidden" name="dataflight" value="{{ dataflight }}" -->
                <button type="submit" class="button-stroke flight__button" onclick="setDataFlight(event, '${dataflight}') formaction="{% url 'flight_checkout' %}" ">
                  <span class="flight__price">${flight.price.currency} ${flight.price.total}</span>
                  <span class="flight__more">
                    <span>View deal</span>
                    <svg class="icon icon-arrow-next">
                      <use xlink:href="#icon-arrow-next"></use>
                    </svg>
                  </span>
              </button>
              </div>
              </form>
            </div>
            `;
          const dataflightInput = document.getElementById("dataflight");
          dataflightInput.value = dataflight;  
        });
        flightData.innerHTML = flightEl;

      } else {
        alert("No flight Data found");
      }
    })
    .catch((error) => console.log(error));
}



function BookFlight(flight) {
  const first = document.getElementById("first").value;
  const last = document.getElementById("last").value;

  fetch("https://traviabooking.azurewebsites.net/api/v1/flight/price_offers", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      flight,
    }),
  })
    .then((response) => response.json())
    .then((dataObject) => {
      console.log("Success:", dataObject);

      fetch("https://traviabooking.azurewebsites.net/api/v1/flight/book_flight/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          flight,
          traveler: { first, last },
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Success:", data);
          flights = [];
        })
        .catch((error) => {
          alert(error);
        });
    })
    .catch((error) => {
      console.error("Error:", error);
      alert(error);
    });
}

function setDataFlight(event, dataflight) {
  const dataflightInput = event.target.form.querySelector("#dataflight");
  dataflightInput.value = dataflight;
}
//const adults = document.getElementById('adultsCount').textContent;
//const children = document.getElementById('childrenCount').textContent;