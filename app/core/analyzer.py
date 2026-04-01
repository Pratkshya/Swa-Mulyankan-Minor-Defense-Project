from app.core.logic import calculate_mastery, calculate_gap, classify
from collections import defaultdict

def calculate_severity_factor(question_id, attempts, is_correct):
    """
    Calculate severity factor based on number of attempts to find correct answer.
    Severity increases with more attempts (higher severity = more struggles).
    
    - 1 attempt: severity = 0 (correct on first try)
    - 2 attempts: severity = 1 (mild difficulty)
    - 3 attempts: severity = 2 (moderate difficulty)
    - 4+ attempts: severity = 3 (high difficulty)
    """
    if not is_correct:
        return 4  # Maximum severity for unanswered questions
    
    if attempts <= 1:
        return 0
    elif attempts == 2:
        return 1
    elif attempts == 3:
        return 2
    else:
        return 3


def analyze(answers, questions, attempts_data=None):
    """
    Analyze quiz responses with severity factor calculation.
    
    Args:
        answers: Dict of question_id -> selected_answer
        questions: List of question objects
        attempts_data: Dict of question_id -> number_of_attempts (optional)
    """
    if attempts_data is None:
        attempts_data = {}
    
    mastery = calculate_mastery(answers, questions)
    gap = calculate_gap(answers, questions)
    status = classify(mastery)
    
    # Calculate unit-wise performance
    unit_scores = defaultdict(list)
    severity_by_question = {}
    severity_by_unit = defaultdict(list)
    
    for q in questions:
        unit = q.get('unit', 'Unknown')
        question_id = str(q['id'])
        
        is_correct = answers.get(question_id) == q['correct_answer']
        correct_score = 1 if is_correct else 0
        unit_scores[unit].append(correct_score)
        
        # Calculate severity for this question
        attempts = int(attempts_data.get(question_id, 1)) if attempts_data else 1
        severity = calculate_severity_factor(q['id'], attempts, is_correct)
        severity_by_question[question_id] = {
            'severity': severity,
            'attempts': attempts,
            'correct': is_correct,
            'question': q['question']
        }
        severity_by_unit[unit].append(severity)
    
    # Calculate heatmap (unit-wise performance)
    heatmap = {
        unit: round(sum(scores)/len(scores), 2) if scores else 0 
        for unit, scores in unit_scores.items()
    }
    
    # Calculate average severity by unit
    severity_by_unit_avg = {
        unit: round(sum(severities)/len(severities), 2) if severities else 0
        for unit, severities in severity_by_unit.items()
    }
    
    # Generate study plan
    plan = []
    severity_analysis = {
        'by_question': severity_by_question,
        'by_unit': severity_by_unit_avg,
        'overall_severity': round(sum(s['severity'] for s in severity_by_question.values()) / 
                                   len(severity_by_question) if severity_by_question else 0, 2)
    }
    
    for unit, score in heatmap.items():
        severity = severity_by_unit_avg.get(unit, 0)
        
        if score < 0.5:
            plan.append(f"🔴 {unit} - Score: {score*100:.0f}% (Severity: {severity:.1f}/3) - Requires intensive study")
        elif score < 0.75:
            if severity >= 1.5:
                plan.append(f"🟡 {unit} - Score: {score*100:.0f}% (Severity: {severity:.1f}/3) - Review needed, multiple attempts required")
            else:
                plan.append(f"🟡 {unit} - Score: {score*100:.0f}% (Severity: {severity:.1f}/3) - Additional practice recommended")
        else:
            if severity <= 0.5:
                plan.append(f"🟢 {unit} - Score: {score*100:.0f}% (Severity: {severity:.1f}/3) - Excellent! Keep practicing to maintain")
            else:
                plan.append(f"🟡 {unit} - Score: {score*100:.0f}% (Severity: {severity:.1f}/3) - Good score but multiple attempts needed - review weak areas")
    
    if not plan:
        plan.append("🟢 Great job! Maintain your performance with regular practice.")
    
    return {
        "mastery": round(mastery, 2),
        "gap": gap,
        "status": status,
        "heatmap": heatmap,
        "plan": plan,
        "severity_analysis": severity_analysis
    }