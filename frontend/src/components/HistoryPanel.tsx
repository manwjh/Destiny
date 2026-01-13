/**
 * 历史记录面板组件
 */
import React, { useState, useEffect } from 'react';
import { History, X, Clock } from 'lucide-react';

interface HistoryItem {
  id: number;
  question: string;
  result: string;
  language: string;
  category: string;
  timestamp: string;
  is_night: number;
  response_time_ms: number;
}

interface HistoryPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export const HistoryPanel: React.FC<HistoryPanelProps> = ({ isOpen, onClose }) => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchHistory();
    }
  }, [isOpen]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE_URL}/api/v1/stats/user/recent?limit=20`);
      const data = await response.json();
      
      if (data.success) {
        setHistory(data.data);
      }
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto bg-gradient-to-br from-purple-900/95 to-indigo-900/95 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 animate-slide-up">
        {/* 关闭按钮 */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-300 z-10"
          aria-label="关闭"
        >
          <X className="w-5 h-5 text-white" />
        </button>

        {/* 标题 */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <History className="w-7 h-7 text-purple-300" />
            <h2 className="text-2xl font-bold text-white">
              历史记录
            </h2>
          </div>
          <p className="text-white/60 text-sm mt-2">
            最近 {history.length} 条算卦记录
          </p>
        </div>

        {/* 内容 */}
        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="destiny-spinner" />
            </div>
          ) : history.length > 0 ? (
            <div className="space-y-4">
              {history.map((item, index) => (
                <div
                  key={item.id}
                  className="bg-white/5 backdrop-blur-sm rounded-2xl p-5 border border-white/10 hover:bg-white/10 transition-all duration-300"
                >
                  {/* 问题 */}
                  <div className="mb-3">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-white/40 text-xs">#{history.length - index}</span>
                      <div className="flex items-center gap-2 text-white/60 text-xs">
                        <Clock className="w-3 h-3" />
                        <span>{new Date(item.timestamp).toLocaleString('zh-CN')}</span>
                      </div>
                      {item.is_night === 1 && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-purple-500/20 text-purple-300">
                          夜间
                        </span>
                      )}
                    </div>
                    <p className="text-white/80 font-medium">
                      {item.question}
                    </p>
                  </div>

                  {/* 结果 */}
                  <div className="pl-4 border-l-2 border-purple-500/30">
                    <p className="text-white/90 leading-relaxed">
                      {item.result}
                    </p>
                  </div>

                  {/* 元数据 */}
                  <div className="mt-3 flex items-center gap-3 text-xs text-white/40">
                    <span>响应: {item.response_time_ms}ms</span>
                    {item.category && (
                      <span className="px-2 py-0.5 rounded-full bg-white/5">
                        {item.category}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-white/60">暂无历史记录</p>
              <p className="text-white/40 text-sm mt-2">
                开始您的第一次算卦吧
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
