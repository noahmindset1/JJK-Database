<?php

// Set headers to allow cross-origin requests (CORS)
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");

// Check if the file exists
if (!file_exists("jjk.db")) {
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

// Query to select all data from a table named 'your_table_name'
$query = "SELECT * FROM your_table_name";

// Execute the query
$result = $db->query($query);

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

// Close database connection
$db->close();

// Send JSON response
echo json_encode($data);
?>

