// ============================================================================
// CONFIGURATION
// ============================================================================

const API_URL = 'http://localhost:8000/api/v1/agent';

// ============================================================================
// STATE MANAGEMENT
// ============================================================================

let sessionId = localStorage.getItem('session_id') || null;
let isWaitingForResponse = false;

// ============================================================================
// DOM ELEMENTS
// ============================================================================

const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const sessionStatus = document.getElementById('session-status');
const resetBtn = document.getElementById('reset-btn');
const propertiesContainer = document.getElementById('properties-container');
const propertiesList = document.getElementById('properties-list');
const closePropertiesBtn = document.getElementById('close-properties-btn');
const loadingSpinner = document.getElementById('loading');

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    updateSessionStatus();
    setupEventListeners();
    
    // Show welcome message if no session
    if (!sessionId) {
        showWelcomeMessage();
    }
});

function setupEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    resetBtn.addEventListener('click', resetSession);
    closePropertiesBtn.addEventListener('click', closeProperties);
}

// ============================================================================
// SESSION MANAGEMENT
// ============================================================================

function updateSessionStatus() {
    if (sessionId) {
        sessionStatus.textContent = `Session: ${sessionId.substring(0, 8)}...`;
    } else {
        sessionStatus.textContent = 'No active session';
    }
}

function resetSession() {
    if (confirm('¿Seguro que quieres iniciar una nueva búsqueda?')) {
        sessionId = null;
        localStorage.removeItem('session_id');
        chatContainer.innerHTML = '';
        showWelcomeMessage();
        updateSessionStatus();
        messageInput.value = '';
    }
}

function showWelcomeMessage() {
    chatContainer.innerHTML = `
        <div class="welcome-message">
            <div class="bot-icon">🏠</div>
            <h2>¡Hola! Soy tu asistente inmobiliario</h2>
            <p>Estoy aquí para ayudarte a encontrar la propiedad perfecta.</p>
            <p><strong>Ejemplos de búsqueda:</strong></p>
            <p style="font-size: 14px; color: var(--text-light);">
                • "Busco un departamento en La Molina de 2 ambientes"<br>
                • "Quiero un depto de 80m² en San Isidro"<br>
                • "Necesito 3 dormitorios con balcón"
            </p>
            <p>Cuéntame qué estás buscando...</p>
        </div>
    `;
}

// ============================================================================
// MESSAGE HANDLING
// ============================================================================

async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || isWaitingForResponse) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    messageInput.value = '';
    
    // Disable input while waiting
    isWaitingForResponse = true;
    sendBtn.disabled = true;
    messageInput.disabled = true;
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_URL}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update session ID if new
        if (data.session_id && data.session_id !== sessionId) {
            sessionId = data.session_id;
            localStorage.setItem('session_id', sessionId);
            updateSessionStatus();
        }
        
        // Add bot response to chat
        addMessageToChat('bot', data.reply);
        
        // Check if properties are available
        if (data.data && Array.isArray(data.data) && data.data.length > 0) {
            setTimeout(() => {
                displayProperties(data.data);
            }, 500);
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        addMessageToChat('bot', 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.');
    } finally {
        showLoading(false);
        isWaitingForResponse = false;
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

function addMessageToChat(sender, text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const now = new Date();
    const time = now.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
    
    const avatar = sender === 'bot' ? '🤖' : '👤';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-text">${escapeHtml(text)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ============================================================================
// PROPERTIES DISPLAY
// ============================================================================

function displayProperties(properties) {
    if (!properties || properties.length === 0) {
        propertiesList.innerHTML = '<div class="no-properties">No se encontraron propiedades que coincidan con tus criterios.</div>';
    } else {
        propertiesList.innerHTML = properties.map(prop => createPropertyCard(prop)).join('');
    }
    
    propertiesContainer.classList.remove('hidden');
}

function createPropertyCard(property) {
    // Extract property details
    const titulo = property.titulo || 'Propiedad sin título';
    const valorComercial = formatCurrency(property.valor_comercial);
    const distrito = property.distrito || 'Distrito no especificado';
    const areaM2 = property.area_m2 || 0;
    const dormitorios = property.dormitorios || 0;
    const banios = property.banios || 0;
    const estado = property.estado || 'No especificado';
    
    // Extract optional features
    const features = [];
    if (property.pet_friendly) features.push('Pet Friendly');
    if (property.balcon) features.push('Balcón');
    if (property.terraza) features.push('Terraza');
    if (property.amoblado) features.push('Amoblado');
    
    const featuresHtml = features.length > 0 
        ? `<div class="property-features">${features.map(f => `<span class="feature-badge">${f}</span>`).join('')}</div>`
        : '';
    
    // Build card HTML
    return `
        <div class="property-card">
            <div class="property-header">
                <div class="property-title">${escapeHtml(titulo)}</div>
                <div class="property-price">${valorComercial}</div>
            </div>
            
            <div class="property-details">
                <div class="detail-item">
                    <span>📐</span>
                    <span>${areaM2} m²</span>
                </div>
                <div class="detail-item">
                    <span>🛏️</span>
                    <span>${dormitorios} dormitorios</span>
                </div>
                <div class="detail-item">
                    <span>🚿</span>
                    <span>${banios} baños</span>
                </div>
                <div class="detail-item">
                    <span>🏗️</span>
                    <span>${escapeHtml(estado)}</span>
                </div>
            </div>
            
            ${featuresHtml}
            
            <div class="property-location">
                📍 ${escapeHtml(distrito)}
            </div>
        </div>
    `;
}

function closeProperties() {
    propertiesContainer.classList.add('hidden');
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function formatCurrency(value) {
    if (!value) return 'Precio a consultar';
    
    return new Intl.NumberFormat('es-AR', {
        style: 'currency',
        currency: 'ARS',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showLoading(show) {
    if (show) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}
