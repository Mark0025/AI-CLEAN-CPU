"""Utility for analyzing and summarizing logs."""

import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime, timedelta

class LogAnalyzer:
    """Analyzes logs for patterns and insights."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
    
    def analyze_session(self, session_id: str) -> Dict[str, Any]:
        """Analyze a specific session's logs."""
        analysis = {
            'ai_interactions': self._analyze_ai_interactions(session_id),
            'operations': self._analyze_operations(session_id),
            'errors': self._analyze_errors(session_id),
            'performance': self._analyze_performance(session_id)
        }
        return analysis
    
    def _analyze_ai_interactions(self, session_id: str) -> Dict[str, Any]:
        """Analyze AI interaction patterns."""
        interactions_file = self.log_dir / "ai_interactions" / f"ai_log_{session_id}.jsonl"
        interactions = []
        
        if interactions_file.exists():
            with interactions_file.open() as f:
                for line in f:
                    interactions.append(json.loads(line))
        
        return {
            'total_interactions': len(interactions),
            'interaction_types': self._count_by_field(interactions, 'type'),
            'average_response_time': self._calculate_average_time(interactions)
        }
    
    def _analyze_operations(self, session_id: str) -> Dict[str, Any]:
        """Analyze operation patterns and success rates."""
        operations_file = self.log_dir / "operations" / f"op_log_{session_id}.jsonl"
        operations = []
        
        if operations_file.exists():
            with operations_file.open() as f:
                for line in f:
                    operations.append(json.loads(line))
        
        return {
            'total_operations': len(operations),
            'operation_types': self._count_by_field(operations, 'operation'),
            'success_rate': self._calculate_success_rate(operations)
        }
    
    def _count_by_field(self, items: List[Dict], field: str) -> Dict[str, int]:
        """Count occurrences of values in a specific field."""
        counter = defaultdict(int)
        for item in items:
            counter[item.get(field, 'unknown')] += 1
        return dict(counter)
    
    def _calculate_average_time(self, interactions: List[Dict]) -> float:
        """Calculate average time between interactions."""
        if not interactions:
            return 0.0
            
        times = [datetime.fromisoformat(i['timestamp']) for i in interactions]
        if len(times) < 2:
            return 0.0
            
        total_time = sum((t2 - t1).total_seconds() 
                        for t1, t2 in zip(times[:-1], times[1:]))
        return total_time / (len(times) - 1)
    
    def _calculate_success_rate(self, operations: List[Dict]) -> float:
        """Calculate operation success rate."""
        if not operations:
            return 0.0
            
        successes = sum(1 for op in operations if op.get('status') == 'success')
        return (successes / len(operations)) * 100
    
    def generate_report(self, session_id: str) -> str:
        """Generate a human-readable report for a session."""
        analysis = self.analyze_session(session_id)
        
        report = [
            "Log Analysis Report",
            "=" * 80,
            f"Session ID: {session_id}",
            "",
            "AI Interactions:",
            f"- Total: {analysis['ai_interactions']['total_interactions']}",
            f"- Types: {dict(analysis['ai_interactions']['interaction_types'])}",
            f"- Average Response Time: {analysis['ai_interactions']['average_response_time']:.2f}s",
            "",
            "Operations:",
            f"- Total: {analysis['operations']['total_operations']}",
            f"- Success Rate: {analysis['operations']['success_rate']:.1f}%",
            f"- Types: {dict(analysis['operations']['operation_types'])}",
            "",
            "Performance Metrics:",
            "- See detailed performance logs for timing information",
            "",
            "=" * 80
        ]
        
        return "\n".join(report) 