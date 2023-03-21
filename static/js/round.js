let originCode = ""; let checkoutHost = window.location.host;
let destinationCode = "";
let shortOrigin = "";
let shortDestination = "";
let longOrigin = "";
let longDestination = "";
let departureDate = "";
let returnDate = "";
let returnTime = "";
let arrivalDate = "";
let departureTime = "";
let arrivalTime = "";
let flightDuration = "";
let flightNumber = "";
let returnflightNumber = "";
let flightId = "";
let returnflightId = "";
let depTerminal = "";
let arrTerminal = "";
let returnarrivalDate = "";
let returnarrivalTime = "";
let returnflightDuration = "";
let flightTotal = "";
let airlineCode = "";
let returnairlineCode = "";
let logoUrl = "";
let returnlogoUrl = "";
let bookableSeats = "";
let lastTicketing = "";
let checkout_url = ``;
let adults = 1;
let children = 0;
let infants = 0;
let fromLocationArray = [];
let toLocationArray = [];
let flights = [];
let flightCosts = [];

const fromLocationData = document.getElementById("fromLocationData");
const toLocationData = document.getElementById("toLocationData");
const flightData = document.getElementById("flightData");

function handleFromLocation() {
  const fromInput = document.getElementById("from");
  const fromLocationData = document.getElementById("fromLocationData");

  if (fromInput && fromLocationData) {
    const fromInputValue = fromInput.value.trim();
    if (fromInputValue.length > 1) {
      fetch(`https://${checkoutHost}/api/v1/flight/select_destination/${fromInputValue}`)
        .then((response) => response.json())
        .then((data) => {
          fromLocationArray = data.data;
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
      fetch(`https://${checkoutHost}/api/v1/flight/select_destination/${toInputValue}`)
        .then((response) => response.json())
        .then((data) => {
          toLocationArray = data.data;
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
  adults = document.getElementById("adults").value;
  children = document.getElementById("children").value;
  infants = document.getElementById("infants").value;
  returnDate = document.getElementById("returndate").value;
  let flightEl = "";
  const flightData = document.getElementById("flightData");
   

  fetch(`https://${checkoutHost}/api/v1/flight/search_roundtrip/?originCode=${originCode}&destinationCode=${destinationCode}&departureDate=${departureDate}&returnDate=${returnDate}&adults=${adults}&children=${children}&infants=${infants}`)
    .then((response) => response.json())
    .then((data) => {
      flights = data.data;

      if (flights) {
        flights.map((flight) => {
          // Extract the validating airline code from the flight object
          airlineCode = flight.validatingAirlineCodes[0];
          returnairlineCode = flight.validatingAirlineCodes[1];
          
          // Construct the URL of the airline logo based on the airline code
          logoUrl = `https://s1.apideeplink.com/images/airlines/${airlineCode}.png`;
          returnlogoUrl = `https://s1.apideeplink.com/images/airlines/${returnairlineCode}.png`;
          // Define constants to pass to checkout view          
          flightDuration = flight.itineraries[0].duration;
          flightTotal = flight.price.total;
          lastTicketing = flight.lastTicketingDate;
          bookableSeats = flight.numberOfBookableSeats;
          departureDate = flight.itineraries[0].segments[0].departure.at.split("T")[0];
          departureTime = flight.itineraries[0].segments[0].departure.at.split("T")[1].substring(0, 5);
          arrivalTime = flight.itineraries[0].segments[0].arrival.at.split("T")[1].substring(0, 5);
          arrivalDate = flight.itineraries[0].segments[0].arrival.at.split("T")[0];
          returnDate = flight.itineraries[1].segments[0].departure.at.split("T")[0];
          returnTime = flight.itineraries[1].segments[0].departure.at.split("T")[1].substring(0, 5);
          returnarrivalTime = flight.itineraries[1].segments[0].arrival.at.split("T")[1].substring(0, 5);
          returnarrivalDate = flight.itineraries[1].segments[0].arrival.at.split("T")[0];
          flightId = flight.id;
          flightNumber = flight.itineraries[0].segments[0].number;
          returnflightNumber = flight.itineraries[1].segments[0].number;
          flightDuration = flight.itineraries[0].duration;
          returnflightDuration = flight.itineraries[1].duration;

          flightEl +=
            `
            <div class="flight">
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
              <div class="flight__box">
                <div class="flight__title">${destinationCode}</div>
                  <div class="flight__time">${flight.itineraries[0].segments[0].arrival.at.split("T")[1].substring(0, 5)}</div>                
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
              <div class="flight__item">
              <div class="flight__logo">
                <img src="${returnlogoUrl}" alt="${returnairlineCode}" />
              </div>
              <div class="flight__details">
                <div class="flight__box">
                <div class="flight__title">${destinationCode}</div>
                <div class="flight__time">${flight.itineraries[1].segments[0].departure.at.split("T")[1].substring(0, 5)}</div>
              </div>
              <div class="flight__note">${flight.itineraries[1].segments.length} stops</div>
              <div class="flight__box">
                <div class="flight__title">${originCode}</div>
                  <div class="flight__time">${flight.itineraries[1].segments[0].arrival.at.split("T")[1].substring(0, 5)}</div>                
            `;

          for (let i = 1; i < flight.itineraries[1].segments.length; i++) {
            flightEl +=
              `
              <div class="flight__box">
                <div class="flight__title">${flight.itineraries[1].segments[i].arrival.iataCode}</div>
                <div class="flight__time">${flight.itineraries[1].segments[i].arrival.at.split("T")[1].substring(0, 5)}</div>
              </div>
              `;
          }
          checkout_url = `https://${checkoutHost}/api/v1/flight/flight_checkout/?originCode=${originCode}&destinationCode=${destinationCode}&shortOrigin=${shortOrigin}&shortDestination=${shortDestination}&longOrigin=${longOrigin}&longDestination=${longDestination}&departureDate=${departureDate}&arrivalDate=${arrivalDate}&departureTime=${departureTime}&arrivalTime=${arrivalTime}&flightDuration=${flightDuration}&airlineCode=${airlineCode}&logoUrl=${logoUrl}&bookableSeats=${bookableSeats}&lastTicketing=${lastTicketing}&adults=${adults}&children=${children}&infants=${infants}&flightTotal=${flightTotal}`;
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
                    <button class="button-stroke flight__button" onclick="setDataFlight()">
                          <span class="flight__price"> ${flight.price.currency} ${flight.price.total}</span>
                          <span class="flight__more">
                            <span>View deal</span>
                            <svg class="icon icon-arrow-next">
                              <use xlink:href="#icon-arrow-next"></use>
                            </svg>
                          </span>
                        </button>
                      </div>
                    </div>
              `;
            });
            flightData.innerHTML = flightEl;
          }
             else {
            flightData.innerHTML = "<p>No flights found.</p>";
          }
        })
        .catch((error) => console.error(error));
}

function setDataFlight() {
  window.location.href = checkout_url;
}
//const adults = document.getElementById('adultsCount').textContent;
