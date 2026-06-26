from models.knowledge_base import KnowledgeBase

class RuleEngine:
    @staticmethod
    def get_fallback_reply(email_body):
        kb_entries = KnowledgeBase.query.filter_by(status='Active').all()
        
        best_match = None
        max_keywords_matched = 0
        
        email_body_lower = email_body.lower()
        
        for kb in kb_entries:
            if not kb.keywords:
                continue
            keywords = [k.strip().lower() for k in kb.keywords.split(',')]
            matched = sum(1 for k in keywords if k in email_body_lower)
            
            if matched > max_keywords_matched:
                max_keywords_matched = matched
                best_match = kb.answer
                
        if max_keywords_matched > 0:
            return best_match
        return None
