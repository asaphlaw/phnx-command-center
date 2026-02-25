// types/index.ts

export interface SystemStatus {
  status: 'active' | 'idle' | 'error' | 'warning';
  lastRun?: string;
  message?: string;
}

export interface MCP_SERVER {
  name: string;
  status: 'connected' | 'active' | 'disconnected';
  description: string;
  impact: number;
  details?: string;
}

export interface AgentStatus {
  name: string;
  emoji: string;
  status: SystemStatus['status'];
  lastRun: string;
  queueCount: number;
  description: string;
}

export interface ProjectCard {
  id: string;
  name: string;
  status: 'active' | 'complete' | 'in_progress';
  health: number;
  lastActivity: string;
  metrics: Record<string, string | number>;
}

export interface SystemMetrics {
  cpu: number;
  memory: number;
  uptime: string;
  activeTasks: number;
  queueDepth: number;
}

export interface InfrastructureData {
  core: {
    browserUse: { status: string; version: string };
    vectorMemory: { status: string; collections: number };
    mcpClient: { status: string; servers: number };
    langGraph: { status: string; workflows: number };
  };
  rsi: {
    forager: AgentStatus;
    forge: AgentStatus;
    crucible: AgentStatus;
    warden: AgentStatus;
  };
  mcp: MCP_SERVER[];
  projects: ProjectCard[];
  metrics: SystemMetrics;
}
