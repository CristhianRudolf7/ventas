# Librerias
Librerias a instalar (pip install):
- os
- django
- pathlib
- uuid
- rest_framework
- datetime
- django-cors-headers

# Conexion con el frontend
En el archivo crud/settings.py existe una lista llamada CORS_ALLOWED_ORIGINS, ahí se debe modificar la url del frontend para que django le otorgue permisos para enviar y recibir datos.

# URLs
Las urls se encuentran en ventas/urls.py

# Ejemplos para obtener ratos
1. Obtener todos los trabajadores (GET)
```js
import React, { useState, useEffect } from 'react';

function ListaTrabajadores() {
  const [trabajadores, setTrabajadores] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:800/api/trabajadores/')
      .then(response => response.json())
      .then(data => setTrabajadores(data));
  }, []);

  return (
    <ul>
      {trabajadores.map(trabajador => (
        <li key={trabajador.trabajador_id}>
          {trabajador.nombre}
        </li>
      ))}
    </ul>
  );
}
```

2. Crear un trabajador (POST)
```js
function CrearTrabajador() {
  const [nombre, setNombre] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://127.0.0.1:800/api/trabajadores/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre: nombre }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Trabajador creado:', data);
        setNombre('');
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        placeholder="Nombre del trabajador"
      />
      <button type="submit">Crear</button>
    </form>
  );
}
```

3. Actualizar un trabajador (PUT)
```js
function ActualizarTrabajador({ trabajadorId }) {
  const [nuevoNombre, setNuevoNombre] = useState('');

  const handleUpdate = () => {
    fetch(`http://127.0.0.1:800/api/trabajadores/${trabajadorId}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre: nuevoNombre }),
    })
      .then(response => response.json())
      .then(data => console.log('Actualizado:', data));
  };

  return (
    <div>
      <input
        type="text"
        value={nuevoNombre}
        onChange={(e) => setNuevoNombre(e.target.value)}
        placeholder="Nuevo nombre"
      />
      <button onClick={handleUpdate}>Actualizar</button>
    </div>
  );
}
```

4. Eliminar un trabajador (DELETE)
```js
function EliminarTrabajador({ trabajadorId, onDelete }) {
  const handleDelete = () => {
    fetch(`http://127.0.0.1:800/api/trabajadores/${trabajadorId}/`, {
      method: 'DELETE',
    })
      .then(() => {
        console.log('Trabajador eliminado');
        onDelete(trabajadorId); // Actualizar el estado en el componente padre
      });
  };

  return (
    <button onClick={handleDelete}>Eliminar</button>
  );
}
```