const API_BASE_URL = 'http://localhost:8000/api/v1';

export const apiClient = {
    async sendMessage(message: string, sessionId?: string) {
        const response = await fetch(`${API_BASE_URL}/chat/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message, session_id: sessionId })
        });
        
        if (!response.ok) {
            throw new Error('Failed to send message');
        }
        
        return response.body;
    },

    async indexRepository(path: string) {
        const response = await fetch(`${API_BASE_URL}/repo/index`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ repository_path: path })
        });
        return response.json();
    }
};
