<?php
$server = "localhost";
$user = "root";
$pass = "";
$db = "agenda";

$conexion = new mysqli($server, $user, $pass, $db );


if($conexion->connect_errno){
    die("Error en la conexion" . $conexion->connect_errno);   
}
?>