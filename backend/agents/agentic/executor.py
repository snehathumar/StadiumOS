import datetime
from typing import Dict, Any
from backend.ai_brain.agentic.models import ExecutionPlan, AuditLogEntry
from backend.ai_brain.agentic.tools import TOOL_REGISTRY
from backend.ai_brain.agentic.audit import audit_store
from backend.agents.evaluation.decision_logger import decision_logger

class ExecutionEngine:
    """
    Safely executes an approved ExecutionPlan via the Tool Registry.
    Guarantees Human-in-the-Loop constraint: only processes 'APPROVED' plans.
    """
    
    def execute_plan(self, plan: ExecutionPlan, operator_request: str) -> ExecutionPlan:
        # Strict state check
        if plan.status != "APPROVED":
            plan.status = "FAILED"
            return plan
            
        plan.status = "EXECUTING"
        all_tools_used = []
        has_failure = False
        
        for task in plan.tasks:
            task.status = "IN_PROGRESS"
            task_success = True
            
            for call in task.tool_calls:
                all_tools_used.append(call.tool_name)
                
                # 1. Lookup Tool
                tool_func = TOOL_REGISTRY.get(call.tool_name)
                if not tool_func:
                    task.result_message = f"Tool '{call.tool_name}' not found."
                    task_success = False
                    break
                    
                # 2. Execute Tool
                try:
                    result = tool_func(**call.arguments)
                    task.result_message = f"Success: {result}"
                except Exception as e:
                    task.result_message = f"Execution Error: {str(e)}"
                    task_success = False
                    break
                    
            if task_success:
                task.status = "COMPLETED"
            else:
                task.status = "FAILED"
                has_failure = True
                # Critical safety feature: Halt pipeline on first task failure
                break 
                
        if has_failure:
            plan.status = "FAILED"
        else:
            plan.status = "SUCCESS"
            
        # 3. Create Immutable Audit Log
        audit_entry = AuditLogEntry(
            timestamp=datetime.datetime.utcnow().isoformat(),
            operator_request=operator_request,
            plan_id=plan.plan_id,
            tools_used=all_tools_used,
            execution_status=plan.status
        )
        audit_store.add_entry(audit_entry)
        
        # 4. Log Decision for Evaluation
        decision_logger.log(
            source="Agentic Ops", 
            input_context=operator_request, 
            output_decision=f"Executed Plan {plan.plan_id} with Status: {plan.status}"
        )
        
        return plan

executor_engine = ExecutionEngine()
