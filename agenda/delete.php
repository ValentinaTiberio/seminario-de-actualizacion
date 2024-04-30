<?php
include_once("database.php");


$json_body = file_get_contents('php://input');
$object = json_decode($json_body);
$idContacto = $object->id;

try {
    $query = "DELETE FROM contacto WHERE id = :idContacto";
    $stmt = $connection->prepare($query);
    $stmt->bindParam(':idContacto', $idContacto);
    $stmt->execute();

    $response = array("success" => true);
    echo json_encode($response);
} catch (PDOException $e) {
    $response = array("success" => false, "message" => "Error al eliminar el contacto: " . $e->getMessage());
    echo json_encode($response);
}
?>
