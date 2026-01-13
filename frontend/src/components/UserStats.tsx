/**
 * 用户统计组件
 */
import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Clock, Moon, X } from 'lucide-react';

interface UserStatsData {
  user_id: string;
  total_visits: number;
  total_interactions: number;
  first_visit: string;
  last_visit: string;
  avg_response_time_ms: number;
  night_mode_usage: number;
  categories: Record<string, number>;
}

interface UserStatsProps {
  isOpen: boolean;
  onClose: () => void;
}

export const UserStats: React.FC<UserStatsProps> = ({ isOpen, onClose }) => {
  const [stats, setStats] = useState<UserStatsData | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchStats();
    }
  }, [isOpen]);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_BASE_URL}/api/v1/stats/user`);
      const data = await response.json();
      
      if (data.success) {
        setStats(data.data);
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error);
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
            <BarChart3 className="w-7 h-7 text-purple-300" />
            <h2 className="text-2xl font-bold text-white">
              个人统计
            </h2>
          </div>
          <p className="text-white/60 text-sm mt-2">
            您的算卦记录和使用分析
          </p>
        </div>

        {/* 内容 */}
        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="destiny-spinner" />
            </div>
          ) : stats ? (
            <div className="space-y-6">
              {/* 总体统计 */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-4 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="w-4 h-4 text-green-400" />
                    <span className="text-white/60 text-sm">总访问次数</span>
                  </div>
                  <p className="text-3xl font-bold text-white">{stats.total_visits}</p>
                </div>

                <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-4 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <BarChart3 className="w-4 h-4 text-blue-400" />
                    <span className="text-white/60 text-sm">算卦次数</span>
                  </div>
                  <p className="text-3xl font-bold text-white">{stats.total_interactions}</p>
                </div>

                <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-4 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <Clock className="w-4 h-4 text-yellow-400" />
                    <span className="text-white/60 text-sm">平均响应</span>
                  </div>
                  <p className="text-3xl font-bold text-white">
                    {(stats.avg_response_time_ms / 1000).toFixed(1)}s
                  </p>
                </div>

                <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-4 border border-white/10">
                  <div className="flex items-center gap-2 mb-2">
                    <Moon className="w-4 h-4 text-purple-400" />
                    <span className="text-white/60 text-sm">夜间使用</span>
                  </div>
                  <p className="text-3xl font-bold text-white">
                    {(stats.night_mode_usage * 100).toFixed(0)}%
                  </p>
                </div>
              </div>

              {/* 问题类别分布 */}
              {Object.keys(stats.categories).length > 0 && (
                <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-5 border border-white/10">
                  <h3 className="text-white font-semibold mb-4">问题类别分布</h3>
                  <div className="space-y-3">
                    {Object.entries(stats.categories).map(([category, count]) => {
                      const total = stats.total_interactions;
                      const percentage = (count / total) * 100;
                      
                      const categoryNames: Record<string, string> = {
                        career: '事业',
                        love: '感情',
                        health: '健康',
                        wealth: '财运',
                        study: '学业',
                        relationship: '人际',
                        decision: '决策',
                        future: '未来',
                        general: '通用'
                      };

                      return (
                        <div key={category}>
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-white/80">{categoryNames[category] || category}</span>
                            <span className="text-white/60">{count}次 ({percentage.toFixed(0)}%)</span>
                          </div>
                          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all duration-500"
                              style={{ width: `${percentage}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 访问时间 */}
              <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-5 border border-white/10">
                <h3 className="text-white font-semibold mb-3">使用时间</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-white/60">首次访问</span>
                    <span className="text-white/90">
                      {new Date(stats.first_visit).toLocaleDateString('zh-CN')}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/60">最后访问</span>
                    <span className="text-white/90">
                      {new Date(stats.last_visit).toLocaleDateString('zh-CN')}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-white/60">暂无统计数据</p>
            </div>
          )}
        </div>

        {/* 底部 */}
        <div className="p-6 border-t border-white/10">
          <p className="text-white/40 text-xs text-center">
            数据基于您的使用记录，完全匿名化处理
          </p>
        </div>
      </div>
    </div>
  );
};
