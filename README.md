# City API Visualization

This project provides a web interface for visualizing city information from an API. Users can search for cities based on various filters and view the results in a tabular format.


![demo](demo.png)


## Features

- Search cities by:
  - City ID
  - State Name
  - City Name
  - Modified Date
- Pagination for navigating through results
- Responsive design using Bootstrap

## Technologies Used

- HTML
- CSS
- JavaScript (jQuery)
- Bootstrap


## API Endpoints

### 1. Get All Cities
- **Endpoint:** `/cities`
- **Method:** `GET`
- **Description:** Retrieves a paginated list of all cities.
- **Query Parameters:**
  - `page`: The page number (default: 1).
  - `limit`: Number of results per page (default: 100).
  - Additional optional filters: `city_id`, `state_name`, `city_name`, `modified_after`.

### 2. Get City by ID
- **Endpoint:** `/city/<city_id>`
- **Method:** `GET`
- **Description:** Retrieves detailed information about a specific city using its ID.

### 3. Get Cities Modified After a Specific Date
- **Endpoint:** `/modified_after`
- **Method:** `GET`
- **Description:** Retrieves a paginated list of cities modified after a specified date.
- **Query Parameters:**
  - `date`: The date to filter cities.
  - `page`: The page number (default: 1).
  - `limit`: Number of results per page (default: 100).

## Error Handling
- **400 Bad Request:** Invalid parameters.
- **404 Not Found:** City not found.
- **500 Internal Server Error:** Database or server issues.

## Dependencies
- Python 3.x
- Flask
- psycopg2 (PostgreSQL adapter)

## Setup Instructions
1. Clone the repository.
2. Navigate to the project directory.
3. Install required packages.
4. Configure the database connection.
5. Run the application.

