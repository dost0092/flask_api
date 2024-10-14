// let currentPage = 1;
// let totalPages = 0;
// const limit = 10;

// function fetchCities() {
//   const cityId = $("#cityId").val();
//   const stateName = $("#stateName").val();
//   const cityName = $("#cityName").val();
//   const modifiedDate = $("#modifiedDate").val();

//   let url = `/cities?page=${currentPage}&limit=${limit}`;
//   if (cityId) url += `&city_id=${cityId}`;
//   if (stateName) url += `&state_name=${stateName}`;
//   if (cityName) url += `&city_name=${cityName}`;
//   if (modifiedDate) url += `&modified_after=${modifiedDate}`;

//   console.log(`Fetching data from: ${url}`);
//   $.getJSON(url, function (data) {
//     if (data.error) {
//       $("#resultContainer").html(
//         `<div class="alert alert-danger">${data.error}</div>`
//       );
//       return;
//     }

//     totalPages = data.total_pages;
//     displayResults(data.cities);
//     setupPagination();
//   });
// }

// function displayResults(cities) {
//   const resultContainer = $("#resultContainer");
//   resultContainer.empty();
//   if (cities.length === 0) {
//     resultContainer.append(
//       '<div class="alert alert-warning">No cities found.</div>'
//     );
//     return;
//   }

//   const table = `<table class="table table-striped">
//         <thead>
//             <tr>
//                 <th>ID</th>
//                 <th>Name</th>
//                 <th>County</th>
//                 <th>State</th>
//                 <th>Date Created</th>
//                 <th>Date Modified</th>
//             </tr>
//         </thead>
//         <tbody>
//             ${cities
//               .map(
//                 (city) => `
//                 <tr>
//                     <td>${city.id}</td>
//                     <td>${city.name}</td>
//                     <td>${city.county}</td>
//                     <td>${city.state}</td>
//                     <td>${new Date(city.date_created).toLocaleDateString()}</td>
//                     <td>${new Date(
//                       city.date_modified
//                     ).toLocaleDateString()}</td>
//                 </tr>
//                 `
//               )
//               .join("")}
//         </tbody>
//     </table>`;
//   resultContainer.append(table);
// }

// function setupPagination() {
//   const paginationControls = $("#paginationControls");
//   paginationControls.empty();

//   const maxPagesToShow = 10;
//   const halfMax = Math.floor(maxPagesToShow / 2);
//   let startPage = Math.max(currentPage - halfMax, 1);
//   let endPage = Math.min(startPage + maxPagesToShow - 1, totalPages);

//   if (endPage - startPage < maxPagesToShow - 1) {
//     startPage = Math.max(endPage - maxPagesToShow + 1, 1);
//   }

//   if (currentPage > 1) {
//     paginationControls.append(`
//         <li class="page-item">
//             <a class="page-link" href="#" data-page="${
//               currentPage - 1
//             }">Previous</a>
//         </li>
//     `);
//   }

//   for (let i = startPage; i <= endPage; i++) {
//     const pageItem = `
//         <li class="page-item ${currentPage === i ? "active" : ""}">
//             <a class="page-link" href="#" data-page="${i}">${i}</a>
//         </li>`;
//     paginationControls.append(pageItem);
//   }

//   if (currentPage < totalPages) {
//     paginationControls.append(`
//         <li class="page-item">
//             <a class="page-link" href="#" data-page="${
//               currentPage + 1
//             }">Next</a>
//         </li>
//     `);
//   }

//   paginationControls.append(`
//     <li class="page-item disabled">
//         <span class="page-link">Total Pages: ${totalPages}</span>
//     </li>
// `);

//   $(".page-link").click(function (event) {
//     event.preventDefault();
//     currentPage = $(this).data("page");
//     fetchCities();
//   });
// }

// $("#searchForm").submit(function (event) {
//   event.preventDefault();
//   currentPage = 1;
//   fetchCities();
// });














let currentPage = 1;
let totalPages = 0;
const limit = 10;

function fetchCities() {
  const cityId = $("#cityId").val();
  const stateName = $("#stateName").val();
  const cityName = $("#cityName").val();
  const modifiedDate = $("#modifiedDate").val();

  let url = `/cities?page=${currentPage}&limit=${limit}`;
  if (cityId) url += `&city_id=${cityId}`;
  if (stateName) url += `&state_name=${stateName}`;
  if (cityName) url += `&city_name=${cityName}`;
  if (modifiedDate) url += `&modified_after=${modifiedDate}`;

  $.getJSON(url, function (data) {
    if (data.error) {
      $("#resultContainer").html(
        `<div class="alert alert-danger">${data.error}</div>`
      );
      return;
    }

    totalPages = data.total_pages;
    displayResults(data.cities);
    setupPagination();
  });
}

function displayResults(cities) {
  const resultContainer = $("#resultContainer");
  resultContainer.empty();
  if (cities.length === 0) {
    resultContainer.append(
      '<div class="alert alert-warning">No cities found.</div>'
    );
    return;
  }

  const table = `<table class="table table-bordered table-striped"> <!-- Added table-bordered class -->
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>County</th>
                        <th>State</th>
                        <th>Date Created</th>
                        <th>Date Modified</th>
                    </tr>
                </thead>
                <tbody>
                    ${cities
                      .map(
                        (city) => `
                    <tr>
                        <td>${city.id}</td>
                        <td>${city.name}</td>
                        <td>${city.county}</td>
                        <td>${city.state}</td>
                        <td>${new Date(
                          city.date_created
                        ).toLocaleDateString()}</td>
                        <td>${new Date(
                          city.date_modified
                        ).toLocaleDateString()}</td>
                    </tr>
                    `
                      )
                      .join("")}
                </tbody>
            </table>`;
  resultContainer.append(table);
}

function setupPagination() {
  const paginationControls = $("#paginationControls");
  paginationControls.empty();

  const maxPagesToShow = 10;
  const halfMax = Math.floor(maxPagesToShow / 2);
  let startPage = Math.max(currentPage - halfMax, 1);
  let endPage = Math.min(startPage + maxPagesToShow - 1, totalPages);

  if (endPage - startPage < maxPagesToShow - 1) {
    startPage = Math.max(endPage - maxPagesToShow + 1, 1);
  }

  // previous button
  if (currentPage > 1) {
    paginationControls.append(`
            <li class="page-item">
                <a class="page-link" href="#" data-page="${
                  currentPage - 1
                }">Previous</a>
            </li>
        `);
  }

  // page buttons
  for (let i = startPage; i <= endPage; i++) {
    const pageItem = `
            <li class="page-item ${currentPage === i ? "active" : ""}">
                <a class="page-link" href="#" data-page="${i}">${i}</a>
            </li>`;
    paginationControls.append(pageItem);
  }

  // next button
  if (currentPage < totalPages) {
    paginationControls.append(`
            <li class="page-item">
                <a class="page-link" href="#" data-page="${
                  currentPage + 1
                }">Next</a>
            </li>
        `);
  }

  //total pages
  paginationControls.append(`
        <li class="page-item disabled">
            <span class="page-link">Total Pages: ${totalPages}</span>
        </li>
    `);

  // event handler
  $(".page-link").click(function (event) {
    event.preventDefault();
    currentPage = $(this).data("page");
    fetchCities();
  });
}

$("#searchForm").submit(function (event) {
  event.preventDefault();
  currentPage = 1;
  fetchCities();
});
