import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, Cpu, Database, GitBranch, Globe, Layers, Shield, Zap, Terminal, LayoutDashboard } from 'lucide-react';
import './index.css';

// Types
interface AgentStatus {
  name: string;
  emoji: string;
  status: 'active' | 'idle' | 'error';
  lastRun: string;
  queueCount: number;
}

interface MCPServer {
  name: string;
  status: 'connected' | 'active' | 'disconnected';
  icon: React.ReactNode;
  details?: string;
}

interface Project {
  id: string;
  name: string;
  status: 'active' | 'complete';
  health: number;
  metric: string;
  value: string;
}

// Sample Data
const infrastructureData = {
  agents: [
    { name: 'Forager', emoji: '🤖', status: 'idle' as const, lastRun: '2m ago', queueCount: 12 },
    { name: 'Forge', emoji: '🔨', status: 'idle' as const, lastRun: '2m ago', queueCount: 12 },
    { name: 'Crucible', emoji: '🔥', status: 'idle' as const, lastRun: '2m ago', queueCount: 12 },
    { name: 'Warden', emoji: '🛡️', status: 'idle' as const, lastRun: '2m ago', queueCount: 20 },
  ],
  mcpServers: [
    { name: 'GitHub', status: 'connected' as const, icon: <GitBranch size={20} />, details: 'fredericklaw' },
    { name: 'Google', status: 'connected' as const, icon: <Globe size={20} />, details: 'Gmail/Calendar' },
    { name: 'Filesystem', status: 'active' as const, icon: <Database size={20} /> },
    { name: 'Fetch', status: 'active' as const, icon: <Zap size={20} /> },
    { name: 'Git', status: 'active' as const, icon: <GitBranch size={20} /> },
    { name: 'SQLite', status: 'active' as const, icon: <Database size={20} /> },
  ],
  projects: [
    { id: '1', name: 'RSI System', status: 'active' as const, health: 100, metric: 'Proposals', value: '12' },
    { id: '2', name: 'PT Booking Bot', status: 'active' as const, health: 100, metric: 'Status', value: 'Ready' },
    { id: '3', name: 'Browser-Use', status: 'complete' as const, health: 100, metric: 'Version', value: '0.11.13' },
    { id: '4', name: 'MCP Suite', status: 'complete' as const, health: 100, metric: 'Servers', value: '6' },
  ],
};

// Components
const StatusIndicator: React.FC<{ status: string; size?: 'sm' | 'md' | 'lg' }> = ({ status, size = 'md' }) => {
  const colors = {
    active: 'bg-green-500',
    idle: 'bg-yellow-500',
    error: 'bg-red-500',
    connected: 'bg-green-500',
    complete: 'bg-blue-500',
  };
  
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
  };
  
  return (
    <motion.div
      className={`${colors[status as keyof typeof colors] || 'bg-gray-500'} ${sizeClasses[size]} rounded-full`}
      animate={{ opacity: [1, 0.5, 1] }}
      transition={{ duration: 2, repeat: Infinity }}
    />
  );
};

const Card: React.FC<{ children: React.ReactNode; title?: string; className?: string }> = ({ children, title, className = '' }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className={`bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-xl p-6 ${className}`}
  >
    {title && <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">{title}</h3>}
    {children}
  </motion.div>
);

const MetricBox: React.FC<{ label: string; value: string; unit?: string }> = ({ label, value, unit }) => (
  <div className="bg-slate-800/50 rounded-lg p-4">
    <p className="text-slate-400 text-sm">{label}</p>
    <p className="text-2xl font-bold text-white">{value}<span className="text-sm text-slate-400 ml-1">{unit}</span></p>
  </div>
);

// Main App
function App() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [command, setCommand] = useState('');
  const [output, setOutput] = useState<string[]>(['PHNX Command Center v2.0 initialized...', 'All systems operational.']);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const handleCommand = (e: React.FormEvent) => {
    e.preventDefault();
    if (!command.trim()) return;
    
    setOutput(prev => [...prev, `> ${command}`, `Executing: ${command}...`]);
    
    // Simulate command response
    setTimeout(() => {
      const responses: Record<string, string> = {
        'status': 'All systems operational. RSI: 4/4 pillars active. MCP: 6 servers connected.',
        'agents': 'Forager: idle, Forge: idle, Crucible: idle, Warden: idle',
        'help': 'Available commands: status, agents, mcp, projects, clear',
      };
      setOutput(prev => [...prev, responses[command.toLowerCase()] || `Command executed: ${command}`]);
    }, 500);
    
    setCommand('');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white font-mono">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Layers className="text-cyan-400" size={28} />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
              PHNX COMMAND CENTER
            </h1>
          </div>
          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-2">
              <StatusIndicator status="active" />
              <span className="text-green-400">OPERATIONAL</span>
            </div>
            <span className="text-slate-400">{currentTime.toLocaleTimeString()}</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Infrastructure Health */}
          <Card title={<><Activity className="text-cyan-400" /> Infrastructure Health</>}>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
                <span className="flex items-center gap-2"><Cpu size={16} /> PHNX Core</span>
                <StatusIndicator status="active" />
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
                <span className="flex items-center gap-2"><Shield size={16} /> RSI System</span>
                <StatusIndicator status="active" />
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
                <span className="flex items-center gap-2"><Database size={16} /> Vector Memory</span>
                <StatusIndicator status="active" />
              </div>
              <div className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
                <span className="flex items-center gap-2"><Globe size={16} /> MCP Client (6)</span>
                <StatusIndicator status="connected" />
              </div>
            </div>
          </Card>

          {/* Agent Swarm */}
          <Card title={<><LayoutDashboard className="text-purple-400" /> Agent Swarm</>}>
            <div className="space-y-3">
              {infrastructureData.agents.map((agent) => (
                <div key={agent.name} className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <span>{agent.emoji}</span>
                    <div>
                      <p className="font-medium">{agent.name}</p>
                      <p className="text-xs text-slate-400">Queue: {agent.queueCount}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-400">{agent.lastRun}</span>
                    <StatusIndicator status={agent.status} />
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* Metrics */}
          <Card title={<><Terminal className="text-green-400" /> Real-time Metrics</>}>
            <div className="grid grid-cols-2 gap-3">
              <MetricBox label="CPU" value="23" unit="%" />
              <MetricBox label="Memory" value="1.2" unit="GB" />
              <MetricBox label="Uptime" value="4h 32m" />
              <MetricBox label="Tasks" value="3" />
            </div>
            <div className="mt-4 pt-4 border-t border-slate-700">
              <p className="text-xs text-slate-400">Queue Depth: <span className="text-cyan-400">12 items</span></p>
            </div>
          </Card>
        </div>

        {/* Project Dashboard */}
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Layers className="text-cyan-400" /> Project Dashboard
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {infrastructureData.projects.map((project) => (
              <Card key={project.id} className="hover:border-cyan-500/50 transition-colors cursor-pointer">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-lg">{project.name}</h4>
                  <StatusIndicator status={project.status} size="sm" />
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-slate-400">{project.metric}</span>
                  <span className="text-cyan-400 font-mono">{project.value}</span>
                </div>
                <div className="mt-3 pt-3 border-t border-slate-700">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-400">Health</span>
                    <span className="text-xs text-green-400">{project.health}%</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2 mt-1">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: `${project.health}%` }} />
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* MCP Servers */}
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Globe className="text-purple-400" /> MCP Servers
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            {infrastructureData.mcpServers.map((server) => (
              <div key={server.name} className="bg-slate-900/50 border border-slate-700 rounded-lg p-4 text-center hover:border-cyan-500/50 transition-colors">
                <div className="flex justify-center mb-2 text-cyan-400">{server.icon}</div>
                <p className="font-medium text-sm">{server.name}</p>
                <div className="flex items-center justify-center gap-1 mt-2">
                  <StatusIndicator status={server.status} size="sm" />
                  <span className="text-xs text-slate-400">{server.status}</span>
                </div>
                {server.details && <p className="text-xs text-slate-500 mt-1">{server.details}</p>}
              </div>
            ))}
          </div>
        </div>

        {/* Command Interface */}
        <Card title={<><Terminal className="text-yellow-400" /> Command Interface</>} className="mt-6">
          <div className="bg-slate-950 rounded-lg p-4 font-mono text-sm h-48 overflow-y-auto border border-slate-800">
            {output.map((line, i) => (
              <div key={i} className={line.startsWith('>') ? 'text-cyan-400' : 'text-slate-300'}>
                {line}
              </div>
            ))}
          </div>
          <form onSubmit={handleCommand} className="mt-4 flex gap-2">
            <span className="text-cyan-400 py-2">{'>'}</span>
            <input
              type="text"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              className="flex-1 bg-transparent border-none outline-none text-white font-mono"
              placeholder="Enter command (try: status, agents, help)"
            />
          </form>
          <div className="mt-4 flex gap-2 flex-wrap">
            {['Run Forager', 'Check Status', 'View Reports', 'System Health'].map((action) => (
              <button
                key={action}
                onClick={() => setCommand(action.toLowerCase().replace(' ', '_'))}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm transition-colors"
              >
                {action}
              </button>
            ))}
          </div>
        </Card>
      </main>
    </div>
  );
}

export default App;
