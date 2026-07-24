import React from 'react';

interface Props {
    actionType: string;
    details: string;
    onApprove: () => void;
    onReject: () => void;
}

export const ApprovalDialog: React.FC<Props> = ({ actionType, details, onApprove, onReject }) => {
    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-gray-800 p-6 rounded-lg max-w-md w-full border border-yellow-600 shadow-2xl">
                <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-full bg-yellow-600/20 flex items-center justify-center text-yellow-500">
                        ⚠️
                    </div>
                    <h2 className="text-xl font-bold text-white">Action Requires Approval</h2>
                </div>
                
                <div className="mb-6">
                    <p className="text-gray-300 mb-2 font-medium">The agent wants to execute:</p>
                    <div className="bg-gray-900 p-3 rounded font-mono text-sm text-yellow-400 overflow-x-auto">
                        {details}
                    </div>
                </div>
                
                <div className="flex justify-end gap-3">
                    <button 
                        onClick={onReject}
                        className="px-4 py-2 rounded bg-gray-700 hover:bg-gray-600 text-white font-medium transition-colors"
                    >
                        Reject
                    </button>
                    <button 
                        onClick={onApprove}
                        className="px-4 py-2 rounded bg-yellow-600 hover:bg-yellow-700 text-white font-medium transition-colors"
                    >
                        Approve Action
                    </button>
                </div>
            </div>
        </div>
    );
};
