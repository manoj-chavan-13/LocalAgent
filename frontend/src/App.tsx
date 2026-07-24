import React, { useState, useEffect } from 'react'
import { Chat } from './components/Chat'
import { ApprovalDialog } from './components/ApprovalDialog'
import { Sidebar } from './components/Sidebar'
import { apiClient } from './api/client'

function App() {
  const [pendingApproval, setPendingApproval] = useState<any>(null);

  useEffect(() => {
    // Poll for pending approvals every 2 seconds
    const interval = setInterval(async () => {
      try {
        const data = await apiClient.getPendingApprovals();
        if (data.pending && data.pending.length > 0) {
          // Just handle the first pending approval for simplicity
          setPendingApproval(data.pending[0]);
        } else {
          setPendingApproval(null);
        }
      } catch (err) {
        console.error("Failed to poll approvals", err);
      }
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleResolve = async (approved: boolean) => {
    if (pendingApproval) {
      await apiClient.resolveApproval(pendingApproval.id, approved);
      setPendingApproval(null);
    }
  };

  return (
    <div className="flex h-screen w-full bg-gray-900 text-white">
      {/* Settings / Repo sidebar */}
      <Sidebar />
      
      {/* Main Chat Area */}
      <div className="flex flex-col flex-1 items-center pt-10">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-blue-500 mb-2">Local AI DevOps Agent</h1>
          <p className="text-gray-400">Autonomous ReAct Loop Enabled</p>
        </div>
        
        <Chat />

        {pendingApproval && (
          <ApprovalDialog 
            actionType={pendingApproval.type}
            details={pendingApproval.details}
            onApprove={() => handleResolve(true)}
            onReject={() => handleResolve(false)}
          />
        )}
      </div>
    </div>
  )
}

export default App
