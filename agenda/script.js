function getFormValues() {
    let createFormData = {
        name: null,
        lastname: null,
        phone: null
    };
    
    createFormData.name = document.getElementById('nameInput').value;
    createFormData.lastname = document.getElementById('lastnameInput').value;
    createFormData.phone = document.getElementById('phoneInput').value;
    
    return createFormData;
}

function onCreateUserButtonClick() {
    fetch('./create.php', { method: 'post', body: JSON.stringify(getFormValues()) })
        .then(response => response.json())
        .then(response => { alert(response.description); })
        .catch(error => console.error('Error al crear el usuario:', error));
}

const contactsTableBody = document.getElementById('contactsTableBody');

function mostrarContactos(contactos) {
    contactsTableBody.innerHTML = '';

    contactos.forEach(contacto => {
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${contacto.name}</td>
            <td>${contacto.lastname}</td>
            <td>${contacto.phone}</td>
            <td><button onclick="eliminarContacto(${contacto.id})">Eliminar</button></td>
        `;
        contactsTableBody.appendChild(fila);
    });
}

function obtenerContactos() {
    fetch('./obtener_contactos.php')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarContactos(data.contacts);
            } else {
                console.error('Error al obtener los contactos:', data.message);
            }
        })
        .catch(error => console.error('Error al obtener los contactos:', error));
}

obtenerContactos();

function eliminarContacto(idContacto) {
    if (confirm('¿Estás seguro de que deseas eliminar este contacto?')) {
        fetch('./eliminar_contacto.php', {
            method: 'post',
            body: JSON.stringify({ id: idContacto })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`contacto-${idContacto}`).remove();
                alert('Contacto eliminado exitosamente.');
            } else {
                alert('Error al eliminar el contacto: ' + data.message);
            }
        })
        .catch(error => console.error('Error al eliminar el contacto:', error));
    }
}

document.getElementById('createUserButton').addEventListener('click', onCreateUserButtonClick);
