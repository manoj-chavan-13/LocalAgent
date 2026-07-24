import React, { useState } from 'react';
import { apiClient } from '../api/client';

export function Sidebar() {
    const [repoPath, setRepoPath] = useState('');
    const [indexing, setIndexing] = useState(false);
    const [status, setStatus] = useState('');

    const handleIndex = async () => {
        if (!repoPath) return;
        setIndexing(true);
        setStatus('Indexing...');
        
        try {
            const result = await apiClient.indexRepository(repoPath);
            setStatus(`Indexed ${result.files_indexed} files.`);
        } catch (err) {
            setStatus('Failed to index.');
            console.error(err);
        } finally {
            setIndexing(false);
        }
    };

    return (
        <div className="w-64 bg-gray-800 border-r border-gray-700 p-4 flex flex-col">
            <h2 className="text-xl font-bold mb-6 text-blue-400">Settings</h2>
            
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                    Repository Path
                </label>
                <input 
                    type="text" 
                    value={repoPath}
                    onChange={(e) => setRepoPath(e.target.value)}
                    placeholder="/path/to/repo"
                    className="w-full bg-gray-900 border border-gray-600 rounded p-2 text-white text-sm focus:outline-none focus:border-blue-500"
                />
            </div>
            
            <button 
                onClick={handleIndex}
                disabled={indexing || !repoPath}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:text-gray-400 text-white font-medium py-2 px-4 rounded transition-colors"
            >
                {indexing ? 'Scanning...' : 'Index Codebase'}
            </button>
            
            {status && (
                <p className="mt-4 text-sm text-green-400">
                    {status}
                </p>
            )}
            
            <div className="mt-auto pt-6 border-t border-gray-700">
                <p className="text-xs text-gray-500 text-center">
                    Agent connected to local ChromaDB & Ollama instance.
                </p>
            </div>
        </div>
    );
}
