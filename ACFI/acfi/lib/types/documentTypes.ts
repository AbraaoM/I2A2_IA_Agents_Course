export interface DocumentChunk {
  id: string;
  content: string;
  metadata: {
    source: string;
    chunkIndex: number;
    totalChunks: number;
    wordCount: number;
    createdAt: Date;
  };
}

export interface ProcessingConfig {
  chunkSize: number;
  overlap: number;
  minChunkSize: number;
  separators: string[];
}

export interface LoadedDocument {
  path: string;
  content: string;
  metadata: {
    fileName: string;
    fileSize: number;
    fileType: string;
    loadedAt: Date;
  };
}