// Funções de Modal
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Fechar modal ao clicar fora
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        hideModal(e.target.id);
    }
});

// Funções de Formulário
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });

    return isValid;
}

// Funções de Formatação
function formatDate(date) {
    if (!date) return '';
    const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
    return new Date(date).toLocaleDateString('pt-BR', options);
}

function formatTime(time) {
    if (!time) return '';
    return time.substring(0, 5);
}

function formatCurrency(value) {
    if (!value) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Funções de Tabela
function sortTable(tableId, columnIndex) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const isAscending = table.dataset.sortDirection === 'asc';

    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();

        if (isNaN(aValue) && isNaN(bValue)) {
            return isAscending
                ? aValue.localeCompare(bValue)
                : bValue.localeCompare(aValue);
        }

        return isAscending
            ? parseFloat(aValue) - parseFloat(bValue)
            : parseFloat(bValue) - parseFloat(aValue);
    });

    table.dataset.sortDirection = isAscending ? 'desc' : 'asc';
    rows.forEach(row => tbody.appendChild(row));
}

// Funções de Notificação
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Funções de Filtro
function filterTable(tableId, searchTerm) {
    const table = document.getElementById(tableId);
    if (!table) return;

    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');

    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm.toLowerCase()) ? '' : 'none';
    });
}

// Funções de Paginação
function updatePagination(currentPage, totalPages) {
    const pagination = document.querySelector('.pagination');
    if (!pagination) return;

    let html = '';

    // Botão Anterior
    html += `
        <button class="btn btn-secondary" onclick="changePage(${currentPage - 1})" 
                ${currentPage === 1 ? 'disabled' : ''}>
            <i class="fas fa-chevron-left"></i> Anterior
        </button>
    `;

    // Números das páginas
    for (let i = 1; i <= totalPages; i++) {
        if (
            i === 1 ||
            i === totalPages ||
            (i >= currentPage - 2 && i <= currentPage + 2)
        ) {
            html += `
                <button class="btn ${i === currentPage ? 'btn-primary' : 'btn-secondary'}"
                        onclick="changePage(${i})">
                    ${i}
                </button>
            `;
        } else if (
            i === currentPage - 3 ||
            i === currentPage + 3
        ) {
            html += '<span class="pagination-ellipsis">...</span>';
        }
    }

    // Botão Próximo
    html += `
        <button class="btn btn-secondary" onclick="changePage(${currentPage + 1})"
                ${currentPage === totalPages ? 'disabled' : ''}>
            Próximo <i class="fas fa-chevron-right"></i>
        </button>
    `;

    pagination.innerHTML = html;
}

// Funções de Armazenamento Local
const storage = {
    set: (key, value) => {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Erro ao salvar no localStorage:', error);
            return false;
        }
    },
    get: (key) => {
        try {
            const value = localStorage.getItem(key);
            return value ? JSON.parse(value) : null;
        } catch (error) {
            console.error('Erro ao ler do localStorage:', error);
            return null;
        }
    },
    remove: (key) => {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Erro ao remover do localStorage:', error);
            return false;
        }
    }
};

// Funções de Máscara de Input
function applyMask(input, mask) {
    if (!input) return;

    input.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, '');
        let result = '';

        for (let i = 0, j = 0; i < mask.length && j < value.length; i++) {
            if (mask[i] === '#') {
                result += value[j];
                j++;
            } else {
                result += mask[i];
            }
        }

        e.target.value = result;
    });
}

// Inicialização de Máscaras
document.addEventListener('DOMContentLoaded', () => {
    // CPF
    const cpfInputs = document.querySelectorAll('input[data-mask="cpf"]');
    cpfInputs.forEach(input => applyMask(input, '###.###.###-##'));

    // Telefone
    const phoneInputs = document.querySelectorAll('input[data-mask="phone"]');
    phoneInputs.forEach(input => applyMask(input, '(##) #####-####'));

    // Data
    const dateInputs = document.querySelectorAll('input[data-mask="date"]');
    dateInputs.forEach(input => applyMask(input, '##/##/####'));

    // Hora
    const timeInputs = document.querySelectorAll('input[data-mask="time"]');
    timeInputs.forEach(input => applyMask(input, '##:##'));
});

// Funções de Validação
const validation = {
    cpf: (cpf) => {
        cpf = cpf.replace(/[^\d]/g, '');

        if (cpf.length !== 11) return false;

        // Verifica CPFs inválidos conhecidos
        if (/^(\d)\1+$/.test(cpf)) return false;

        let sum = 0;
        let remainder;

        for (let i = 1; i <= 9; i++) {
            sum += parseInt(cpf.substring(i - 1, i)) * (11 - i);
        }

        remainder = (sum * 10) % 11;
        if (remainder === 10 || remainder === 11) remainder = 0;
        if (remainder !== parseInt(cpf.substring(9, 10))) return false;

        sum = 0;
        for (let i = 1; i <= 10; i++) {
            sum += parseInt(cpf.substring(i - 1, i)) * (12 - i);
        }

        remainder = (sum * 10) % 11;
        if (remainder === 10 || remainder === 11) remainder = 0;
        if (remainder !== parseInt(cpf.substring(10, 11))) return false;

        return true;
    },

    email: (email) => {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    },

    phone: (phone) => {
        phone = phone.replace(/[^\d]/g, '');
        return phone.length >= 10 && phone.length <= 11;
    },

    date: (date) => {
        const [day, month, year] = date.split('/');
        const d = new Date(year, month - 1, day);
        return d && d.getMonth() + 1 === parseInt(month) && d.getDate() === parseInt(day);
    },

    time: (time) => {
        return /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/.test(time);
    }
};

// Funções de API
const api = {
    get: async (url, options = {}) => {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erro na requisição GET:', error);
            throw error;
        }
    },

    post: async (url, data, options = {}) => {
        try {
            const response = await fetch(url, {
                method: 'POST',
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erro na requisição POST:', error);
            throw error;
        }
    },

    put: async (url, data, options = {}) => {
        try {
            const response = await fetch(url, {
                method: 'PUT',
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erro na requisição PUT:', error);
            throw error;
        }
    },

    delete: async (url, options = {}) => {
        try {
            const response = await fetch(url, {
                method: 'DELETE',
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Erro na requisição DELETE:', error);
            throw error;
        }
    }
};

// Exportar funções
window.utils = {
    showModal,
    hideModal,
    validateForm,
    formatDate,
    formatTime,
    formatCurrency,
    sortTable,
    showNotification,
    filterTable,
    updatePagination,
    storage,
    applyMask,
    validation,
    api
}; 