document.addEventListener('DOMContentLoaded', () => {
    const retosGrid = document.getElementById('retosGrid');
    const sidebarForm = document.getElementById('sidebarForm');
    const retoForm = document.getElementById('retoForm');
    const addRetoBtn = document.getElementById('addRetoBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    const categoriaFilter = document.getElementById('categoriaFilter');
    const dificultadFilter = document.getElementById('dificultadFilter');

    // Función para obtener y mostrar los retos
    const obtenerRetos = async (filtros = {}) => {
        let url = 'http://127.0.0.1:5000/retos';
        const params = new URLSearchParams(filtros);
        if (params.toString()) {
            url += '?' + params.toString();
        }

        const respuesta = await fetch(url);
        const retos = await respuesta.json();

        retosGrid.innerHTML = '';
        retos.forEach(reto => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <div class="card-title">${reto.titulo}</div>
                <div class="card-desc">${reto.descripcion}</div>
                <div class="card-meta">
                    <span>Categoría: ${reto.categoria}</span>
                    <span>Dificultad: ${reto.dificultad}</span>
                </div>
                <div class="card-actions">
                    <select class="estado-select" data-id="${reto.id}">
                        <option value="pendiente" ${reto.estado === 'pendiente' ? 'selected' : ''}>Pendiente</option>
                        <option value="en proceso" ${reto.estado === 'en proceso' ? 'selected' : ''}>En Proceso</option>
                        <option value="completado" ${reto.estado === 'completado' ? 'selected' : ''}>Completado</option>
                    </select>
                    <button class="delete-btn" data-id="${reto.id}">
                        <span class="material-symbols-outlined">delete</span>
                    </button>
                </div>
            `;
            retosGrid.appendChild(card);
        });
    };

    // Eventos para abrir y cerrar el panel lateral del formulario
    addRetoBtn.addEventListener('click', () => {
        sidebarForm.classList.add('open');
    });

    closeSidebarBtn.addEventListener('click', () => {
        sidebarForm.classList.remove('open');
    });

    // Evento para enviar el formulario de nuevo reto
    retoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(retoForm);
        const nuevoReto = Object.fromEntries(formData.entries());

        await fetch('http://127.0.0.1:5000/retos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(nuevoReto)
        });

        sidebarForm.classList.remove('open');
        retoForm.reset();
        obtenerRetos();
    });

    // Evento para los filtros de categoría y dificultad
    categoriaFilter.addEventListener('change', () => {
        obtenerRetos({ categoria: categoriaFilter.value, dificultad: dificultadFilter.value });
    });

    dificultadFilter.addEventListener('change', () => {
        obtenerRetos({ categoria: categoriaFilter.value, dificultad: dificultadFilter.value });
    });
    
    // Evento para el cambio de estado y eliminación
    retosGrid.addEventListener('change', async (e) => {
        if (e.target.classList.contains('estado-select')) {
            const retoId = e.target.dataset.id;
            const nuevoEstado = e.target.value;
            await fetch(`http://127.0.0.1:5000/retos/${retoId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ estado: nuevoEstado })
            });
            obtenerRetos();
        }
    });

    retosGrid.addEventListener('click', async (e) => {
        if (e.target.closest('.delete-btn')) {
            const retoId = e.target.closest('.delete-btn').dataset.id;
            await fetch(`http://127.0.0.1:5000/retos/${retoId}`, {
                method: 'DELETE'
            });
            obtenerRetos();
        }
    });

    // Cargar los retos al iniciar la página
    obtenerRetos();
});