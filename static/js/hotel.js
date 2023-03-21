let locationCode = "";
let checkInDate = "";
let checkOutDate = "";
let rooms = 1;
let adultsPerRoom = 1;
let childrenPerRoom = 0;
let hotels = [];

const locationData = document.getElementById("locationData");
const hotelData = document.getElementById("hotelData");

function handleLocation() {
  const locationInput = document.getElementById("location");
  const locationData = document.getElementById("locationData");

  if (locationInput && locationData) {
    const locationInputValue = locationInput.value.trim();
    if (locationInputValue.length > 1) {
        fetch(`https://traviabooking.azurewebsites.net/api/v1/flight/select_destination/${locationInputValue}`)
        .then((response) => response.json())
        .then((data) => {
          const locationArray = data.data;
          if (locationArray) {
            const locationList = document.createElement("div");
            locationList.classList.add("location__list");
            locationArray.forEach((location) => {
              const locationItem = document.createElement("a");
              locationItem.classList.add("location__item");
              locationItem.classList.add("js-location-item");
              locationItem.innerText = `${location.name}, ${location.address.cityName}`;
              locationItem.onclick = () => {
                locationInput.value = location.name;
                locationCode = location.iataCode;
                locationData.style.display = "none";
              };
              locationList.appendChild(locationItem);
            });
            locationData.innerHTML = "";
            locationData.appendChild(locationList);
            locationData.style.display = "block";
          }
        })
        .catch((error) => console.log(error));
    } else {
      locationData.innerHTML = "";
      locationData.style.display = "none";
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const locationInput = document.getElementById("location");
  const locationData = document.getElementById("locationData");

  if (locationInput) {
    locationInput.addEventListener("input", handleLocation);
  }

  if (locationData) {
    locationData.addEventListener("mouseleave", () => {
      locationData.style.display = "none";
    });
  }
});

function getLocation(locationCode) {
  console.log(locationCode);
  locationData.style.display = "none";
}

function handleFindHotel() {
  checkInDate = document.getElementById("checkInDate").value;
  checkOutDate = document.getElementById("checkOutDate").value;
  adultsPerRoom = document.getElementById("adults").value;
  childrenPerRoom = document.getElementById("children").value;
  const hotelresults_URL = `https://traviabooking.azurewebsites.net/api/v1/hotel/search_hotels/?locationCode=${locationCode}&checkInDate=${checkInDate}&checkOutDate=${checkOutDate}`;
  window.location.href = hotelresults_URL;
}

function handleFindHotelstopped() {
  checkInDate = document.getElementById("checkInDate").value;
  checkOutDate = document.getElementById("checkOutDate").value;
  let hotelEl = "";
  const hotelData = document.getElementById("hotelData");

  fetch(`https://traviabooking.azurewebsites.net/api/v1/flight/search_hotels/?locationCode=${locationCode}&checkInDate=${checkInDate}&checkOutDate=${checkOutDate}&rooms=${rooms}&adultsPerRoom=${adultsPerRoom}&childrenPerRoom=${childrenPerRoom}`)
    .then((response) => response.json())
    .then((data) => {
      hotels = data.data;
      console.log(hotels);
      
      if (hotels) {
        hotels.map((hotel) => {
          // Construct the URL of the hotel image based on the hotel ID
          const imageUrl = `https://s1.travix.com/hotels/${hotel.hotelId}.jpg`;
          hotelEl +=
            `
            <div class="hotel">
              <div class="hotel__wrap">
                <div class="hotel__item">
                  <div class="hotel__image">
                    <img src="${imageUrl}" alt="${hotel.name}" />
                  </div>
                  <div class="hotel__details">
                    <div class="hotel__box">
                      <div class="hotel__name">${hotel.name}</div>
                      <div class="hotel__location">${hotel.address.cityName}, ${hotel.address.countryCode}</div>
                      <div class="hotel__price">${hotel.price.total} ${hotel.price.currency}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            `;
            });
            hotelData.innerHTML = hotelEl;
        } else {
          hotelData.innerHTML = "No hotels found";
        }
      })
      .catch((error) => console.log(error));
}

document.addEventListener("DOMContentLoaded", () => {
const findHotelBtn = document.getElementById("findHotelBtn");

if (findHotelBtn) {
findHotelBtn.addEventListener("click", handleFindHotel);
}
});