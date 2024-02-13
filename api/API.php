<?php

// Set headers to allow cross-origin requests (CORS)
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

// Check if the file exists
if (!file_exists("db.db")) {
    http_response_code(404);
    echo json_encode(array("message" => "Database file not found."));
    exit;
}

// Connect to SQLite database
try {
    $db = new SQLite3("jjk.db");
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(array("message" => "Failed to connect to the database."));
    exit;
}

// Parameters for pagination
$page = isset($_GET['page']) && is_numeric($_GET['page']) ? $_GET['page'] : 1;
$recordsPerPage = 10;
$offset = ($page - 1) * $recordsPerPage;

// Query to select data from a table named 'your_table_name' with pagination
$query = "SELECT * FROM your_table_name LIMIT :limit OFFSET :offset";
$stmt = $db->prepare($query);
$stmt->bindValue(':limit', $recordsPerPage, SQLITE3_INTEGER);
$stmt->bindValue(':offset', $offset, SQLITE3_INTEGER);

// Execute the query
$result = $stmt->execute();

// Check if there are results
if (!$result) {
    http_response_code(404);
    echo json_encode(array("message" => "No data found."));
    exit;
}

// Fetch data and encode it as JSON
$data = array();
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $data[] = $row;
}

// Count total records
$totalQuery = "SELECT COUNT(*) as total FROM your_table_name";
$totalResult = $db->querySingle($totalQuery);
$totalPages = ceil($totalResult / $recordsPerPage);

// Close database connection
$db->close();

// Response data
$response = array(
    "data" => $data,
    "pagination" => array(
        "page" => $page,
        "totalPages" => $totalPages,
        "recordsPerPage" => $recordsPerPage,
        "totalRecords" => $totalResult
    )
);

// Send JSON response
echo json_encode($response);
?>
