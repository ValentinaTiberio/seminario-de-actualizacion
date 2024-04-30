<?php
include_once("database.php");

try {
    $query = "SELECT * FROM contacto";
    $stmt = $connection->prepare($query);
    $stmt->execute();
    $contacts = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $response = array("success" => true, "contacts" => $contacts);
    echo json_encode($response);
} catch (PDOException $e) {
    $response = array("success" => false, "message" => "Error al obtener los contactos: " . $e->getMessage());
    echo json_encode($response);
}
?>
