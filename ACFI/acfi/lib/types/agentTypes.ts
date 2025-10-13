export interface AgentConfig {
  name: string;
  description: string;
  model: string;
  temperature: number;
  maxTokens: number;
}

export interface AgentMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

export interface AgentSession {
  id: string;
  userId?: string;
  messages: AgentMessage[];
  config: AgentConfig;
  createdAt: Date;
  updatedAt: Date;
}

export interface AgentResponse {
  message: string;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
}