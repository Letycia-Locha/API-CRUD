document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const form = document.getElementById('licaoForm');
    const licoesDiv = document.getElementById('licoesExistentes');

    // Função de login para obter o token JWT
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch('http://127.0.0.1:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password,
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao realizar login. Verifique as credenciais.');
            }
            return response.json();
        })
        .then(data => {
            // Armazena o token JWT no localStorage
            localStorage.setItem('accessToken', data.access);
            localStorage.setItem('refreshToken', data.refresh);
            console.log('Login realizado com sucesso');
        })
        .catch(error => console.error('Erro ao realizar login:', error));
    });

    // Função para carregar lições existentes
    function carregarLicoes() {
        const token = localStorage.getItem('accessToken');
        if (!token) {
            console.error('Usuário não autenticado. Token JWT não encontrado.');
            return;
        }

        fetch('http://127.0.0.1:8000/licoes/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar lições, verifique a autenticação.');
            }
            return response.json();
        })
        .then(data => {
            licoesDiv.innerHTML = '';
            data.forEach(licao => {
                licoesDiv.innerHTML += `
                    <div>
                        <h3>${licao.titulo}</h3>
                        <div>${licao.conteudo_html}</div>
                        <button onclick="editarLicao(${licao.id})">Editar</button>
                    </div>
                `;
            });
        })
        .catch(error => console.error('Erro ao carregar lições:', error));
    }

    // Carregar lições ao iniciar a página
    carregarLicoes();

    // Enviar nova lição
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const titulo = document.getElementById('titulo').value;
        const conteudo = document.getElementById('conteudo').value;
        const token = localStorage.getItem('accessToken');

        if (!token) {
            console.error('Usuário não autenticado. Token JWT não encontrado.');
            return;
        }

        fetch('http://127.0.0.1:8000/licoes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                titulo: titulo,
                conteudo_html: conteudo
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao criar lição. Verifique a autenticação e os dados enviados.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Lição criada:', data);
            form.reset();
            carregarLicoes(); // Recarrega a lista de lições
        })
        .catch(error => console.error('Erro ao criar lição:', error));
    });
});

// Função para editar uma lição
function editarLicao(id) {
    const novoConteudo = prompt("Digite o novo conteúdo HTML:");
    if (novoConteudo) {
        const token = localStorage.getItem('accessToken');

        if (!token) {
            console.error('Usuário não autenticado. Token JWT não encontrado.');
            return;
        }

        fetch(`http://127.0.0.1:8000/licoes/${id}/editar-html/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                conteudo_html: novoConteudo
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao atualizar lição. Verifique a autenticação e o endpoint.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Lição atualizada:', data);
            carregarLicoes(); // Recarrega a lista de lições
        })
        .catch(error => console.error('Erro ao atualizar lição:', error));
    }
}
